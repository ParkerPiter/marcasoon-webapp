import logging
from typing import Any, Dict, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class USPTOClient:
    def __init__(self,
                 base_url: Optional[str] = None,
                 api_key: Optional[str] = None,
                 timeout: int = 30):
        # Read from settings safely; allow direct string config
        base = base_url or getattr(settings, 'USPTO_API_BASE', '')
        self.base_url = base.rstrip('/') if base else ''
        self.api_key = api_key or getattr(settings, 'USPTO_API_KEY', '')
        self.timeout = timeout
        if not self.api_key:
            logger.warning("USPTO_API_KEY is not set; requests will likely fail.")

    def _headers(self) -> Dict[str, str]:
        return {
            'X-Api-Key': self.api_key,
            'Accept': 'application/json',
            'User-Agent': 'marcasoon-webapp/1.0'
        }

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, expect_json: bool = True):
        # Support absolute URLs and relative paths
        if path.startswith('http://') or path.startswith('https://'):
            url = path
        else:
            if not self.base_url:
                raise RuntimeError('USPTO_API_BASE is not configured')
            if not path.startswith('/'):
                path = '/' + path
            url = f"{self.base_url}{path}"
        params = dict(params or {})
        # Some api.data.gov proxies require api_key param; include both header and query param.
        if self.api_key and 'api_key' not in params:
            params['api_key'] = self.api_key
        resp = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            # Log helpful context for 4xx/5xx
            snippet = resp.text[:500] if resp.text else ''
            logger.error("USPTO request failed %s %s -> %s: %s", url, params, resp.status_code, snippet)
            raise
        if expect_json:
            # Try to parse JSON; if not JSON, raise to surface mismatch
            ct = resp.headers.get('Content-Type', '')
            if 'application/json' in ct:
                return resp.json()
            # Fallback attempt but wrap as structured payload
            return {
                'content_type': ct,
                'text': resp.text,
                'url': resp.url,
                'status_code': resp.status_code,
            }
        else:
            return resp.text

    # Example wrappers — replace paths with actual ones from documentation
    def tsdr_case_status(self,
                         serial_number: Optional[str] = None,
                         registration_number: Optional[str] = None,
                         case_id: Optional[str] = None):
        path = getattr(settings, 'USPTO_TSDR_CASE_STATUS_PATH', '') or 'trademark/v1/tsdr/case-status'
        # If path expects a case id placeholder, use it and return text (HTML)
        if '{case.id}' in path:
            if not case_id:
                raise ValueError('Provide case_id for the configured casestatus path')
            filled = path.replace('{case.id}', str(case_id))
            return self.get(filled, expect_json=False)

        # Default JSON API flow with serial/registration
        params: Dict[str, Any] = {}
        sn = self._clean_identifier(serial_number)
        rn = self._clean_identifier(registration_number)
        if sn:
            params['serialNumber'] = sn
        if rn:
            params['registrationNumber'] = rn
        if not params:
            raise ValueError('Provide serial_number or registration_number')
        return self.get(path, params, expect_json=True)

    def trademark_search(self, q: str, **filters: Any) -> Dict[str, Any]:
        path = getattr(settings, 'USPTO_TRADEMARK_SEARCH_PATH', '') or 'trademark/v1/search'
        params = {'searchText': q}
        params.update(filters)
        return self.get(path, params)

    @staticmethod
    def _clean_identifier(value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        v = str(value).strip()
        # common prefixes like 'sn' can appear; strip non-digits
        digits = ''.join(ch for ch in v if ch.isdigit())
        return digits or None

    # Explicit JSON variant independent from HTML path setting
    def tsdr_case_status_json(self,
                              serial_number: Optional[str] = None,
                              registration_number: Optional[str] = None) -> Dict[str, Any]:
        path = 'trademark/v1/tsdr/case-status'
        params: Dict[str, Any] = {}
        sn = self._clean_identifier(serial_number)
        rn = self._clean_identifier(registration_number)
        if sn:
            params['serialNumber'] = sn
        if rn:
            params['registrationNumber'] = rn
        if not params:
            raise ValueError('Provide serial_number or registration_number')
        return self.get(path, params, expect_json=True)

    def last_update_info(self, serial: str) -> Dict[str, Any]:
        """GET https://tsdrapi.uspto.gov/last-update/info.json?sn={serial}
        Public endpoint; no api_key required; absolute URL to avoid api.uspto.gov base.
        """
        serial_clean = self._clean_identifier(serial) or serial
        url = f"https://tsdrapi.uspto.gov/last-update/info.json?sn={serial_clean}"
        # Use absolute URL and expect JSON
        return self.get(url, params=None, expect_json=True)
