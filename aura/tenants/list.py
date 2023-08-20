from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command(name="list", help_text="List all tenants for current user")
def list_tenants():
    """
    List tenants a user belongs to.

    Makes "GET /tenants" API request.
    """

    path = "/tenants"

    return make_api_call("GET", path)
