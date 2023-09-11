import json
import os
import sys

from aura.error_handler import (
    CredentialsAlreadyExist,
    CredentialsNotFound,
    InvalidConfigFile,
    UnsupportedConfigFileVersion,
    handle_error,
)
from aura.logger import get_logger, setup_logger
from aura.token_repository import delete_token_file
from aura.version import __version__


class CLIConfig:
    """
    Class which handles configurations of the CLI.
    The CLI's configuration is saved locally as a json file.
    This class handles loading, validatinf and updating this config.
    """

    DEFAULT_AURA_CONFIG_PATH = "~/.aura/config.json"
    DEFAULT_LOG_FILE_PATH = "~/.aura/auracli.log"
    DEFAULT_CONFIG = {
        "VERSION": __version__,
        "AUTH": {"CREDENTIALS": {}, "ACTIVE": None},
        "OPTIONS": {},
    }
    DEFAULT_BASE_URL = "https://api.neo4j.io/v1"
    DEFAULT_AUTH_URL = "https://api.neo4j.io/oauth/token"

    def __init__(self):
        self.logger = None
        self.config_path = os.environ.get("AURA_CLI_CONFIG_PATH", None) or os.path.expanduser(
            self.DEFAULT_AURA_CONFIG_PATH
        )
        self.config = self.load_config()
        self.env = self.load_env()

        self.logger = setup_logger(
            self.env["verbose"], self.env["save_logs"], self.env["log_file_path"]
        )
        self.logger.debug(f"CLI initiated. Version {__version__}")
        self.logger.debug("CLI command called: aura " + " ".join(sys.argv[1:]))
        self.logger.debug("User configuration loaded from " + self.config_path)

    def load_env(self):
        env = {}
        env["base_url"] = (
            os.environ.get("AURA_CLI_BASE_URL")
            or self.get_option("base_url")
            or self.DEFAULT_BASE_URL
        )
        env["auth_url"] = (
            os.environ.get("AURA_CLI_AUTH_URL")
            or self.get_option("auth_url")
            or self.DEFAULT_AUTH_URL
        )
        env["output"] = os.environ.get("AURA_CLI_OUTPUT") or self.get_option("output") or "json"
        env["default_tenant"] = (
            os.environ.get("AURA_CLI_DEFAULT_TENANT") or self.get_option("default_tenant") or None
        )
        env["config_path"] = self.config_path

        if os.environ.get("AURA_CLI_SAVE_LOGS") is not None:
            env["save_logs"] = os.environ.get("AURA_CLI_SAVE_LOGS", "").lower() in {
                "yes",
                "y",
                "true",
                "1",
            }
        elif self.get_option("save_logs") is not None:
            env["save_logs"] = self.get_option("save_logs").lower() in {"yes", "y", "true", "1"}
        else:
            env["save_logs"] = False

        env["log_file_path"] = (
            os.environ.get("AURA_CLI_LOG_FILE_PATH")
            or self.get_option("log_file_path")
            or os.path.expanduser(self.DEFAULT_LOG_FILE_PATH)
        )
        # The verbose flag is supposed to be global but click does not allow checking
        # all nested subcommands and options at this level. So we manually check if the
        # flag was set at any level.
        env["verbose"] = "--verbose" in sys.argv

        return env

    def load_config(self) -> dict:
        try:
            with open(self.config_path, "r", encoding="utf-8") as configfile:
                config = json.load(configfile)
        except (FileNotFoundError, json.JSONDecodeError):
            config = self.write_config(self.DEFAULT_CONFIG)
            return config

        try:
            self.validate_config(config)
        except Exception as e:
            handle_error(e)

        return config

    def write_config(self, config: dict):
        if self.logger:
            self.logger.debug("Updating user configuration at " + self.config_path)

        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        with open(self.config_path, "w", encoding="utf-8") as configfile:
            json.dump(config, configfile)

        return config

    def list_credentials(self):
        credentials = self.config["AUTH"].get("CREDENTIALS")
        return [{"Name": c, "ClientId": credentials[c]["CLIENT_ID"]} for c in credentials.keys()]

    def add_credentials(self, name: str, client_id: str, client_secret: str, use: bool):
        if self.config["AUTH"]["CREDENTIALS"].get(name, None) is not None:
            raise CredentialsAlreadyExist(name)

        self.config["AUTH"]["CREDENTIALS"][name] = {
            "CLIENT_ID": client_id,
            "CLIENT_SECRET": client_secret,
        }

        use_credentials = use or len(self.config["AUTH"]["CREDENTIALS"]) == 1

        if use_credentials:
            self.config["AUTH"]["ACTIVE"] = name
            # Delete saved auth token if it exists
            delete_token_file()

        self.write_config(self.config)

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

        # For outdated config files we will throw an error
        # Throwing such an error is bad user experience and should absolutely be avoided,
        # however we will keep the option for now, while backward compatibility is not required.
        # The current threshold is version 0.4.0
        if not "VERSION" in config:
            raise UnsupportedConfigFileVersion(self.config_path)
        version_list = config["VERSION"].split(".")
        if int(version_list[0]) == 0 and int(version_list[1]) < 4:
            raise UnsupportedConfigFileVersion(self.config_path)

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
        defaults = config.get("OPTIONS")
        if defaults is None:
            self.config["OPTIONS"] = {}
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
        self.config["OPTIONS"][name] = value
        self.write_config(self.config)

    def unset_option(self, name: str):
        if self.config["OPTIONS"].get(name):
            del self.config["OPTIONS"][name]

        self.write_config(self.config)

    def get_option(self, name: str):
        return self.config["OPTIONS"].get(name)

    def list_options(self):
        values = []
        defaults = self.config["OPTIONS"]
        for option in defaults:
            values.append({"Option": option, "Value": defaults[option]})

        return values
