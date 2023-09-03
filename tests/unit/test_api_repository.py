import pytest
from unittest.mock import patch, MagicMock, Mock
import requests
from aura.api_repository import get_headers, _get_credentials, make_api_call, _authenticate
from aura.error_handler import NoCredentialsConfigured


@pytest.fixture
def mock_context():
    mock_context = MagicMock()
    mock_config = MagicMock()
    mock_config.get_option.return_value = None
    mock_context.obj = mock_config
    with patch("click.get_current_context", return_value=mock_context):
        yield


def test_get_headers(mock_version):
    with patch("aura.api_repository._authenticate", return_value="mock_token"):
        headers = get_headers()
        expected_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer mock_token",
            "User-Agent": "AuraCLI/1.0.0",
        }
        assert headers == expected_headers


def test_make_api_call(api_request, get_headers, mock_context):
    mock_response = MagicMock()
    mock_response.status_code = 200
    api_request.return_value = mock_response

    make_api_call("GET", "/instances")

    api_request.assert_called_once_with(
        "GET",
        "https://api.neo4j.io/v1/instances",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer dummy-token",
        },
        timeout=10,
    )


def test_make_api_call_with_url_env_var(monkeypatch, api_request, get_headers, mock_context):
    monkeypatch.setenv("AURA_CLI_BASE_URL", "https://test-url.neo4j.io/v2")

    mock_response = MagicMock()
    mock_response.status_code = 200
    api_request.return_value = mock_response

    make_api_call("GET", "/instances")

    api_request.assert_called_once_with(
        "GET",
        "https://test-url.neo4j.io/v2/instances",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer dummy-token",
        },
        timeout=10,
    )


def test_make_api_call_failed_auth(api_request, get_headers, mock_context):
    mock_response = MagicMock()
    mock_response.status_code = 403
    api_request.return_value = mock_response

    with patch("aura.api_repository.delete_token_file", new_callable=Mock()) as mocked_delete_token:
        make_api_call("GET", "/instances")

        api_request.assert_called_once_with(
            "GET",
            "https://api.neo4j.io/v1/instances",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer dummy-token",
            },
            timeout=10,
        )
        mocked_delete_token.assert_called_once()


def test_get_credentials_from_env_vars(monkeypatch):
    monkeypatch.setenv("AURA_CLI_CLIENT_ID", "client-123")
    monkeypatch.setenv("AURA_CLI_CLIENT_SECRET", "secret-123")

    client_id, client_secret = _get_credentials()

    assert client_id == "client-123"
    assert client_secret == "secret-123"


def test_get_credentials_from_config():
    mock_context = MagicMock()
    mock_config = MagicMock()
    mock_config.current_credentials.return_value = (
        None,
        {"CLIENT_ID": "client-1234", "CLIENT_SECRET": "secret-1234"},
    )
    mock_context.obj = mock_config

    with patch("click.get_current_context", return_value=mock_context):
        client_id, client_secret = _get_credentials()

        assert client_id == "client-1234"
        assert client_secret == "secret-1234"


def test_get_credentials_not_found():
    mock_context = MagicMock()
    mock_config = MagicMock()
    mock_config.current_credentials.return_value = (None, None)
    mock_context.obj = mock_config

    with patch("click.get_current_context", return_value=mock_context):
        with pytest.raises(NoCredentialsConfigured):
            _get_credentials()


def test_authenticate(api_request, mock_context):
    with patch("aura.api_repository.check_existing_token", return_value=None), patch(
        "aura.api_repository._get_credentials", return_value=("mock_id", "mock_secret")
    ), patch("aura.api_repository.save_token") as mock_save_token:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "new_mock_token", "expires_in": 3600}
        api_request.return_value = mock_response

        token = _authenticate()

        mock_save_token.assert_called_with("new_mock_token", 3600)
        assert token == "new_mock_token"


def test_authenticate_with_existing_token():
    with patch("aura.api_repository.check_existing_token", return_value="mock_token"):
        token = _authenticate()

    assert token == "mock_token"


def test_authenticate_failure(api_request, mock_context):
    api_request.side_effect = requests.exceptions.HTTPError("Forbidden")

    with patch("aura.api_repository.check_existing_token", return_value=None), patch(
        "aura.api_repository._get_credentials", return_value=("mock_id", "mock_secret")
    ):
        with pytest.raises(requests.exceptions.HTTPError):
            _authenticate()
