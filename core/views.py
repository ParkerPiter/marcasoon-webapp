from django.shortcuts import render
from django.conf import settings
import requests
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import get_user_model
from .models import Trademark, TrademarkAsset, User, Plan, Testimonial, BlogPost
from .serializers import RegisterSerializer, UserSerializer, PlanSerializer, TestimonialSerializer, TestimonialSimpleSerializer, BlogPostSerializer
from .serializers import ContactSerializer
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .trademark_service import TrademarkLookupClient
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging
import json
import random
from datetime import timedelta
from django.utils import timezone
from .serializers import TrademarkSerializer
from .serializers import TrademarkAssetSerializer
from .serializers import TrademarkIntakeSerializer
from django.http import HttpResponse
from urllib.parse import urlparse



User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    # Allow multipart/form-data so registration can include file uploads
    parser_classes = (MultiPartParser, FormParser, JSONParser)


from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class MeView(generics.RetrieveUpdateAPIView):
    """Return or update the current authenticated user's profile.

    GET /api/auth/me/    -> returns current user
    PATCH /api/auth/me/  -> partial update current user
    PUT  /api/auth/me/   -> full update
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

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
    # Emitir JWT (access + refresh). No es necesario crear sesión.
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    return Response({
        'detail': 'ok',
        'user': UserSerializer(user).data,
        'access': access,
        'refresh': str(refresh),
        'token_type': 'Bearer'
    })


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
@authentication_classes([JWTAuthentication])
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
    # Include uploaded image file if present (request.data.copy() loses files)
    if hasattr(request, 'FILES') and 'image' in request.FILES:
        data['image'] = request.FILES['image']
    serializer = TestimonialSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        obj = serializer.save()
        return Response(TestimonialSimpleSerializer(obj, context={'request': request}).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
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
        if hasattr(request, 'FILES') and 'image' in request.FILES:
            data['image'] = request.FILES['image']
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


# Simple JWT-protected ping to verify Authorization header end-to-end
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def auth_ping(request):
    return Response({'detail': 'ok', 'user': UserSerializer(request.user).data})


# --- Trademark endpoints (create, retrieve) and evidence upload ---
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create_trademark(request):
    data = request.data.copy()
    # Bind to current user in serializer context
    serializer = TrademarkSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        tm = serializer.save()
        return Response(TrademarkSerializer(tm, context={'request': request}).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def trademark_detail(request, pk: int):
    try:
        obj = Trademark.objects.get(pk=pk)
    except Trademark.DoesNotExist:
        return Response({'detail': 'Not found'}, status=404)
    # Only owner or staff can view
    if obj.user_id != request.user.id and not request.user.is_staff:
        return Response({'detail': 'Forbidden'}, status=403)
    return Response(TrademarkSerializer(obj, context={'request': request}).data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def trademark_evidence_upload(request, pk: int):
    try:
        tm = Trademark.objects.get(pk=pk)
    except Trademark.DoesNotExist:
        return Response({'detail': 'Trademark not found'}, status=404)
    # Only owner or staff can upload
    if tm.user_id != request.user.id and not request.user.is_staff:
        return Response({'detail': 'Forbidden'}, status=403)
    # Lazy import to avoid circulars
    from .serializers import TrademarkEvidenceSerializer
    data = request.data.copy()
    # Accept file upload in 'file' field
    if hasattr(request, 'FILES') and 'file' in request.FILES:
        data['file'] = request.FILES['file']
    serializer = TrademarkEvidenceSerializer(data=data, context={'request': request, 'trademark': tm})
    if serializer.is_valid():
        ev = serializer.save()
        return Response(TrademarkEvidenceSerializer(ev, context={'request': request}).data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def contact(request):
    """Render contact form (GET) and send email (POST).

    Fields: full_name, email, phone, message
    """
    if request.method == 'GET':
        return render(request, 'contact.html')

    # POST: parse either JSON or form-encoded
    full_name = email = phone = message = ''
    content_type = (request.META.get('CONTENT_TYPE') or '').lower()
    try:
        if 'application/json' in content_type:
            payload = json.loads(request.body or b"{}")
            full_name = (payload.get('full_name') or '').strip()
            email = (payload.get('email') or '').strip()
            phone = (payload.get('phone') or '').strip()
            message = (payload.get('message') or '').strip()
        else:
            full_name = (request.POST.get('full_name') or '').strip()
            email = (request.POST.get('email') or '').strip()
            phone = (request.POST.get('phone') or '').strip()
            message = (request.POST.get('message') or '').strip()
    except Exception:
        # fall back to empty values; will trigger validation errors
        pass

    errors = {}
    if not full_name:
        errors['full_name'] = 'Required'
    if not email:
        errors['email'] = 'Required'
    if not message:
        errors['message'] = 'Required'
    if errors:
        return render(request, 'contact.html', {'errors': errors, 'full_name': full_name, 'email': email, 'phone': phone, 'message': message})

    # Build email content
    subject = f'Contacto desde sitio: {full_name}'
    html_message = render_to_string('emails/contact_email.html', {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'message': message,
        'site': request.get_host(),
    })
    plain_message = strip_tags(html_message)

    # Fixed recipient as requested; fallback to settings if you later want to change centrally
    recipient = 'marcasoon@gmail.com'
    from_email = getattr(settings, 'EMAIL_HOST_USER', None) or settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(subject, plain_message, from_email, [recipient], html_message=html_message, fail_silently=False)
    except Exception as exc:
        logger = logging.getLogger(__name__)
        logger.exception('Failed sending contact email')
        # Show a friendly error to the user instead of raising 500
        error_msg = 'Ocurrió un error al enviar el mensaje. Por favor inténtalo de nuevo más tarde.'
        return render(request, 'contact.html', {'errors': {'send': error_msg}, 'full_name': full_name, 'email': email, 'phone': phone, 'message': message})

    return render(request, 'contact_success.html', {'full_name': full_name})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def contact_api(request):
    """JSON API endpoint for contact submissions.

    Accepts JSON: { full_name, email, phone?, message }
    Returns JSON: { detail: 'ok' } on success or serializer errors.
    """
    serializer = ContactSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    data = serializer.validated_data
    subject = f'Contacto desde sitio: {data.get("full_name")}'
    html_message = render_to_string('emails/contact_email.html', {**data, 'site': request.get_host()})
    plain_message = strip_tags(html_message)
    recipient = 'marcasoon@gmail.com'
    from_email = getattr(settings, 'EMAIL_HOST_USER', None) or settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, plain_message, from_email, [recipient], html_message=html_message, fail_silently=False)
    except Exception:
        logger = logging.getLogger(__name__)
        logger.exception('Failed sending contact email via API')
        return Response({'detail': 'Failed to send email'}, status=500)
    return Response({'detail': 'ok'}, status=201)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    """Start password reset: accept email, generate code, email it.
    Always respond 200 to avoid email enumeration; but include detail for success path.
    """
    ser = PasswordResetRequestSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=400)
    email = ser.validated_data['email']
    # Try to find the user; don't reveal whether it exists
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        # Still respond 200 to prevent enumeration
        return Response({'detail': 'ok'}, status=200)
    # Generate 6-digit code
    code = f"{random.randint(0, 999999):06d}"
    from .models import PasswordResetCode
    expires_at = timezone.now() + timedelta(minutes=15)
    PasswordResetCode.objects.create(user=user, code=code, expires_at=expires_at)
    # Send email
    html_message = render_to_string('emails/password_reset_code.html', {
        'user': user,
        'code': code,
        'minutes': 15,
        'site': request.get_host(),
    })
    plain_message = strip_tags(html_message)
    subject = 'Código de recuperación de contraseña'
    from_email = getattr(settings, 'EMAIL_HOST_USER', None) or settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, plain_message, from_email, [email], html_message=html_message, fail_silently=False)
    except Exception:
        logger = logging.getLogger(__name__)
        logger.exception('Failed sending password reset code email')
        # Do not reveal failure details to client
    return Response({'detail': 'ok'}, status=200)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request):
    """Confirm reset: verify email+code then set new password."""
    ser = PasswordResetConfirmSerializer(data=request.data)
    if not ser.is_valid():
        return Response(ser.errors, status=400)
    email = ser.validated_data['email']
    code = ser.validated_data['code']
    new_password = ser.validated_data['new_password']
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid code or email'}, status=400)
    from .models import PasswordResetCode
    prc = PasswordResetCode.objects.filter(user=user, code=code, used=False).order_by('-created_at').first()
    if not prc or not prc.is_valid():
        return Response({'detail': 'Invalid or expired code'}, status=400)
    # Update password and mark code used
    user.set_password(new_password)
    user.save()
    prc.used = True
    prc.save(update_fields=['used'])
    return Response({'detail': 'ok'}, status=200)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def webinar_live_embed(request):
    """Public JSON endpoint exposing the configured live webinar embed URL.

    Returns JSON: { "embed_url": "https://..." }
    In DEBUG, allows override via ?url=... for quick testing.
    """
    embed_url = getattr(settings, 'WEBINAR_EMBED_URL', '') or ''
    if settings.DEBUG:
        override = (request.GET.get('url') or '').strip()
        if override:
            embed_url = override
    if not embed_url:
        return Response({'detail': 'Webinar no configurado', 'embed_url': ''}, status=503)
    parsed = urlparse(embed_url)
    if parsed.scheme not in ('http', 'https'):
        return Response({'detail': 'URL inválida', 'embed_url': embed_url}, status=400)
    return Response({'embed_url': embed_url})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def trademark_intake(request):
    """Combined endpoint to read/update the full trademark intake in one call.

    - GET: returns current values for user + trademark + last logo asset
    - POST: accepts JSON or multipart to update fields and optional files
    """
    if request.method == 'GET':
        # Ensure we have a trademark placeholder
        from .models import Trademark, TrademarkAsset
        tm, _ = Trademark.objects.get_or_create(user=request.user)
        asset = TrademarkAsset.objects.filter(trademark=tm, kind=TrademarkAsset.Kind.LOGO).order_by('-id').first()
        data = {
            'user': UserSerializer(request.user, context={'request': request}).data,
            'trademark': TrademarkSerializer(tm, context={'request': request}).data,
        }
        if asset:
            data['asset'] = TrademarkAssetSerializer(asset, context={'request': request}).data
        return Response(data)

    # POST update
    # Normalize multipart edge cases (evidence_links sent as JSON string or comma list)
    incoming = request.data.copy()
    try:
        links_val = incoming.get('evidence_links')
        if isinstance(links_val, str):
            import json as _json
            parsed = None
            try:
                parsed = _json.loads(links_val)
            except Exception:
                # allow comma-separated
                parsed = [s.strip() for s in links_val.split(',') if s.strip()]
            incoming['evidence_links'] = parsed
    except Exception:
        pass

    ser = TrademarkIntakeSerializer(data=incoming, context={'request': request})
    if not ser.is_valid():
        return Response(ser.errors, status=400)
    payload = ser.save(user=request.user)
    return Response(payload, status=200)
    