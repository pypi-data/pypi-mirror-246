"""Mlflow plugin proxy auth"""

import base64
import os

from mlflow.tracking.request_auth.abstract_request_auth_provider import (
    RequestAuthProvider,
)
from requests.auth import AuthBase


class ProxyAuthProvider(RequestAuthProvider):
    """"Mlflow plugin class"""

    def __init__(self):
        self.username = os.getenv("MLFLOW_PROXY_USERNAME")
        self.password = os.getenv("MLFLOW_PROXY_PASSWORD")

    def get_name(self):
        return "proxy_auth_provider"

    def get_auth(self):
        return ProxyAuth(self.username, self.password)


class ProxyAuth(AuthBase):
    """Requests proxy auth class"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, r):
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )
        r.headers["Proxy-Authorization"] = f"Basic {encoded_credentials}"
        return r
