from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def send_invoice_email(user, plan, amount_cents, currency, payment_method):
    """
    Envía un correo de factura/confirmación al usuario tras un pago exitoso.
    """
    try:
        subject = 'Recibo de tu pago - Marcasoon'
        
        # Formatear el monto (de centavos a decimal)
        try:
            amount_val = "{:.2f}".format(int(amount_cents) / 100.0)
        except (ValueError, TypeError):
            amount_val = "0.00"

        context = {
            'user_name': user.get_full_name() or user.username,
            'plan_name': plan.title if hasattr(plan, 'title') else 'Plan Marcasoon',
            'amount': amount_val,
            'currency': currency.upper(),
            'date': timezone.now().strftime('%d/%m/%Y %H:%M'),
            'payment_method': payment_method,
            'site': settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'marcasoon.com'
        }

        html_message = render_to_string('emails/invoice_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
        
        send_mail(
            subject,
            plain_message,
            from_email,
            [user.email],
            html_message=html_message,
            fail_silently=False
        )
        logger.info(f"Invoice email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send invoice email to {user.email}: {e}")
        return False
