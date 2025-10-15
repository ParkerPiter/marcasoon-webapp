## Marcasoon

Backend API using Django + DRF with JWT/session auth, RapidAPI Trademark Lookup, and Stripe payments.

### Stripe setup
- Configure environment variables (or edit `marcasoon/settings.py` for dev defaults):
	- STRIPE_PUBLIC_KEY
	- STRIPE_SECRET_KEY
	- STRIPE_WEBHOOK_SECRET (optional for local unless testing webhooks)
	- STRIPE_CURRENCY (default `usd`)
	- FRONTEND_URL (default `http://localhost:3000`)

### Endpoints
- GET `/api/stripe/config/` → `{ publicKey, currency }`
- POST `/api/stripe/create-checkout-session/` (auth required)
	- Body: `{ price_id: "price_..." }` or `{ amount: 5000, currency: "usd" }`
	- Response: `{ id, url }`
- POST `/api/stripe/create-payment-intent/` (auth required)
	- Body: `{ amount: 5000, currency: "usd" }`
	- Response: `{ client_secret }`
- POST `/api/stripe/webhook/` → set your Stripe endpoint to this URL and provide the signing secret in STRIPE_WEBHOOK_SECRET

### Quick checks
1. Install deps: `pip install -r requirements.txt`
2. Run checks: `python manage.py check`
3. Ensure auth works (JWT or session login via `/api/auth/`)
