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
def uspto_case_status(request, case_id: str | None = None):
    # Only HTML mode using case_id
    if not case_id:
        case_id = request.query_params.get('case_id')
    if not case_id:
        return Response({'detail': 'Provide case_id in the URL path (/uspto/casestatus/<case_id>/) or as ?case_id='}, status=400)
    client = USPTOClient()
    try:
        data = client.tsdr_case_status(case_id=case_id)
    except requests.HTTPError as e:
        resp = e.response
        snippet = resp.text[:2000] if resp is not None and resp.text else ''
        return Response({
            'upstream_status': getattr(resp, 'status_code', 502),
            'detail': 'USPTO request failed',
            'body': snippet,
            'url': getattr(resp, 'url', None),
        }, status=getattr(resp, 'status_code', 502))
    # Returns HTML text -> wrap for JSON transport
    if isinstance(data, str):
        return Response({'content_type': 'text/html', 'text': data})
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def uspto_case_status_json(request):
    serial = request.query_params.get('serial')
    reg = request.query_params.get('registration')
    if not serial and not reg:
        return Response({'detail': 'Provide serial or registration'}, status=400)
    client = USPTOClient()
    try:
        data = client.tsdr_case_status_json(serial_number=serial, registration_number=reg)
    except ValueError as e:
        return Response({'detail': str(e)}, status=400)
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def uspto_search(request):
    q = request.query_params.get('q')
    if not q:
        return Response({'detail': 'Missing q'}, status=400)
    client = USPTOClient()
    # Pasar filtros adicionales como están (ej.: class, status, owner, etc.)
    extra = {k: v for k, v in request.query_params.items() if k != 'q'}
    data = client.trademark_search(q, **extra)
    return Response(data)
    