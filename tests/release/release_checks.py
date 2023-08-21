import os
import subprocess

# TODO Need to run this in Docker container?


def run_cli_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command '{' '.join(command)}' failed: {result.stderr}")
    return result.stdout


def run_release_checks():
    # TODO Also get URLs from ENV Vars (once the feature is implemented)

    client_id = os.environ.get("AURA_CLI_RELEASE_CHECKS_CLIENT_ID")
    if not client_id:
        raise Exception("No Client Id provided.")

    client_secret = os.environ.get("AURA_CLI_RELEASE_CHECKS_CLIENT_SECRET")
    if not client_secret:
        raise Exception("No Client Secret provided.")

    # TODO set credentials, confirm config file format
    # TODO list, get tenant
    # TODO create DBs and test list
    # TODO DB one: create, rename, pause, resume, delete
    # TODO DB two: create, resize
    # TODO DB DS: create, resize, delete
    # TODO DB 3: create, list snaps, create snap, get snap, restore snap, delete
    # TODO 4: Create 2 DBs and overwrite instance

    # TODO set default tenant and do some checks
    # TODO set default output and do some gets requests

    # TODO cleanup


if __name__ == "__main__":
    run_release_checks()
