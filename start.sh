#! /usr/bin/env bash

set -o errexit
set -o pipefail

echo "[start] Running database migrations..."
python manage.py migrate --noinput

echo "[start] Creating superuser if env vars are set..."
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]] && [[ -n "${DJANGO_SUPERUSER_EMAIL:-}" ]] && [[ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  python - <<'PY'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcasoon.settings')
django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']
email = os.environ['DJANGO_SUPERUSER_EMAIL']
password = os.environ['DJANGO_SUPERUSER_PASSWORD']

if not User.objects.filter(username=username).exists():
    print(f"[start] Creating superuser '{username}'...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print(f"[start] Superuser '{username}' already exists. Skipping.")
PY
else
  echo "[start] DJANGO_SUPERUSER_* not set; skipping superuser creation."
fi

echo "[start] Seeding Plans (idempotent)..."
python manage.py shell <<'PY'
from core.models import Plan

def seed_plans():
    p1, _ = Plan.objects.update_or_create(
        title="A tu manera",
        defaults=dict(
            description="Ofrecemos una asesoría estratégica para que entiendas los pasos clave y te sientas seguro al iniciar tu solicitud",
            client_objective="Emprendedores que buscan orientación para iniciar el proceso por su cuenta",
            includes=[
                "Guia para realizar tu búsqueda inicial antes de presentar tu solicitud y clasificar la(s) clase(s) de bienes y/o servicios a proteger",
                "Una hoja de ruta clara para tu proceso de registro, con recomendaciones de nuestro equipo.",
                "Debes presentar tu solicitud directamente ante la USPTO",
            ],
            price_cents=None,
            base_price_cents=8900,
            fee_cents=35000,
            currency="USD",
            is_active=True,
        ),
    )
    print(f"[start] Seeded plan '{p1.title}' (id={p1.id}) total={p1.total_cents/100:.2f} {p1.currency}")

    p2, _ = Plan.objects.update_or_create(
        title="Contigo",
        defaults=dict(
            description="Quienes quieren una gestión profesional y prefieren delegar el proceso de registro.",
            client_objective="Nos encargamos de todo el proceso para que tu marca quede blindada de principio a fin, con la seguridad de que un experto te representa.",
            includes=[
                "Todo lo del Plan a tu manera.",
                "Análisis exhaustivo y profesional de tu marca.",
                "Preparación y presentación de la solicitud oficial.",
                "Representación y gestión de la comunicación con la oficina de marcas (Incluye 1 respuesta a acciones oficiales por detalles de forma)",
                "Monitoreo constante del estado de tu solicitud.",
                "Sesión virtual de consultoría con un abogado licenciado en USA",
            ],
            price_cents=None,
            base_price_cents=45000,
            fee_cents=35000,
            currency="USD",
            is_active=True,
        ),
    )
    print(f"[start] Seeded plan '{p2.title}' (id={p2.id}) total={p2.total_cents/100:.2f} {p2.currency}")

    p3, _ = Plan.objects.update_or_create(
        title="Blindado",
        defaults=dict(
            description="Quienes buscan la máxima seguridad y desean proteger su inversión.",
            client_objective="Este plan te da la tranquilidad total. Nos comprometemos con el éxito de tu registro y te garantizamos que tu inversión profesional está protegida.",
            includes=[
                "Todo lo del Plan Contigo.",
                "Incluye reporte de búsqueda profunda incluyendo a nivel federal y páginas web.",
                "Dos sesiones virtuales de consultoría con abogado licenciado en USA. ",
                "Prioridad en procesamiento y respuestas por parte de nuestro equipo.",
                "Modelo de carta de Cease and Desist para proteger tu marca ",
                "Asesoría para registro de marca a nivel internacional",
            ],
            price_cents=None,
            base_price_cents=99000,
            fee_cents=35000,
            currency="USD",
            is_active=True,
        ),
    )
    print(f"[start] Seeded plan '{p3.title}' (id={p3.id}) total={p3.total_cents/100:.2f} {p3.currency}")

seed_plans()
PY

echo "[start] Launching Gunicorn..."
exec gunicorn marcasoon.wsgi:application --bind 0.0.0.0:"${PORT}"
