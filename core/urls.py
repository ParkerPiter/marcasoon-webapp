from rest_framework import routers
from .views import (
    RegisterView,
    MeView,
    auth_login_json,
    auth_logout_json,
    tasks_page,
    plans_list,
    plan_detail,
    testimonials_list_public,
    testimonials_collection,
    testimonial_detail,
    blog_posts,
    blog_post_detail,
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
from .paypal_views import create_paypal_order, capture_paypal_order, paypal_success, paypal_cancel, paypal_return
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(router.urls)),
    
    # JSON auth endpoints (override DRF's HTML login/logout)
    path('auth/login/', auth_login_json, name='auth-login-json'),
    path('auth/logout/', auth_logout_json, name='auth-logout-json'),

    # DRF browsable API login/logout under /api/auth/
    path('auth/', include('rest_framework.urls')),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    
    # JWT token endpoints moved from root
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', tasks_page, name='tasks-page'),
    
    # Plans endpoints
    path('plans/', plans_list, name='plans-list'),
    path('plans/<int:pk>/', plan_detail, name='plan-detail'),
    # No-trailing-slash aliases to avoid 301 redirects on preflight
    path('plans', plans_list, name='plans-list-noslash'),
    path('plans/<int:pk>', plan_detail, name='plan-detail-noslash'),
  
    # Testimonials endpoints
    path('testimonials/public/', testimonials_list_public, name='testimonials-public'),
    path('testimonials/', testimonials_collection, name='testimonials-collection'),
    path('testimonials/<int:pk>/', testimonial_detail, name='testimonial-detail'),
    path('plans/test/', TemplateView.as_view(template_name='plans/test.html'), name='plans-test'),

    # Blog / Foro endpoints
    path('blog/posts/', blog_posts, name='blog-posts'),
    path('blog/posts/<int:pk>/', blog_post_detail, name='blog-post-detail'),
    
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
    
    # Paypal endpoints
    path('paypal/create-order/', create_paypal_order, name='paypal-create-order'),
    path('paypal/capture-order/', capture_paypal_order, name='paypal-capture-order'),
    path('paypal/return/', paypal_return, name='paypal-return'),
    path('payments/success', paypal_success, name='paypal-success'),
    path('payments/cancel', paypal_cancel, name='paypal-cancel'),
    
    # No-trailing-slash aliases to avoid POST -> GET redirect via APPEND_SLASH
    path('stripe/create-checkout-session', create_checkout_session, name='stripe-create-checkout-session-noslash'),
    path('stripe/create-payment-intent', create_payment_intent, name='stripe-create-payment-intent-noslash'),
    
    # Template pages for checkout flow
    path('checkout/', TemplateView.as_view(template_name='payments/checkout.html'), name='checkout-page'),
    path('paypal/checkout/', lambda request: render(request, 'payments/paypal_checkout.html', { 'paypal_client_id': settings.PAYPAL_CLIENT_ID }), name='paypal-checkout-page'),
    path('payments/success', TemplateView.as_view(template_name='payments/success.html'), name='payment-success'),
    path('payments/cancel', TemplateView.as_view(template_name='payments/cancel.html'), name='payment-cancel'),
]