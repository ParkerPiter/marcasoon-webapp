from rest_framework import serializers, permissions, generics
from django.contrib.auth import get_user_model
from .models import  Trademark, TrademarkAsset, Plan, Testimonial


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