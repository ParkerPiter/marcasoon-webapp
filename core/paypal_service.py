import paypalrestsdk
from django.conf import settings
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment

_CLIENT_CACHE = None

def init_paypal():
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })
    return paypalrestsdk

def get_paypal_client():
    global _CLIENT_CACHE
    if _CLIENT_CACHE is None:
        client_id = (settings.PAYPAL_CLIENT_ID or '').strip()
        client_secret = (settings.PAYPAL_CLIENT_SECRET or '').strip()
        if not client_id or not client_secret:
            raise RuntimeError('PayPal credentials are not configured. Check PAYPAL_CLIENT_ID/SECRET env vars.')
        mode = (getattr(settings, 'PAYPAL_MODE', 'sandbox') or 'sandbox').lower()
        if mode == 'live':
            env = LiveEnvironment(client_id=client_id, client_secret=client_secret)
        else:
            env = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
        _CLIENT_CACHE = PayPalHttpClient(env)
    return _CLIENT_CACHE