from rest_framework import serializers, permissions, generics
from django.contrib.auth import get_user_model
from .models import  Trademark, TrademarkAsset, Plan, Testimonial, BlogPost
from .models import PasswordResetCode


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Allow updating password via this serializer (write-only)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=8)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'phone_number', 'password', 'profile_image'
        )

    def update(self, instance, validated_data):
        # Handle password correctly
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# Expose more user/profile fields for registration and profile edit
UserSerializer.Meta.fields = tuple(list(UserSerializer.Meta.fields) + ['nationality', 'address', 'postal_code'])


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    # Required fields for registration
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    # Allow passing basic profile fields at registration
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    nationality = serializers.CharField(write_only=True, required=False, allow_blank=True)
    address = serializers.CharField(write_only=True, required=False, allow_blank=True)
    postal_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    # Optional fields to create an initial Trademark and TrademarkAsset
    asset_kind = serializers.CharField(write_only=True, required=False, allow_blank=True)
    asset_text = serializers.CharField(write_only=True, required=False, allow_blank=True)
    asset_image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    brand_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    # Read-only representation of the created/tracked trademark and asset
    trademark = serializers.SerializerMethodField(read_only=True)
    initial_asset = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone', 'brand_name', 'asset_kind', 'asset_text', 'asset_image', 'trademark', 'initial_asset', 'full_name', 'nationality', 'address', 'postal_code')

    def create(self, validated_data):
        # Extract possible asset fields
        asset_kind = validated_data.pop('asset_kind', None) or ''
        asset_text = validated_data.pop('asset_text', None)
        asset_image = validated_data.pop('asset_image', None)
        brand_name = validated_data.pop('brand_name', None)
        # Optional profile fields
        full_name = validated_data.pop('full_name', None)
        nationality = validated_data.pop('nationality', None)
        address = validated_data.pop('address', None)
        postal_code = validated_data.pop('postal_code', None)
        
        # Required fields
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        phone = validated_data.pop('phone')

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )
        user.phone_number = phone
        
        # Set optional profile fields if provided
        if full_name:
            user.full_name = full_name
        else:
            user.full_name = f"{first_name} {last_name}".strip()
            
        if nationality:
            user.nationality = nationality
        if address:
            user.address = address
        if postal_code:
            user.postal_code = postal_code
        user.save()

        # Create an empty Trademark for the user (placeholder "mi marca")
        try:
            from .models import Trademark, TrademarkAsset
            tm = Trademark.objects.create(user=user)

            # If any asset information was provided, create a TrademarkAsset
            kind = (asset_kind or '').upper()
            if asset_image or asset_text or kind:
                # Normalize kind to known values; default to LOGO if image provided, else NAME
                valid_kinds = {c[0] for c in TrademarkAsset.Kind.choices}
                if not kind:
                    kind = 'LOGO' if asset_image else 'NAME'
                if kind not in valid_kinds:
                    kind = 'NAME'

                asset_kwargs = {'trademark': tm, 'kind': kind}
                if kind in ('NAME', 'SLOGAN'):
                    asset_kwargs['text_value'] = asset_text or brand_name or ''
                elif kind == 'LOGO':
                    # attach uploaded image file if present
                    if asset_image:
                        asset_kwargs['logo'] = asset_image
                elif kind == 'SOUND':
                    # If sound upload supported in future, user can provide via asset_image field too
                    if asset_image:
                        asset_kwargs['sound'] = asset_image

                TrademarkAsset.objects.create(**asset_kwargs)
        except Exception:
            # Non-fatal: if trademark creation fails, user creation should still succeed.
            # Log can be added in future iterations.
            pass

        return user

    def get_trademark(self, obj):
        try:
            from .models import Trademark
            tm = Trademark.objects.filter(user=obj).order_by('created_at').first()
            if not tm:
                return None
            # TrademarkSerializer is defined later in this module; reference it directly
            return TrademarkSerializer(tm, context=self.context).data
        except Exception:
            return None

    def get_initial_asset(self, obj):
        try:
            from .models import Trademark, TrademarkAsset
            tm = Trademark.objects.filter(user=obj).order_by('created_at').first()
            if not tm:
                return None
            asset = TrademarkAsset.objects.filter(trademark=tm).order_by('-id').first()
            if not asset:
                return None
            return TrademarkAssetSerializer(asset, context=self.context).data
        except Exception:
            return None

