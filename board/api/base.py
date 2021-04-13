from abc import ABC, abstractmethod


class BaseWrapper(ABC):
    def __init__(self, api_url):
        self._api_url = api_url

    def _api_request(self, endpoint, query, requests_method):
        url = self._build_url(endpoint)
        params = self._compose_request(query)
        response = requests_method(url, **params)
        response.raise_for_status()
        return response.json()

    def _build_url(self, endpoint=''):
        return f'{self._api_url}{endpoint}'

    @abstractmethod
    def _compose_request(self, query):
        pass
