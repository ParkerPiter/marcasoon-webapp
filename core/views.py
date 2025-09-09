from django.shortcuts import render
import requests
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import TestModel, Task
from .serializers import TestSerializer, TaskSerializer, RegisterSerializer, UserSerializer
from .trademark_service import TrademarkLookupClient

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
def trademark_classification_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.classification_search(name, page=page, page_size=page_size)
        return Response(data)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_name_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    count = int(request.query_params.get('count', 10))
    client = TrademarkLookupClient()
    try:
        data = client.name_search(name, page=page, count=count)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))
    