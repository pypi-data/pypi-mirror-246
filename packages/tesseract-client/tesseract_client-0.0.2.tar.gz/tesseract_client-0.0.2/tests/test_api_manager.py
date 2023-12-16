import pytest
from responses import RequestsMock
import requests
from tesseract.settings import API_URL
from tesseract.api_manager import (
    APIManager,
    InvalidCredentials,
    ServerError,
    NotFoundError
)


def test_login_successful():
    api_urls = API_URL("https://example.com")
    manager = APIManager("user", "pass", api_urls)

    with RequestsMock() as rsps:
        rsps.add(rsps.POST, api_urls.login, json={"access_token": "token123"}, status=200)
        manager.login()

        assert manager.access_token == "token123"


def test_login_invalid_credentials():
    api_urls = API_URL("https://example.com")
    manager = APIManager("user", "wrongpass", api_urls)

    with RequestsMock() as rsps:
        rsps.add(rsps.POST, api_urls.login, status=401)

        with pytest.raises(InvalidCredentials):
            manager.login()


def test_login_server_error():
    api_urls = API_URL("https://example.com")
    manager = APIManager("user", "pass", api_urls)

    with RequestsMock() as rsps:
        rsps.add(rsps.POST, api_urls.login, status=500)

        with pytest.raises(ServerError):
            manager.login()


def test_login_not_found_error():
    api_urls = API_URL("https://example.com")
    manager = APIManager("user", "pass", api_urls)

    with RequestsMock() as rsps:
        rsps.add(rsps.POST, api_urls.login, status=404)

        with pytest.raises(NotFoundError):
            manager.login()
