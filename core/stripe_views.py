from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework.response import Response
from .stripe_service import init_stripe
import stripe
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def stripe_config(request):
    return JsonResponse({
        'publicKey': settings.STRIPE_PUBLIC_KEY,
        'currency': settings.STRIPE_CURRENCY,
    })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create_checkout_session(request):
    try:
        s = init_stripe()
        data = request.data or {}
        plan_id = data.get('plan_id')
        price_id = data.get('price_id')
        amount = data.get('amount')  # in cents
        currency = data.get('currency', settings.STRIPE_CURRENCY)
        mode = data.get('mode', 'payment')

        # Permite sobreescribir rutas de éxito/cancelación para usar páginas backend
        success_path = data.get('success_path')  # e.g. '/api/payments/success'
        cancel_path = data.get('cancel_path')    # e.g. '/api/payments/cancel'

        if success_path:
            # Asegura URL absoluta
            if success_path.startswith('http://') or success_path.startswith('https://'):
                success_url = f"{success_path}?session_id={{CHECKOUT_SESSION_ID}}"
            else:
                success_url = request.build_absolute_uri(success_path) + '?session_id={CHECKOUT_SESSION_ID}'
        else:
            # Default: redirect to backend callback to ensure DB update before frontend load
            callback_url = request.build_absolute_uri(reverse('stripe-payment-success'))
            success_url = f"{callback_url}?session_id={{CHECKOUT_SESSION_ID}}"

        if cancel_path:
            if cancel_path.startswith('http://') or cancel_path.startswith('https://'):
                cancel_url = cancel_path
            else:
                cancel_url = request.build_absolute_uri(cancel_path)
        else:
            backend_cancel = '/api/payments/cancel'
            cancel_url = request.build_absolute_uri(backend_cancel)

        if plan_id:
            from .models import Plan
            try:
                plan = Plan.objects.get(pk=plan_id, is_active=True)
            except Plan.DoesNotExist:
                return JsonResponse({'detail': 'Invalid plan_id'}, status=400)
            session = s.checkout.Session.create(
                mode=mode,
                line_items=[{
                    'price_data': {
                        'currency': plan.currency,
                        'product_data': {
                            'name': plan.title,
                            'description': (plan.description or '')[:400]
                        },
                        'unit_amount': int(plan.total_cents),
                    },
                    'quantity': 1,
                }],
                metadata={
                    'plan_id': str(plan.id),
                    'user_id': str(request.user.id),
                    'base_price_cents': str(plan.base_price_cents),
                    'fee_cents': str(plan.fee_cents),
                    'total_cents': str(plan.total_cents),
                },
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=request.user.email or None,
            )
        elif price_id:
            session = s.checkout.Session.create(
                mode=mode,
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=request.user.email or None,
            )
        elif amount:
            session = s.checkout.Session.create(
                mode=mode,
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {'name': 'Custom payment'},
                        'unit_amount': int(amount),
                    },
                    'quantity': 1,
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=request.user.email or None,
            )
        else:
            return JsonResponse({'detail': 'Provide price_id or amount'}, status=400)

        return JsonResponse({'id': session.id, 'url': session.url})
    except stripe.error.StripeError as e:
        body = getattr(e, 'json_body', None) or {}
        err = body.get('error') if isinstance(body, dict) else None
        message = err.get('message') if isinstance(err, dict) else str(e)
        return JsonResponse({'detail': message}, status=400)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create_payment_intent(request):
    try:
        s = init_stripe()
        data = request.data or {}
        amount = data.get('amount')
        currency = data.get('currency', settings.STRIPE_CURRENCY)
        if not amount:
            return JsonResponse({'detail': 'amount required'}, status=400)
        intent = s.PaymentIntent.create(
            amount=int(amount),
            currency=currency,
            metadata={'user_id': str(request.user.id)},
            automatic_payment_methods={'enabled': True},
        )
        return JsonResponse({'client_secret': intent.client_secret})
    except stripe.error.StripeError as e:
        body = getattr(e, 'json_body', None) or {}
        err = body.get('error') if isinstance(body, dict) else None
        message = err.get('message') if isinstance(err, dict) else str(e)
        return JsonResponse({'detail': message}, status=400)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)


