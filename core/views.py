from django.shortcuts import render
import requests
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import Trademark, TrademarkAsset, User, Plan
from .serializers import RegisterSerializer, UserSerializer, PlanSerializer
from .trademark_service import TrademarkLookupClient



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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_logo_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.logo_search(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_serial_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.serial_search(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_registration_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.registration_search(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_owners_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.owners_search(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_status_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.status_search(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_transaction_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.transaction(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_filing_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.filing_search(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_event_search(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    client = TrademarkLookupClient()
    try:
        data = client.event_search(name, page=page, page_size=page_size)
        return Response(data)
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trademark_availability(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Missing name'}, status=400)
    client = TrademarkLookupClient()
    try:
        text = client.availability(name)
        # Normalize to requested response. If the API returns exactly the text
        # `failed:"google is Not Available to Register"` we pass-as is.
        # Wrap into a simple JSON with a `result` field for frontend simplicity.
        return Response({'result': text})
    except ValueError as ve:
        return Response({'detail': str(ve)}, status=400)
    except requests.HTTPError as e:
        resp = e.response
        return Response({'detail': 'Upstream error', 'status': getattr(resp, 'status_code', 502), 'url': getattr(resp, 'url', None), 'body': getattr(resp, 'text', '')[:500]}, status=getattr(resp, 'status_code', 502))


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def plans_list(request):
    qs = Plan.objects.filter(is_active=True).order_by('price_cents')
    return Response(PlanSerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def plan_detail(request, pk: int):
    try:
        plan = Plan.objects.get(pk=pk, is_active=True)
    except Plan.DoesNotExist:
        return Response({'detail': 'Plan not found'}, status=404)
    return Response(PlanSerializer(plan).data)
    