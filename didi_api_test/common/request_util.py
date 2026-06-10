import requests

from common.config import BASE_URL, DEFAULT_TIMEOUT


class RequestUtil:
    """Small wrapper around requests for this learning project."""

    def __init__(self, base_url=BASE_URL, timeout=DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path, params=None, headers=None):
        url = self.base_url + path
        return requests.get(url, params=params, headers=headers, timeout=self.timeout)

    def post(self, path, json=None, headers=None):
        url = self.base_url + path
        return requests.post(url, json=json, headers=headers, timeout=self.timeout)
