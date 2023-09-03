import pytest
import json
import os
from unittest.mock import patch, mock_open
from aura.token_repository import check_existing_token, save_token, delete_token_file
from datetime import datetime, timedelta


def test_check_existing_token_not_existing():
    with patch("os.path.isfile", return_value=False):
        result = check_existing_token()
        assert result is None


def test_check_existing_token_expired_token():
    mock_file_content = {
        "token": "mock_token",
        "expires_at": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
    }

    with patch("os.path.isfile", return_value=True), patch(
        "builtins.open", mock_open(read_data=json.dumps(mock_file_content))
    ):
        result = check_existing_token()
        assert result is None


def test_check_existing_token_valid_token():
    mock_file_content = {
        "token": "mock_token",
        "expires_at": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
    }

    with patch("os.path.isfile", return_value=True), patch(
        "builtins.open", mock_open(read_data=json.dumps(mock_file_content))
    ):
        result = check_existing_token()
        assert result == "mock_token"


def test_save_token():
    mock_token = "test_token"
    mock_expires_in = 3600

    expected_expiry_time_str = (datetime.now() + timedelta(seconds=mock_expires_in)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    expected_token_json = {"token": mock_token, "expires_at": expected_expiry_time_str}

    m = mock_open()
    with patch("builtins.open", m), patch("json.dump") as mock_json_dump:
        save_token(mock_token, mock_expires_in)

        mock_file_handle = m()
        mock_json_dump.assert_called_once_with(expected_token_json, mock_file_handle)


def test_delete_existing_token_file():
    with patch("os.path.isfile", return_value=True), patch("os.remove") as mock_remove:
        delete_token_file()

        mock_remove.assert_called_once_with(os.path.expanduser("~/.aura/token.json"))
