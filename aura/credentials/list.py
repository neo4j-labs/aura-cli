import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import handle_error
from aura.format import format_text_output


@click.command(name="list", help="List all configured OAuth client credentials")
@pass_config
def list_credentials(config: CLIConfig):
    """
    List all configured credentials
    """
    try:
        credentials = config.list_credentials()
        current_creds, _ = config.current_credentials()
    except Exception as exception:
        handle_error(exception)

    if not credentials:
        return click.echo("No credentials have been added yet.")

    output = []
    for creds in credentials:
        if creds["Name"] == current_creds:
            output.append({**creds, "Current": "   X   "})
        else:
            output.append({**creds, "Current": ""})

    out = format_text_output(output)
    print(out)
