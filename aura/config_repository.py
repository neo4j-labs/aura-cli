import json
import os
from aura.error_handler import (
    CredentialsAlreadyExist,
    CredentialsNotFound,
    InvalidConfigFile,
)

from aura.token_repository import delete_token_file


class CLIConfig:
    AURA_CONFIG_PATH = "~/.aura/config.json"
    DEFAULT_CONFIG = {"AUTH": {"CREDENTIALS": {}, "ACTIVE": None}, "DEFAULTS": {}}

    def __init__(self):
        self.config_path = os.path.expanduser(self.AURA_CONFIG_PATH)
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, "r") as configfile:
                config = json.load(configfile)
        except FileNotFoundError:
            return self.write_config(self.DEFAULT_CONFIG)
        else:
            self.validate_config(config)
            return config

    def write_config(self, config):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        with open(self.config_path, "w") as configfile:
            json.dump(config, configfile)

        return config

    def list_credentials(self):
        credentials = self.config["AUTH"].get("CREDENTIALS")
        return [{"Name": c, "ClientId": credentials[c]["CLIENT_ID"]} for c in credentials.keys()]

    def add_credentials(self, name, client_id, client_secret):
        if self.config["AUTH"]["CREDENTIALS"].get(name, None) is not None:
            raise CredentialsAlreadyExist(f"Credentials with name {name} already exist.")

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

    def delete_credentials(self, name):
        if name in self.config["AUTH"]["CREDENTIALS"]:
            del self.config["AUTH"]["CREDENTIALS"][name]
            if self.config["AUTH"]["ACTIVE"] == name:
                self.config["AUTH"]["ACTIVE"] = None
            self.write_config(self.config)
        else:
            raise CredentialsNotFound(f"Credentials {name} not found")

    def use_credentials(self, name):
        if name in self.config["AUTH"]["CREDENTIALS"]:
            self.config["AUTH"]["ACTIVE"] = name
            self.write_config(self.config)

            # Delete saved auth token if it exists
            delete_token_file()
        else:
            raise CredentialsNotFound(f"Credentials {name} not found")

    def validate_config(self, config):
        if not isinstance(config, dict):
            raise InvalidConfigFile("Config file has an invalid type")

        # Validate Auth section
        auth = config.get("AUTH")
        if not isinstance(auth, dict):
            raise InvalidConfigFile("Malformed config file")

        credentials = auth.get("CREDENTIALS")
        if not isinstance(credentials, dict):
            raise InvalidConfigFile("Malformed config file")

        for _, cred in credentials.items():
            if not isinstance(cred, dict):
                raise InvalidConfigFile("Malformed config file")

            if "CLIENT_ID" not in cred or not isinstance(cred["CLIENT_ID"], str):
                raise InvalidConfigFile("Malformed config file")

            if "CLIENT_SECRET" not in cred or not isinstance(cred["CLIENT_SECRET"], str):
                raise InvalidConfigFile("Malformed config file")

        active = auth.get("ACTIVE")
        if active is not None and (not isinstance(active, str) or active not in credentials):
            raise InvalidConfigFile("Malformed config file")

        # Validate Defaults section
        defaults = config.get("DEFAULTS")
        if defaults is None:
            self.config["DEFAULTS"] = {}
            self.write_config(self.config)
        else:
            if not isinstance(defaults, dict):
                raise InvalidConfigFile("Malformed config file")

            for option, default in defaults.items():
                if not isinstance(option, str):
                    raise InvalidConfigFile("Malformed config file")

                if not isinstance(default, str):
                    raise InvalidConfigFile("Malformed config file")

    def set_option(self, name, value):
        self.config["DEFAULTS"][name] = value
        self.write_config(self.config)

    def unset_option(self, name):
        if self.config["DEFAULTS"].get(name):
            del self.config["DEFAULTS"][name]

        self.write_config(self.config)

    def get_option(self, name):
        if value := self.config["DEFAULTS"].get(name):
            return value

    def list_options(self):
        values = []
        defaults = self.config["DEFAULTS"]
        for option in defaults:
            values.append({"Option": option, "Value": defaults[option]})

        return values
