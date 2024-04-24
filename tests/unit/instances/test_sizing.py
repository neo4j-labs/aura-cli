import pytest
from click.testing import CliRunner
from unittest.mock import Mock
import json

from aura.instances import size_instance
from unit.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
	    "data": {
		"did_exceed_maximum": False,
		"min_required_memory": "1GB",
		"recommended_size": "8GB",
	    }
    }

    return mock_res


def test_size_instance(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(
        size_instance,
        [
            "--type",
            "enterprise-ds",
            "--node-count",
            "42",
            "--relationship-count",
            "1337",
            "--algorithm-categories",
            "centrality",
            "--algorithm-categories",
            "node-embeddings",
        ],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        {
		    "did_exceed_maximum": False,
		    "min_required_memory": "1GB",
		    "recommended_size": "8GB"
        }
    )

    api_request.assert_called_once_with(
        "POST",
        "https://api.neo4j.io/v1/instances/sizing",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        data=json.dumps(
            {
        "node_count": 42,
        "relationship_count": 1337,
        "algorithm_categories": ["centrality", "node-embeddings"],
        "instance_type": "enterprise-ds",
            }
        ),
        timeout=10,
    )


def test_sizing_instance_without_ac(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(
        size_instance,
        [
            "--type",
            "enterprise-ds",
            "--node-count",
            "42",
            "--relationship-count",
            "1337",
        ],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        {
		    "did_exceed_maximum": False,
		    "min_required_memory": "1GB",
		    "recommended_size": "8GB"
        }
    )

    api_request.assert_called_once_with(
        "POST",
        "https://api.neo4j.io/v1/instances/sizing",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        data=json.dumps(
            {
        "node_count": 42,
        "relationship_count": 1337,
        "algorithm_categories": [],
        "instance_type": "enterprise-ds",
            }
        ),
        timeout=10,
    )