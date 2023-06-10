from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command(help="List all tenants for current user")
def list():
    path = "/tenants"

    return make_api_call("GET", path)