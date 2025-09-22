from rest_framework import routers
from .views import (
    RegisterView,
    MeView,
    tasks_page,
    trademark_classification_search,
    trademark_name_search,
    trademark_availability,
    trademark_logo_search,
    trademark_serial_search,
    trademark_registration_search,
    trademark_owners_search,
    trademark_status_search,
    trademark_transaction_search,
    trademark_filing_search,
    trademark_event_search,
)
from .stripe_views import stripe_config, create_checkout_session, create_payment_intent, stripe_webhook
from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(router.urls)),
    # DRF browsable API login/logout under /api/auth/
    path('auth/', include('rest_framework.urls')),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    # JWT token endpoints moved from root
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', tasks_page, name='tasks-page'),
    # Trademark lookup endpoints
    path('trademark/classification-search/', trademark_classification_search, name='trademark-classification-search'),
    path('trademark/name-search/', trademark_name_search, name='trademark-name-search'),
    path('trademark/availability/', trademark_availability, name='trademark-availability'),
    path('trademark/logo-search/', trademark_logo_search, name='trademark-logo-search'),
    path('trademark/serial-search/', trademark_serial_search, name='trademark-serial-search'),
    path('trademark/registration-search/', trademark_registration_search, name='trademark-registration-search'),
    path('trademark/owners-search/', trademark_owners_search, name='trademark-owners-search'),
    path('trademark/status-search/', trademark_status_search, name='trademark-status-search'),
    path('trademark/transaction/', trademark_transaction_search, name='trademark-transaction-search'),
    path('trademark/filing-search/', trademark_filing_search, name='trademark-filing-search'),
    path('trademark/event-search/', trademark_event_search, name='trademark-event-search'),
    # Stripe endpoints
    path('stripe/config/', stripe_config, name='stripe-config'),
    path('stripe/create-checkout-session/', create_checkout_session, name='stripe-create-checkout-session'),
    path('stripe/create-payment-intent/', create_payment_intent, name='stripe-create-payment-intent'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    # No-trailing-slash aliases to avoid POST -> GET redirect via APPEND_SLASH
    path('stripe/create-checkout-session', create_checkout_session, name='stripe-create-checkout-session-noslash'),
    path('stripe/create-payment-intent', create_payment_intent, name='stripe-create-payment-intent-noslash'),
    # Template pages for checkout flow
    path('checkout/', TemplateView.as_view(template_name='payments/checkout.html'), name='checkout-page'),
    path('payments/success', TemplateView.as_view(template_name='payments/success.html'), name='payment-success'),
    path('payments/cancel', TemplateView.as_view(template_name='payments/cancel.html'), name='payment-cancel'),
]