import backoff
import requests
from requests.exceptions import ConnectionError
from singer import metrics
import singer

LOGGER = singer.get_logger()


class Server500Error(Exception):
    pass


ERROR_CODE_EXCEPTION_MAPPING = {
    500: Server500Error
}


def get_exception_for_error_code(error_code):
    return ERROR_CODE_EXCEPTION_MAPPING.get(error_code)


def raise_for_error(response):
    LOGGER.error('ERROR {}: {}, REASON: {}'.format(response.status_code,
                                                   response.text, response.reason))
    try:
        response.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError) as error:
        try:
            content_length = len(response.content)
            if content_length == 0:
                return
            raise Server500Error(error)
        except (ValueError, TypeError):
            raise Server500Error(error)


class PokeApiClient:
    def __init__(
        self,
        page_size: int = 10
    ) -> None:
        self.base_url = "https://pokeapi.co/api/v2"
        self.page_size = page_size

    @backoff.on_exception(backoff.expo,
                          (Server500Error, ConnectionError),
                          max_tries=7)
    def request(self, method, path=None, url=None, json=None, **kwargs):
        if not url and path:
            url = '{}/{}'.format(self.base_url, path)

        if 'endpoint' in kwargs:
            endpoint = kwargs['endpoint']
            del kwargs['endpoint']
        else:
            endpoint = None

        if method == 'POST':
            kwargs['headers']['Content-Type'] = 'application/json'

        with metrics.http_request_timer(endpoint) as timer:
            response = requests.request(
                method=method,
                url=url,
                json=json,
                **kwargs)
            timer.tags[metrics.Tag.http_status_code] = response.status_code

        if response.status_code >= 500:
            raise Server500Error()

        if response.status_code != 200:
            raise_for_error(response)

        return response.json()
