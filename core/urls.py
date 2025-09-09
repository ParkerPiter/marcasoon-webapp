from rest_framework import routers
from .views import TestViewSet, TaskView, RegisterView, MeView, tasks_page, trademark_classification_search, trademark_name_search, trademark_availability, trademark_logo_search
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'TestModel', TestViewSet)
router.register(r'Task', TaskView, basename='task')

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
]