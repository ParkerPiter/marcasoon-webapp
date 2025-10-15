import paypalrestsdk
from django.conf import settings
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

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
        env = SandboxEnvironment(
            client_id=settings.PAYPAL_CLIENT_ID,
            client_secret=settings.PAYPAL_CLIENT_SECRET
        )
        _CLIENT_CACHE = PayPalHttpClient(env)
    return _CLIENT_CACHE