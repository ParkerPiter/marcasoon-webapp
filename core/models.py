from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username or self.full_name or super().__str__()


class Trademark(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trademark')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    price_cents = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    currency = models.CharField(max_length=10, default='USD')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.currency} {self.price_cents/100:.2f})"

