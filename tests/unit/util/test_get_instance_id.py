from unittest.mock import patch
import pytest

from aura.util.get_instance_id import get_instance_id
from aura.error_handler import (
    InstanceIDAndNameBothProvided,
    InstanceIDorNameMissing,
    InstanceNameNotFound,
    InstanceNameNotUnique,
)


def test_both_id_and_name_provided():
    with pytest.raises(InstanceIDAndNameBothProvided):
        get_instance_id("some_id", "some_name")


def test_only_id_provided():
    assert get_instance_id("some_id", None) == "some_id"


def test_neither_id_nor_name_provided():
    with pytest.raises(InstanceIDorNameMissing):
        get_instance_id(None, None)


@patch("aura.util.get_instance_id.make_api_call")
def test_instance_name_provided_found_once(mock_make_api_call):
    mock_make_api_call.return_value.json.return_value = {
        "data": [{"id": "123", "name": "my_instance"}]
    }
    assert get_instance_id(None, "my_instance") == "123"


@patch("aura.util.get_instance_id.make_api_call")
def test_instance_name_provided_found_multiple(mock_make_api_call):
    mock_make_api_call.return_value.json.return_value = {
        "data": [{"id": "123", "name": "my_instance"}, {"id": "456", "name": "my_instance"}]
    }
    with pytest.raises(InstanceNameNotUnique):
        get_instance_id(None, "my_instance")


@patch("aura.util.get_instance_id.make_api_call")
def test_instance_name_provided_not_found(mock_make_api_call):
    mock_make_api_call.return_value.json.return_value = {
        "data": [{"id": "123", "name": "other_instance"}]
    }
    with pytest.raises(InstanceNameNotFound):
        get_instance_id(None, "my_instance")