@csrf_exempt
def stripe_webhook(request):
    import logging
    logger = logging.getLogger(__name__)
    
    s = init_stripe()
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    # Retrieve secrets from settings (can be a single string or a list/comma-separated string)
    # We support STRIPE_WEBHOOK_SECRET (legacy/single) and STRIPE_WEBHOOK_SECRET_V2
    secrets = []
    if settings.STRIPE_WEBHOOK_SECRET:
        secrets.append(settings.STRIPE_WEBHOOK_SECRET)
    
    # Check for additional secrets in settings if defined (e.g. for v2 events)
    # You can add STRIPE_WEBHOOK_SECRET_V2 to your settings.py and .env
    if hasattr(settings, 'STRIPE_WEBHOOK_SECRET_V2') and settings.STRIPE_WEBHOOK_SECRET_V2:
        secrets.append(settings.STRIPE_WEBHOOK_SECRET_V2)
    
    # If user put comma separated secrets in STRIPE_WEBHOOK_SECRET
    if ',' in settings.STRIPE_WEBHOOK_SECRET:
        secrets = [secret.strip() for secret in settings.STRIPE_WEBHOOK_SECRET.split(',')]

    event = None
    verification_exception = None

    # Try to verify signature with each secret
    for secret in secrets:
        try:
            event = s.Webhook.construct_event(payload, sig_header, secret)
            verification_exception = None
            break # Success
        except Exception as e:
            verification_exception = e
            continue
    
    if event is None:
        logger.error(f"Webhook signature verification failed for all secrets. Last error: {verification_exception}")
        return HttpResponse(status=400)

    # Log the event type for debugging
    logger.info(f"Webhook received event type: {event.get('type')} | Object: {event.get('object')}")

    # Handle Stripe v2 Events (Thin Events)
    if event.get('object') == 'v2.core.event':
        event_type = event.get('type')
        logger.info(f"Received Stripe v2 event: {event_type}")
        # Example: v1.billing.meter.error_report_triggered
        if event_type == 'v1.billing.meter.error_report_triggered':
            related_object = event.get('related_object')
            logger.info(f"Billing meter error: {related_object}")
        return HttpResponse(status=200)

    # Handle Stripe v1 Events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill order: update user plan
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        plan_id = metadata.get('plan_id')
        
        logger.info(f"Webhook checkout.session.completed. User: {user_id}, Plan: {plan_id}")

        if user_id and plan_id:
            from django.contrib.auth import get_user_model
            from .models import Plan
            User = get_user_model()
            try:
                user = User.objects.get(pk=user_id)
                plan = Plan.objects.get(pk=plan_id)
                user.plan = plan
                user.save()
                logger.info(f"Webhook updated plan for user {user.username}")
            except Exception as e:
                logger.error(f"Error updating user plan via webhook: {e}")

    elif event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        # TODO: mark payment as successful

    return HttpResponse(status=200)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def verify_checkout_session(request):
    import logging
    logger = logging.getLogger(__name__)
    
    session_id = request.data.get('session_id')
    if not session_id:
        return Response({'detail': 'session_id required'}, status=400)
    
    s = init_stripe()
    try:
        session = s.checkout.Session.retrieve(session_id)
    except Exception as e:
        logger.error(f"Verify session error: {e}")
        return Response({'detail': str(e)}, status=400)

    if session.payment_status == 'paid':
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        plan_id = metadata.get('plan_id')
        
        # Verify user matches
        if str(user_id) != str(request.user.id):
             logger.warning(f"User mismatch in verify. Session user: {user_id}, Request user: {request.user.id}")
             return Response({'detail': 'User mismatch'}, status=403)

        if plan_id:
            from .models import Plan
            from .serializers import UserSerializer
            try:
                plan = Plan.objects.get(pk=plan_id)
                request.user.plan = plan
                request.user.save()
                logger.info(f"Verify endpoint updated plan for user {request.user.username}")
                return Response(UserSerializer(request.user).data)
            except Plan.DoesNotExist:
                return Response({'detail': 'Plan not found'}, status=404)
    
    return Response({'detail': 'Session not paid or invalid'}, status=400)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def stripe_payment_success(request):
    """
    Callback URL for Stripe Checkout success.
    Updates the user plan synchronously and then redirects to frontend.
    """
    import logging
    import urllib.parse
    logger = logging.getLogger(__name__)
    
    session_id = request.GET.get('session_id')
    target_url = f"{settings.FRONTEND_URL}/profile"
    
    logger.info(f"Stripe payment success callback triggered. Session ID: {session_id}")

    if session_id:
        # Use & if ? exists, else ? (though target_url doesn't have ? yet)
        separator = '&' if '?' in target_url else '?'
        target_url += f"{separator}session_id={session_id}"
        
        try:
            s = init_stripe()
            session = s.checkout.Session.retrieve(session_id)
            logger.info(f"Session retrieved. Status: {session.payment_status}")
            
            if session.payment_status == 'paid':
                metadata = session.get('metadata', {})
                user_id = metadata.get('user_id')
                plan_id = metadata.get('plan_id')
                
                logger.info(f"Metadata - User ID: {user_id}, Plan ID: {plan_id}")

                if user_id and plan_id:
                    from django.contrib.auth import get_user_model
                    from .models import Plan
                    User = get_user_model()
                    try:
                        user = User.objects.get(pk=user_id)
                        plan = Plan.objects.get(pk=plan_id)
                        user.plan = plan
                        user.save()
                        logger.info(f"Successfully updated plan {plan.title} for user {user.username}")
                    except User.DoesNotExist:
                        logger.error(f"User {user_id} not found")
                        target_url += f"&error=UserNotFound"
                    except Plan.DoesNotExist:
                        logger.error(f"Plan {plan_id} not found")
                        target_url += f"&error=PlanNotFound"
                    except Exception as e:
                        logger.error(f"Error updating user plan in callback: {e}")
                        target_url += f"&error=UpdateFailed:{urllib.parse.quote(str(e))}"
                else:
                    logger.warning("Missing user_id or plan_id in session metadata")
                    target_url += "&error=MissingMetadata"
            else:
                logger.warning(f"Session not paid. Status: {session.payment_status}")
                target_url += f"&error=NotPaid:{session.payment_status}"
        except Exception as e:
            logger.error(f"Error retrieving session in callback: {e}")
            target_url += f"&error=SessionRetrieveFailed:{urllib.parse.quote(str(e))}"

    return redirect(target_url)
