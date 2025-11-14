from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    # Additional profile fields used by the intake form
    nationality = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username or self.full_name or super().__str__()


class Trademark(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trademark')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Fields added to capture intake form data
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    foreign_meaning = models.CharField(max_length=255, blank=True)
    basis_for_registration = models.CharField(max_length=100, blank=True)
    intention_of_use = models.BooleanField(null=True, blank=True)
    current_use_description = models.TextField(blank=True)
    first_use_date = models.DateField(null=True, blank=True)
    foreign_application_number = models.CharField(max_length=120, blank=True)
    foreign_application_translation = models.TextField(blank=True)
    foreign_registration_number = models.CharField(max_length=120, blank=True)
    foreign_registration_translation = models.TextField(blank=True)
    disclaimer = models.TextField(blank=True)

    def __str__(self):
        return f"Trademark of {getattr(self.user, 'username', 'user')}"


class TrademarkAsset(models.Model):
    class Kind(models.TextChoices):
        NAME = 'NAME', 'Nombre'
        LOGO = 'LOGO', 'Logo (JPEG)'
        SLOGAN = 'SLOGAN', 'Slogan'
        SOUND = 'SOUND', 'Sonido'

    trademark = models.ForeignKey(Trademark, on_delete=models.CASCADE, related_name='assets')
    kind = models.CharField(max_length=10, choices=Kind.choices)
    text_value = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    sound = models.FileField(upload_to='sounds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Extra metadata commonly collected in intake forms
    protect_colors = models.BooleanField(default=False)
    colors = models.CharField(max_length=255, blank=True)
    includes_person_name = models.BooleanField(default=False)
    person_name = models.CharField(max_length=200, blank=True)
    authorization = models.TextField(blank=True)
    services = models.TextField(blank=True)


class TrademarkEvidence(models.Model):
    """Files/links used as proof of use or supporting documents for a Trademark."""
    trademark = models.ForeignKey(Trademark, on_delete=models.CASCADE, related_name='evidence')
    file = models.FileField(upload_to='evidence/', null=True, blank=True)
    # store multiple links as JSON array or leave blank
    links = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)
    first_use_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Evidence for {self.trademark} ({self.created_at:%Y-%m-%d})"

    def __str__(self):
        return f"{self.kind} for {self.trademark.user}" if self.trademark_id else self.kind

    def clean(self):
        # Minimal validation to ensure the appropriate field is provided per kind
        from django.core.exceptions import ValidationError
        if self.kind in (self.Kind.NAME, self.Kind.SLOGAN):
            if not self.text_value:
                raise ValidationError({'text_value': 'Este campo es requerido para Nombre/Slogan.'})
        elif self.kind == self.Kind.LOGO:
            if not self.logo:
                raise ValidationError({'logo': 'Debes subir un archivo JPEG para Logo.'})
        elif self.kind == self.Kind.SOUND:
            if not self.sound:
                raise ValidationError({'sound': 'Debes subir un archivo de audio para Sonido.'})


class Plan(models.Model):
    """Planes vendibles para checkout (Stripe/PayPal)."""
    title = models.CharField(max_length=120)
    description = models.TextField()
    client_objective = models.CharField(max_length=255)
    includes = models.JSONField(default=list, help_text="Lista de elementos incluidos en el plan")
    # Guardamos precio en centavos para precisión
    # (DEPRECATED) price_cents: mantenido por compatibilidad, no se usa si hay base/fee
    price_cents = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    # Desglose de costos (en centavos)
    base_price_cents = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0, help_text="Precio del plan sin tasas")
    fee_cents = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=35000, help_text="Tasa USPTO u otra, en centavos")
    currency = models.CharField(max_length=10, default='USD')
    is_active = models.BooleanField(default=True)

    def __str__(self):
            return f"{self.title} ({self.currency} {self.total_cents/100:.2f})"

    @property
    def total_cents(self) -> int:
        """Total a cobrar = base + fee. Si no hay base/fee, usa price_cents como respaldo."""
        if self.base_price_cents is not None or self.fee_cents is not None:
            return int((self.base_price_cents or 0) + (self.fee_cents or 0))
        return int(self.price_cents or 0)


class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='testimonials')
    trademark = models.ForeignKey('Trademark', on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    client_name = models.CharField(max_length=150)
    brand_name = models.CharField(max_length=150)
    title = models.CharField(max_length=180, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        who = self.client_name or getattr(self.user, 'username', 'user')
        return f"{who} sobre {self.brand_name}" if self.brand_name else who


class BlogPost(models.Model):
    """Blog/foro: entradas creadas por usuarios.
    - author: usuario creador
    - title, slug: título y slug único
    - body: contenido
    - is_published: visible públicamente si True
    - created_at/updated_at
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Autogenerar slug único a partir del título si no se suministra
        if not self.slug:
            base = slugify(self.title) or 'post'
            candidate = base
            i = 1
            Model = self.__class__
            while Model.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f"{base}-{i}"
            self.slug = candidate
        super().save(*args, **kwargs)


class PasswordResetCode(models.Model):
    """Reset codes for password recovery via email."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='password_reset_codes')
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'code']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"ResetCode({self.user_id}, {self.code}, used={self.used})"

    def is_valid(self) -> bool:
        return (not self.used) and timezone.now() <= self.expires_at

