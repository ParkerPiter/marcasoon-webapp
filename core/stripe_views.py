from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .stripe_service import init_stripe
import stripe


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def stripe_config(request):
    return JsonResponse({
        'publicKey': settings.STRIPE_PUBLIC_KEY,
        'currency': settings.STRIPE_CURRENCY,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_checkout_session(request):
    try:
        s = init_stripe()
        data = request.data or {}
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
            # Default: usar las páginas del backend en lugar de FRONTEND_URL
            backend_success = '/api/payments/success'
            success_url = request.build_absolute_uri(backend_success) + '?session_id={CHECKOUT_SESSION_ID}'

        if cancel_path:
            if cancel_path.startswith('http://') or cancel_path.startswith('https://'):
                cancel_url = cancel_path
            else:
                cancel_url = request.build_absolute_uri(cancel_path)
        else:
            backend_cancel = '/api/payments/cancel'
            cancel_url = request.build_absolute_uri(backend_cancel)

        if price_id:
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
    s = init_stripe()
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = s.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # TODO: fulfill order, mark payment success
    elif event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        # TODO: mark payment as successful

    return HttpResponse(status=200)
