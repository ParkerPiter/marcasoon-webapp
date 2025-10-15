import stripe
from django.conf import settings


def init_stripe():
    if not settings.STRIPE_SECRET_KEY:
        raise RuntimeError('STRIPE_SECRET_KEY not configured')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe
