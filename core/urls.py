from rest_framework import routers
from .views import TestViewSet, TaskView, RegisterView, MeView, tasks_page, uspto_case_status, uspto_case_status_json, uspto_search
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'TestModel', TestViewSet)
router.register(r'Task', TaskView, basename='task')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('tasks/', tasks_page, name='tasks-page'),
    # Case status: HTML only with case_id in path
    path('uspto/casestatus/<str:case_id>/', uspto_case_status, name='uspto-case-status-by-id'),
    path('uspto/casestatus/<str:case_id>', uspto_case_status),
    path('uspto/casestatus-json/', uspto_case_status_json, name='uspto-case-status-json'),
    path('uspto/search/', uspto_search, name='uspto-search'),
    path('uspto/case-multi-status/', uspto_search, name='uspto-case-multi-status'),
]