# core/paypal_views.py
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from .paypal_service import get_paypal_client
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create_paypal_order(request):
    try:
        client = get_paypal_client()
        data = request.data or {}
        plan_id = data.get('plan_id')
        amount = data.get('amount')
        currency = data.get('currency', 'USD')
        redirect_mode = bool(data.get('redirect'))
        if plan_id:
            from .models import Plan
            try:
                plan = Plan.objects.get(pk=plan_id, is_active=True)
            except Plan.DoesNotExist:
                return JsonResponse({'detail': 'Invalid plan_id'}, status=400)
            amount = plan.total_cents / 100.0
            currency = plan.currency
            purchase_desc = f"{plan.title} (Base: {plan.base_price_cents/100:.2f} + Fee: {plan.fee_cents/100:.2f})"
        else:
            purchase_desc = 'Custom payment'
            if amount is None:
                return JsonResponse({'detail': 'Amount is required'}, status=400)
        # Normaliza a 2 decimales por requisitos de PayPal
        try:
            amount_value = f"{float(amount):.2f}"
        except Exception:
            return JsonResponse({'detail': 'Amount must be a number'}, status=400)

        req = OrdersCreateRequest()
        req.prefer('return=representation')
        body = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": currency,
                    "value": amount_value
                },
                "description": purchase_desc,
                "custom_id": str(plan_id) if plan_id else None
            }]
        }
        if redirect_mode:
            scheme = 'https' if request.is_secure() else 'http'
            base = f"{scheme}://{request.get_host()}"
            body["application_context"] = {
                "return_url": f"{base}/api/paypal/return/",
                "cancel_url": f"{base}/api/payments/cancel",
                "user_action": "PAY_NOW"
            }
        req.request_body(body)
        resp = client.execute(req)
        approve_url = None
        try:
            links = getattr(resp.result, 'links', []) or []
            for l in links:
                if getattr(l, 'rel', '') == 'approve':
                    approve_url = getattr(l, 'href', None)
                    break
        except Exception:
            approve_url = None
        return JsonResponse({"orderID": resp.result.id, "approveUrl": approve_url})
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def capture_paypal_order(request):
    try:
        client = get_paypal_client()
        data = request.data or {}
        order_id = data.get('orderID')
        if not order_id:
            return JsonResponse({'detail': 'orderID is required'}, status=400)
        req = OrdersCaptureRequest(order_id)
        resp = client.execute(req)
        
        status = getattr(resp.result, 'status', 'UNKNOWN')
        
        # Update user plan if payment is completed
        if status == 'COMPLETED':
            plan_id = data.get('plan_id')
            # If not provided in request, try to get from PayPal order custom_id
            if not plan_id:
                try:
                    units = getattr(resp.result, 'purchase_units', [])
                    if units:
                        plan_id = getattr(units[0], 'custom_id', None)
                except Exception:
                    pass
            
            if plan_id:
                from .models import Plan
                try:
                    plan = Plan.objects.get(pk=plan_id)
                    request.user.plan = plan
                    request.user.save()
                    
                    # Send invoice email
                    try:
                        amount_cents = 0
                        currency = 'USD'
                        units = getattr(resp.result, 'purchase_units', [])
                        if units:
                            amount_obj = getattr(units[0], 'amount', None)
                            if amount_obj:
                                val_str = getattr(amount_obj, 'value', '0')
                                amount_cents = int(float(val_str) * 100)
                                currency = getattr(amount_obj, 'currency_code', 'USD')
                        
                        from .utils import send_invoice_email
                        send_invoice_email(request.user, plan, amount_cents, currency, 'PayPal')
                    except Exception as e_mail:
                        # Logging could be added here
                        print(f"Error sending invoice email: {e_mail}")

                except Exception:
                    pass

        return JsonResponse({
            'status': status,
            'id': getattr(resp.result, 'id', order_id)
        })
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def paypal_return(request):
    """Handle PayPal redirect return (same-window flow): capture and redirect to success/cancel."""
    try:
        token = request.GET.get('token') or request.GET.get('orderID')
        if not token:
            return HttpResponseRedirect('/api/payments/cancel')
        client = get_paypal_client()
        req = OrdersCaptureRequest(token)
        client.execute(req)
        # Redirect to frontend profile
        return HttpResponseRedirect(f"{settings.FRONTEND_URL}/profile?orderID={token}")
    except Exception:
        return HttpResponseRedirect('/api/payments/cancel')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def paypal_success(request):
    return JsonResponse({'status': 'success'})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def paypal_cancel(request):
    return JsonResponse({'status': 'cancelled'})