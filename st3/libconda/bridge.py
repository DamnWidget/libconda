import requests

from .packages.typing import Dict
from .packages.prometheus_client import Summary, Counter

REQUEST_TIME = Summary(
    'golconda_request_processing_seconds',
    'Time spent processing requests from ST3 plugins to golconda server'
)

REQUESTS_COUNT = Counter(
    'golconda_requests_total', 'Total number of requests performed'
)

REQUESTS_EXCEPTIONS = Counter(
    'golconda_requests_exceptions', 'Number of raised exceptions on requests'
)


class GolcondaBridge:
    """Bridge between ST3 and Golconda's standalone service
    """

    def __init__(self, hostname: str, port: int) -> None:
        self.__hostname = hostname
        self.__port = port

    @property
    def hostname(self) -> str:
        """Return the hostname:port to connect to
        """

        return 'http://{}:{}'.format(self.__hostname, self.__port)

    @REQUEST_TIME.time()
    def request(self, end: str, pl: Dict, ttl: float=0.1) -> requests.Response:
        """Make a request to the Golconda service and return it's result

        Requests to Golconda are always POST (Except for instrumentation)
        """

        REQUESTS_COUNT.inc()

        with REQUESTS_EXCEPTIONS.count_exceptions():
            endpoint = '{}/{}'.format(self.hostname, end)
            result = requests.post(endpoint, json=pl, timeout=ttl)

        return result
