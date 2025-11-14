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

### Live webinar embed
- Public JSON endpoint: `GET /api/webinar/live/`
	- Returns `{ "embed_url": "https://..." }` with the configured stream URL.
	- Configure the stream URL with the `WEBINAR_EMBED_URL` environment variable (supports YouTube/Vimeo/Zoom embed links), e.g.:
		- `WEBINAR_EMBED_URL=https://www.youtube.com/embed/VIDEO_ID?autoplay=1`
	- In development you can override via query param: `/api/webinar/live/?url=https://...` (only when `DEBUG=True`).
- Example (React):
	```tsx
	import { useEffect, useState } from 'react';

	export default function LiveWebinar() {
		const [url, setUrl] = useState('');
		useEffect(() => {
			fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/webinar/live/`)
				.then(r => r.json())
				.then(d => setUrl(d.embed_url || ''))
				.catch(() => setUrl(''));
		}, []);
		if (!url) return <p>No hay webinar configurado.</p>;
		return (
			<div style={{position:'relative',paddingTop:'56.25%'}}>
				<iframe
					src={url}
					title="Webinar en vivo"
					allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
					allowFullScreen
					style={{position:'absolute',inset:0,width:'100%',height:'100%',border:0}}
				/>
			</div>
		);
	}
	```
