from rest_framework import serializers, permissions, generics
from django.contrib.auth import get_user_model
from .models import  Trademark, TrademarkAsset, Plan, Testimonial, BlogPost


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'phone_number'
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class TrademarkAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrademarkAsset
        fields = ('id', 'kind', 'text_value', 'logo', 'sound', 'created_at')


class TrademarkSerializer(serializers.ModelSerializer):
    assets = TrademarkAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Trademark
        fields = ('id', 'user', 'assets', 'created_at', 'updated_at')


class PlanSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = (
            'id', 'title', 'description', 'client_objective', 'includes',
            'price_cents', 'base_price_cents', 'fee_cents', 'currency',
            'price', 'total', 'is_active'
        )

    def get_price(self, obj):
        cents = obj.price_cents if obj.price_cents is not None else (obj.base_price_cents or 0)
        return {
            'amount': cents / 100.0,
            'currency': obj.currency,
        }

    def get_total(self, obj):
        return {
            'amount': obj.total_cents / 100.0,
            'currency': obj.currency,
        }


class TestimonialSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    trademark = serializers.PrimaryKeyRelatedField(queryset=Trademark.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Testimonial
        fields = (
            'id', 'user', 'trademark', 'client_name', 'brand_name', 'title', 'content', 'rating', 'approved', 'created_at'
        )
        read_only_fields = ('approved', 'created_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        validated_data['user'] = user
        # Auto-fill client/brand when missing
        if not validated_data.get('client_name') and user:
            validated_data['client_name'] = (user.get_full_name() or user.username or '').strip()
        tm = validated_data.get('trademark')
        if not validated_data.get('brand_name') and tm:
            # If you later store brand name in assets, adapt here
            validated_data['brand_name'] = getattr(user, 'username', '')
        return super().create(validated_data)


class TestimonialSimpleSerializer(serializers.ModelSerializer):
    """Public/simple representation to match frontend shape.
    Shape:
      {
        id: number,
        name: string,       # maps from brand_name or client_name or user name
        quote: string,      # maps from content
        logo: string|null,  # placeholder until model adds a field
        country: string|null
      }
    """

    name = serializers.SerializerMethodField()
    quote = serializers.CharField(source='content')
    logo = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ('id', 'name', 'quote', 'logo', 'country')

    def get_name(self, obj):
        # Prefer brand_name, then client_name, then user display
        if getattr(obj, 'brand_name', None):
            return obj.brand_name
        if getattr(obj, 'client_name', None):
            return obj.client_name
        user = getattr(obj, 'user', None)
        if user:
            return getattr(user, 'full_name', '') or getattr(user, 'username', '') or str(user)
        return ''

    def get_logo(self, obj):
        # No dedicated field yet; return None for now or derive from future assets
        return None

    def get_country(self, obj):
        # Country not stored yet; return None to keep shape stable
        return None


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'id', 'author', 'title', 'slug', 'body', 'is_published', 'created_at', 'updated_at'
        )
        read_only_fields = ('slug', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        validated_data['author'] = user
        return super().create(validated_data)