class MeView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class TrademarkAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrademarkAsset
        fields = ('id', 'kind', 'text_value', 'logo', 'sound', 'created_at', 'protect_colors', 'colors', 'includes_person_name', 'person_name', 'authorization', 'services')


class TrademarkSerializer(serializers.ModelSerializer):
    assets = TrademarkAssetSerializer(many=True, read_only=True)

    class Meta:
        model = Trademark
        fields = ('id', 'user', 'name', 'description', 'foreign_meaning', 'basis_for_registration', 'intention_of_use', 'current_use_description', 'first_use_date', 'foreign_application_number', 'foreign_application_translation', 'foreign_registration_number', 'foreign_registration_translation', 'disclaimer', 'assets', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Ensure user is set by view/context when creating
        user = self.context.get('request').user if self.context.get('request') else None
        if user and not validated_data.get('user'):
            validated_data['user'] = user
        return super().create(validated_data)


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
            'id', 'user', 'trademark', 'client_name', 'brand_name', 'country', 'title', 'content', 'rating', 'image', 'approved', 'created_at'
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
        
        # Auto-fill country from user profile if not provided
        if not validated_data.get('country') and user:
            validated_data['country'] = getattr(user, 'nationality', '') or ''
            
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

    class Meta:
        model = Testimonial
        fields = ('id', 'name', 'quote', 'logo', 'country', 'rating', 'created_at')

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
        try:
            f = getattr(obj, 'image', None)
            if f and getattr(f, 'url', None):
                request = self.context.get('request')
                url = f.url
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
        except Exception:
            pass
        return None


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'id', 'author', 'title', 'slug', 'body', 'country', 'image', 'is_published', 'created_at', 'updated_at'
        )
        read_only_fields = ('slug', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        validated_data['author'] = user
        return super().create(validated_data)


class TrademarkEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # set dynamically below if import available
        fields = ('id', 'file', 'links', 'description', 'first_use_date', 'created_at')

# Import TrademarkEvidence model lazily to avoid issues if model isn't loaded yet
try:
    from .models import TrademarkEvidence
    TrademarkEvidenceSerializer.Meta.model = TrademarkEvidence
except Exception:
    # If model not present, keep serializer base; view will raise if used
    TrademarkEvidenceSerializer.Meta.model = None


class ContactSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    message = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)
    new_password = serializers.CharField(min_length=8)


