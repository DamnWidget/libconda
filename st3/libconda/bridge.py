import requests

from .packages.typing import Dict


class GolcondaBridge:
    """Bridge between ST3 and Golconda's standalone service
    """

    def __init__(self, hostname: str, port: int):
        self.__hostname = hostname
        self.__port = port

    @property
    def hostname(self) -> str:
        """Return the hostname:port to connect to
        """

        return 'http://{}:{}'.format(self.__hostname, self.__port)

    def request(self, end: str, pl: Dict, ttl: float=0.1) -> requests.Response:
        """Make a request to the Golconda service and return it's result

        Requests to Golconda are always POST (Except for instrumentation)
        """

        endpoint = '{}/{}'.format(self.hostname, end)
        return requests.post(endpoint, json=pl, timeout=ttl)
