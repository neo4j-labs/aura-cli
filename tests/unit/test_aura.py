from unittest.mock import MagicMock
from aura.aura import cli


def test_cli_has_commands():
    registered_commands = [cmd for cmd in cli.list_commands(ctx=MagicMock())]
    assert "credentials" in registered_commands
    assert "instances" in registered_commands
    assert "snapshots" in registered_commands
    assert "tenants" in registered_commands
    assert "config" in registered_commands
