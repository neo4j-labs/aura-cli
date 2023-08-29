import json
import os

from aura.error_handler import (
    CredentialsAlreadyExist,
    CredentialsNotFound,
    InvalidConfigFile,
)
from aura.token_repository import delete_token_file
from aura.version import __version__


class CLIConfig:
    """
    Class which handles configurations of the CLI.
    The CLI's configuration is saved locally as a json file.
    This class handles loading, validatinf and updating this config.
    """

    AURA_CONFIG_PATH = "~/.aura/config.json"
    DEFAULT_CONFIG = {
        "VERSION": __version__,
        "AUTH": {"CREDENTIALS": {}, "ACTIVE": None},
        "DEFAULTS": {},
    }

    def __init__(self):
        self.config_path = os.path.expanduser(self.AURA_CONFIG_PATH)
        self.config = self.load_config()

    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r", encoding="utf-8") as configfile:
                config = json.load(configfile)
        except FileNotFoundError:
            config = self.write_config(self.DEFAULT_CONFIG)
            return config

        self.validate_config(config)
        return config

    def write_config(self, config: dict):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        with open(self.config_path, "w", encoding="utf-8") as configfile:
            json.dump(config, configfile)

        return config

    def list_credentials(self):
        credentials = self.config["AUTH"].get("CREDENTIALS")
        return [{"Name": c, "ClientId": credentials[c]["CLIENT_ID"]} for c in credentials.keys()]

    def add_credentials(self, name: str, client_id: str, client_secret: str):
        if self.config["AUTH"]["CREDENTIALS"].get(name, None) is not None:
            raise CredentialsAlreadyExist(name)

        self.config["AUTH"]["CREDENTIALS"][name] = {
            "CLIENT_ID": client_id,
            "CLIENT_SECRET": client_secret,
        }
        self.config["AUTH"]["ACTIVE"] = name

        self.write_config(self.config)

        # Delete saved auth token if it exists
        delete_token_file()

    def current_credentials(self):
        active = self.config["AUTH"].get("ACTIVE")
        if active is None:
            return None, None

        return active, self.config["AUTH"]["CREDENTIALS"][active]

    def delete_credentials(self, name: str):
        if name in self.config["AUTH"]["CREDENTIALS"]:
            del self.config["AUTH"]["CREDENTIALS"][name]
            if self.config["AUTH"]["ACTIVE"] == name:
                self.config["AUTH"]["ACTIVE"] = None
                delete_token_file()
            self.write_config(self.config)
        else:
            raise CredentialsNotFound(name)

    def use_credentials(self, name: str):
        if name in self.config["AUTH"]["CREDENTIALS"]:
            self.config["AUTH"]["ACTIVE"] = name
            self.write_config(self.config)

            # Delete saved auth token if it exists
            delete_token_file()
        else:
            raise CredentialsNotFound(name)

    def validate_config(self, config: dict):
        if not isinstance(config, dict):
            raise InvalidConfigFile()

        # Validate Auth section
        auth = config.get("AUTH")
        if not isinstance(auth, dict):
            raise InvalidConfigFile()

        credentials = auth.get("CREDENTIALS")
        if not isinstance(credentials, dict):
            raise InvalidConfigFile()

        for _, cred in credentials.items():
            if not isinstance(cred, dict):
                raise InvalidConfigFile()

            if "CLIENT_ID" not in cred or not isinstance(cred["CLIENT_ID"], str):
                raise InvalidConfigFile()

            if "CLIENT_SECRET" not in cred or not isinstance(cred["CLIENT_SECRET"], str):
                raise InvalidConfigFile()

        active = auth.get("ACTIVE")
        if active is not None and (not isinstance(active, str) or active not in credentials):
            raise InvalidConfigFile()

        # Validate Defaults section
        defaults = config.get("DEFAULTS")
        if defaults is None:
            self.config["DEFAULTS"] = {}
            self.write_config(self.config)
        else:
            if not isinstance(defaults, dict):
                raise InvalidConfigFile()

            for option, default in defaults.items():
                if not isinstance(option, str):
                    raise InvalidConfigFile()

                if not isinstance(default, str):
                    raise InvalidConfigFile()

    def set_option(self, name: str, value: str):
        self.config["DEFAULTS"][name] = value
        self.write_config(self.config)

    def unset_option(self, name: str):
        if self.config["DEFAULTS"].get(name):
            del self.config["DEFAULTS"][name]

        self.write_config(self.config)

    def get_option(self, name: str):
        return self.config["DEFAULTS"].get(name)

    def list_options(self):
        values = []
        defaults = self.config["DEFAULTS"]
        for option in defaults:
            values.append({"Option": option, "Value": defaults[option]})

        return values
