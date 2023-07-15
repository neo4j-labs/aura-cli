### How to run

In the root directory run `. venv/bin/activate` to active the virtual environment.

Next, run `pip install --editable .` to install the dependencies. Then you can run the cli `aura --help`.

When finished, run `deactivate` to deactivate the venv.

To run the unit tests, run `pytest tests/`.

For development you will need the following packages:
- `pytest`
- `black`
- `pylint`
- `pre-commit`
- `pytest-cov`

### Environment Variables

There are 4 environment variables that can be set for use in the CLI:

- `AURA_CLI_AUTH_URL` - The url used for getting an auth token (default to https://api.neo4j.io/oauth/token)
- `AURA_CLI_BASE_URL` - The base url used for all API calls (defaults to https://api.neo4j.io/v1beta3)
- `AURA_CLI_CLIENT_ID` - The client id used for authentication
- `AURA_CLI_CLIENT_SECRET` - The client secret used for authentication

`AURA_CLI_CLIENT_ID` and `AURA_CLI_CLIENT_SECRET` will override any configured credentials.

### Credentials

Aura API credentials need to be created in the console. These can then be added to the CLI through the `aura credentials add` command. The credentials will then be saved locally in a config file. You can add multiple credentials and switch between them. Here is a list of all credentials commands:

- `aura credentials add`
- `aura credentials list`
- `aura credentials current`
- `aura credentials use`
- `aura credentials delete`

Configured credentials will be overriden if environment variables for the Client ID or Client Secret are set.

### Config

The `aura config` commands allows to set configurations and default values. Currently there are 2 options which can be set with the `aura config set` command:

- `default-tenant` - the default tenant which to use for commands like `aura instances create` (where a tenant-id is required)
- `default-output` - the default output format for API commands (json, text or table)

List of all config commands:

- `aura config get`
- `aura config list`
- `aura config set`
- `aura config unset`

### API Commands

API commands are divided into 3 resources: `instance`, `tenants` and `snapshots`.

Example commands:

`aura instances get --name DevInstance`

`aura instances create --name DevInstance --region europe-west1 --type professional-db --tenant-id my-tenant-123`

`aura snapshots list --instance-id=d3kn20el`

### Output format

By default the output format is json. Using the `output` option the format can be changed to `table` or `text`, e.g.

`aura instances list --output table`

### Useful flags

All API commands have the following two flags:

- `--include, -i` : Print the API response headers
- `--raw` : Print the raw API response body
