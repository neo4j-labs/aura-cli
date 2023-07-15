import click
from aura.decorators import pass_config
from aura.error_handler import handle_error
from aura.format import format_text_output


@click.command(help="List all configured OAuth client credentials")
@pass_config
def list(config):
    try:
        credentials = config.list_credentials()
        current_creds, _ = config.current_credentials()
    except Exception as e:
        handle_error(e)

    if not credentials:
        return click.echo("No credentials have been added yet.")

    output = []
    for c in credentials:
        if c["Name"] == current_creds:
            output.append({**c, "Current": "   X   "})
        else:
            output.append({**c, "Current": ""})

    format_text_output(output)
