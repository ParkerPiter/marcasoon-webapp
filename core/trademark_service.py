import requests
from typing import Dict, Any, Optional
from django.conf import settings
from urllib.parse import quote

class TrademarkLookupClient:
    """Client for RapidAPI Trademark Lookup API."""
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key or getattr(settings, 'TRADEMARK_LOOKUP_API_KEY', '')
        self.base_url = (base_url or getattr(settings, 'TRADEMARK_LOOKUP_API_BASE', '')).rstrip('/')
        self.timeout = timeout
        if not self.api_key:
            raise RuntimeError('TRADEMARK_LOOKUP_API_KEY missing')

    def _headers(self) -> Dict[str, str]:
        return {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'trademark-lookup-api.p.rapidapi.com',
            'Accept': 'application/json',
            'User-Agent': 'marcasoon/1.0'
        }

    def get(self, path: str) -> Any:
        if not path.startswith('/'):
            path = '/' + path
        url = f"{self.base_url}{path}"
        resp = requests.get(url, headers=self._headers(), timeout=self.timeout)
        resp.raise_for_status()
        ct = resp.headers.get('Content-Type', '')
        if 'application/json' in ct:
            return resp.json()
        return {'content_type': ct, 'text': resp.text, 'status_code': resp.status_code, 'url': resp.url}

    def classification_search(self, name: str, page: int = 1, page_size: int = 10) -> Any:
        """Pattern: /{name}/classificationsearch/{page}/{page_size}
        Returns classification search results for the given trademark name.
        """
        safe_name = name.strip()
        if not safe_name:
            raise ValueError('Empty name')
        if page < 1:
            raise ValueError('page must be >= 1')
        if page_size < 1:
            raise ValueError('page_size must be >= 1')
        encoded = quote(safe_name)
        path = f"/{encoded}/classificationsearch/{page}/{page_size}"
        return self.get(path)

    def name_search(self, name: str, page: int = 1, count: int = 10) -> Any:
        """Pattern: /{name}/namesearch/{page}/{count}
        Returns JSON list of results for the given trademark name.
        """
        safe_name = name.strip()
        if not safe_name:
            raise ValueError('Empty name')
        if page < 1:
            raise ValueError('page must be >= 1')
        if count < 1:
            raise ValueError('count must be >= 1')
        path = f"/{safe_name}/namesearch/{page}/{count}"
        return self.get(path)