class TrademarkIntakeSerializer(serializers.Serializer):
    """Combined intake serializer to populate User, Trademark, and related Asset/Evidence.

    Accepts both JSON and multipart (for logo/evidence_file). All fields optional so it can PATCH-like update.
    """
    # Applicant/User fields
    applicant_name = serializers.CharField(required=False, allow_blank=True)
    nationality = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)

    # Trademark fields
    brand_name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    foreign_meaning = serializers.CharField(required=False, allow_blank=True)
    basis_for_registration = serializers.CharField(required=False, allow_blank=True)
    intention_of_use = serializers.BooleanField(required=False)
    current_use_description = serializers.CharField(required=False, allow_blank=True)
    first_use_date = serializers.DateField(required=False)
    foreign_application_number = serializers.CharField(required=False, allow_blank=True)
    foreign_application_translation = serializers.CharField(required=False, allow_blank=True)
    foreign_registration_number = serializers.CharField(required=False, allow_blank=True)
    foreign_registration_translation = serializers.CharField(required=False, allow_blank=True)
    disclaimer = serializers.CharField(required=False, allow_blank=True)

    # Asset (logo/name) and extra attributes
    logo = serializers.ImageField(required=False, allow_null=True)
    protect_colors = serializers.BooleanField(required=False)
    colors = serializers.CharField(required=False, allow_blank=True)
    includes_person_name = serializers.BooleanField(required=False)
    person_name = serializers.CharField(required=False, allow_blank=True)
    authorization = serializers.CharField(required=False, allow_blank=True)
    services = serializers.CharField(required=False, allow_blank=True)

    # Evidence
    evidence_file = serializers.FileField(required=False, allow_null=True)
    evidence_links = serializers.ListField(child=serializers.URLField(), required=False)
    evidence_description = serializers.CharField(required=False, allow_blank=True)
    evidence_first_use_date = serializers.DateField(required=False)

    def save(self, **kwargs):
        request = self.context.get('request')
        user = kwargs.get('user') or (getattr(request, 'user', None))
        if not user:
            raise serializers.ValidationError({'detail': 'Authentication required'})

        data = self.validated_data

        # Update User fields
        if 'applicant_name' in data:
            user.full_name = data.get('applicant_name') or user.full_name
        if 'nationality' in data:
            user.nationality = data.get('nationality') or user.nationality
        if 'address' in data:
            user.address = data.get('address') or user.address
        if 'postal_code' in data:
            user.postal_code = data.get('postal_code') or user.postal_code
        user.save()

        # Ensure Trademark exists
        tm, _ = Trademark.objects.get_or_create(user=user)

        # Map Trademark fields
        for f in (
            'name','description','foreign_meaning','basis_for_registration','intention_of_use',
            'current_use_description','first_use_date','foreign_application_number','foreign_application_translation',
            'foreign_registration_number','foreign_registration_translation','disclaimer'
        ):
            pass

        if 'brand_name' in data:
            tm.name = data.get('brand_name') or tm.name
        if 'description' in data:
            tm.description = data.get('description') or tm.description
        if 'foreign_meaning' in data:
            tm.foreign_meaning = data.get('foreign_meaning') or tm.foreign_meaning
        if 'basis_for_registration' in data:
            tm.basis_for_registration = data.get('basis_for_registration') or tm.basis_for_registration
        if 'intention_of_use' in data:
            tm.intention_of_use = data.get('intention_of_use')
        if 'current_use_description' in data:
            tm.current_use_description = data.get('current_use_description') or tm.current_use_description
        if 'first_use_date' in data:
            tm.first_use_date = data.get('first_use_date')
        if 'foreign_application_number' in data:
            tm.foreign_application_number = data.get('foreign_application_number') or tm.foreign_application_number
        if 'foreign_application_translation' in data:
            tm.foreign_application_translation = data.get('foreign_application_translation') or tm.foreign_application_translation
        if 'foreign_registration_number' in data:
            tm.foreign_registration_number = data.get('foreign_registration_number') or tm.foreign_registration_number
        if 'foreign_registration_translation' in data:
            tm.foreign_registration_translation = data.get('foreign_registration_translation') or tm.foreign_registration_translation
        if 'disclaimer' in data:
            tm.disclaimer = data.get('disclaimer') or tm.disclaimer
        tm.save()

        # Create or update an asset (prefer LOGO if logo provided)
        asset = TrademarkAsset.objects.filter(trademark=tm, kind=TrademarkAsset.Kind.LOGO).order_by('-id').first()
        if not asset:
            # If no logo asset exists and we have asset-related data, create one
            if any(k in data for k in ('logo','protect_colors','colors','includes_person_name','person_name','authorization','services')):
                asset = TrademarkAsset.objects.create(trademark=tm, kind=TrademarkAsset.Kind.LOGO)
        if asset:
            if 'logo' in data and data.get('logo') is not None:
                asset.logo = data.get('logo')
            if 'protect_colors' in data:
                asset.protect_colors = bool(data.get('protect_colors'))
            if 'colors' in data:
                asset.colors = data.get('colors') or asset.colors
            if 'includes_person_name' in data:
                asset.includes_person_name = bool(data.get('includes_person_name'))
            if 'person_name' in data:
                asset.person_name = data.get('person_name') or asset.person_name
            if 'authorization' in data:
                asset.authorization = data.get('authorization') or asset.authorization
            if 'services' in data:
                asset.services = data.get('services') or asset.services
            asset.save()

        # Evidence: create a new record if provided
        has_evidence = any(k in data for k in ('evidence_file','evidence_links','evidence_description','evidence_first_use_date'))
        if has_evidence:
            from .models import TrademarkEvidence
            links = data.get('evidence_links') or []
            ev_first = data.get('evidence_first_use_date') or tm.first_use_date
            TrademarkEvidence.objects.create(
                trademark=tm,
                file=data.get('evidence_file'),
                links=links,
                description=data.get('evidence_description') or '',
                first_use_date=ev_first,
            )

        # Build combined response structure
        from .serializers import TrademarkSerializer, TrademarkAssetSerializer
        payload = {
            'user': UserSerializer(user, context=self.context).data,
            'trademark': TrademarkSerializer(tm, context=self.context).data,
        }
        if asset:
            payload['asset'] = TrademarkAssetSerializer(asset, context=self.context).data
        return payload