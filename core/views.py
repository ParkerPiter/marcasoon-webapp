from django.shortcuts import render
from django.conf import settings
import requests
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import Trademark, TrademarkAsset, User, Plan, Testimonial, BlogPost
from .serializers import RegisterSerializer, UserSerializer, PlanSerializer, TestimonialSerializer, TestimonialSimpleSerializer, BlogPostSerializer
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


# JSON login/logout endpoints (no HTML templates)
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def auth_login_json(request):
    data = request.data or {}
    username = data.get('username') or data.get('email')
    password = data.get('password')
    if not username or not password:
        return Response({'detail': 'username and password are required'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'detail': 'Invalid credentials'}, status=401)
    login(request, user)
    return Response({'detail': 'ok', 'user': UserSerializer(user).data})


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def auth_logout_json(request):
    if request.user.is_authenticated:
        logout(request)
    return Response({'detail': 'ok'})


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
    # If the client requests HTML (e.g., direct browser navigation), render the demo page
    accept = request.META.get('HTTP_ACCEPT', '') or ''
    if 'text/html' in accept:
        # Template uses fetch('/api/plans/') to load JSON and buttons to hit Stripe/PayPal endpoints
        return render(request, 'plans/test.html', {
            'paypal_client_id': getattr(settings, 'PAYPAL_CLIENT_ID', ''),
            'stripe_public_key': getattr(settings, 'STRIPE_PUBLIC_KEY', ''),
        })
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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def testimonials_list_public(request):
    qs = Testimonial.objects.filter(approved=True).order_by('-created_at')
    return Response(TestimonialSimpleSerializer(qs, many=True, context={'request': request}).data)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def testimonials_collection(request):
    if request.method == 'GET':
        qs = Testimonial.objects.filter(user=request.user).order_by('-created_at')
        return Response(TestimonialSimpleSerializer(qs, many=True, context={'request': request}).data)
    # POST create
    data = request.data.copy()
    # Accept new shape: name -> brand_name, quote -> content
    if 'name' in data and 'brand_name' not in data:
        data['brand_name'] = data.get('name')
    if 'quote' in data and 'content' not in data:
        data['content'] = data.get('quote')
    serializer = TestimonialSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        obj = serializer.save()
        return Response(TestimonialSimpleSerializer(obj, context={'request': request}).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def testimonial_detail(request, pk: int):
    try:
        obj = Testimonial.objects.get(pk=pk)
    except Testimonial.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)
    # Owner or staff can edit/delete; public get is restricted to owner unless approved
    if request.method == 'GET':
        if obj.approved or obj.user_id == request.user.id or request.user.is_staff:
            return Response(TestimonialSimpleSerializer(obj, context={'request': request}).data)
        return Response({'detail': 'Forbidden'}, status=403)
    if obj.user_id != request.user.id and not request.user.is_staff:
        return Response({'detail': 'Forbidden'}, status=403)
    if request.method == 'PATCH':
        data = request.data.copy()
        if 'name' in data:
            data['brand_name'] = data.pop('name') or data.get('brand_name')
        if 'quote' in data:
            data['content'] = data.pop('quote') or data.get('content')
        serializer = TestimonialSerializer(obj, data=data, partial=True, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            return Response(TestimonialSimpleSerializer(obj, context={'request': request}).data)
        return Response(serializer.errors, status=400)
    obj.delete()
    return Response(status=204)


# Blog / Foro
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def blog_posts(request):
    """Lista pública de posts publicados. Crear requiere autenticación."""
    if request.method == 'GET':
        qs = BlogPost.objects.filter(is_published=True).order_by('-created_at')
        return Response(BlogPostSerializer(qs, many=True, context={'request': request}).data)
    # POST create (auth required)
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=401)
    serializer = BlogPostSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        obj = serializer.save()
        return Response(BlogPostSerializer(obj, context={'request': request}).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.AllowAny])
def blog_post_detail(request, pk: int):
    try:
        obj = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)

    if request.method == 'GET':
        # Permitir ver borradores solo al autor o staff
        if obj.is_published or (request.user.is_authenticated and (request.user.is_staff or request.user.id == obj.author_id)):
            return Response(BlogPostSerializer(obj, context={'request': request}).data)
        return Response({'detail': 'Forbidden'}, status=403)

    # PATCH/DELETE requieren autenticación y ser autor (o staff)
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication required'}, status=401)
    if request.user.id != obj.author_id and not request.user.is_staff:
        return Response({'detail': 'Forbidden'}, status=403)

    if request.method == 'PATCH':
        serializer = BlogPostSerializer(obj, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            return Response(BlogPostSerializer(obj, context={'request': request}).data)
        return Response(serializer.errors, status=400)

    obj.delete()
    return Response(status=204)
    