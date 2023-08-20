import pytest
from click.testing import CliRunner
from unittest.mock import Mock
import json

from aura.instances import create as create_instance
from tests.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "data": {
            "connection_url": "neo4j+s://some-url",
            "id": "4k23f9n",
            "password": "qweasd",
            "tenant_id": "123",
            "username": "neo4j",
            "cloud_provider": "gcp",
        }
    }
    return mock_res


def test_create_instance(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(
        create_instance,
        [
            "--name",
            "TestInstance",
            "--type",
            "professional-db",
            "--region",
            "europe-west1",
            "--tenant-id",
            "123",
            "--cloud-provider",
            "gcp",
        ],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        {
            "connection_url": "neo4j+s://some-url",
            "id": "4k23f9n",
            "password": "qweasd",
            "tenant_id": "123",
            "username": "neo4j",
            "cloud_provider": "gcp",
        }
    )

    api_request.assert_called_once_with(
        "POST",
        "https://api.neo4j.io/v1/instances",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        data=json.dumps(
            {
                "version": "5",
                "region": "europe-west1",
                "memory": "2GB",
                "name": "TestInstance",
                "type": "professional-db",
                "tenant_id": "123",
                "cloud_provider": "gcp",
            }
        ),
    )


def test_create_instance_with_memory(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(
        create_instance,
        [
            "--name",
            "TestInstance",
            "--type",
            "professional-db",
            "--region",
            "europe-west1",
            "--tenant-id",
            "123",
            "--memory",
            "8",
            "--cloud-provider",
            "gcp",
        ],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        {
            "connection_url": "neo4j+s://some-url",
            "id": "4k23f9n",
            "password": "qweasd",
            "tenant_id": "123",
            "username": "neo4j",
            "cloud_provider": "gcp",
        }
    )

    api_request.assert_called_once_with(
        "POST",
        "https://api.neo4j.io/v1/instances",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        data=json.dumps(
            {
                "version": "5",
                "region": "europe-west1",
                "memory": "8GB",
                "name": "TestInstance",
                "type": "professional-db",
                "tenant_id": "123",
                "cloud_provider": "gcp",
            }
        ),
    )


def test_create_instance_with_version(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(
        create_instance,
        [
            "--name",
            "TestInstance",
            "--type",
            "professional-db",
            "--region",
            "europe-west1",
            "--tenant-id",
            "123",
            "--version",
            "4",
            "--cloud-provider",
            "gcp",
        ],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        {
            "connection_url": "neo4j+s://some-url",
            "id": "4k23f9n",
            "password": "qweasd",
            "tenant_id": "123",
            "username": "neo4j",
            "cloud_provider": "gcp",
        }
    )

    api_request.assert_called_once_with(
        "POST",
        "https://api.neo4j.io/v1/instances",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        data=json.dumps(
            {
                "version": "4",
                "region": "europe-west1",
                "memory": "2GB",
                "name": "TestInstance",
                "type": "professional-db",
                "tenant_id": "123",
                "cloud_provider": "gcp",
            }
        ),
    )
