import pytest
from unittest.mock import patch, Mock
import pprint

def mock_headers():
    return {"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"}

@pytest.fixture(autouse=True)
def get_headers():
    with patch('aura.api_repository.get_headers', new=mock_headers):
        yield

@pytest.fixture()
def api_request():
    with patch('requests.request', new_callable=Mock()) as mocked_request:
        yield mocked_request

# Utility function to verify the command output is printed correctly
def printed_data(data):
    return pprint.pformat(data) + "\n"