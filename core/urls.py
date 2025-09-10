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
from django.urls import path, include


router = routers.DefaultRouter()


urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
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
]