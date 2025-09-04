from django.shortcuts import render
import requests
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import TestModel, Task
from .serializers import TestSerializer, TaskSerializer, RegisterSerializer, UserSerializer
from .uspto_service import USPTOClient

class TestViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer
    
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


def tasks_page(request):
    """Renderiza una página simple que consume la API de tareas via fetch."""
    return render(request, 'core/tasks.html')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def uspto_last_update(request):
    sn = request.query_params.get('sn')
    if not sn:
        return Response({'detail': 'Missing sn'}, status=400)
    client = USPTOClient()
    try:
        data = client.last_update_info(sn)
        return Response(data)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'body': getattr(resp, 'text', '')[:1000], 'url': getattr(resp, 'url', None)}, status=getattr(resp, 'status_code', 502))
    