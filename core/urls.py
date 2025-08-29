from rest_framework import routers
from .views import TestViewSet, TaskView, RegisterView, MeView, tasks_page
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'TestModel', TestViewSet)
router.register(r'Task', TaskView, basename='task')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('tasks/', tasks_page, name='tasks-page'),
]