import os
import re
from configparser import ConfigParser
from copy import deepcopy
from typing import Any
from .core import ConfigService

import yaml



class IniConfigService(ConfigService):
    """Credentials are stored in a confi.ini file."""

    def __init__(self, filename: str):
        self._config = ConfigParser()
        with open(filename, "r") as f:
            self._config.read_file(f)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            values = key.split(".")
            if len(values) == 1:
                return default
            section, key = values
            return self._config[section][key]
        except KeyError:
            return default
        except ValueError:
            return default


class OsEnvironmentConfigService(ConfigService):
    """Service values from keys inside os environment."""

    def get(self, key: str, default=None):
        """Return value of key or default if not found."""
        value = os.environ.get(key)
        if value:
            return value

        return default


class EnvironmentIniConfigService(ConfigService):
    """Ini file with one section for each environment."""

    def __init__(self, filename: str, environment: str = "devel"):
        config = ConfigParser()
        config.optionxform = str
        self._env = environment
        with open(filename, "r") as f:
            config.read_file(f)
        self._parameters = self._load_parameters(config)

    def _load_parameters(self, config):
        parameters = {}

        for section in ("prod", "pre", "devel"):
            for key in config.options(section):
                parameters[key] = config.get(section, key)
            if self._env == section:
                break

        return parameters

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value of a parameter otherwise default."""
        try:
            return self._parameters[key]
        except KeyError:
            return default
        except ValueError:
            return default


class YamlConfigService(ConfigService):
    """Configuration service using yaml file."""

    def __init__(self, filename: str):
        self._config = {}
        with open(filename, "r") as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return the value of a parameter by its key, None if is not found."""
        return self._config.get(key, default)


class ComposedConfigService(ConfigService):
    """Combine several config service in only one."""

    def __init__(self, *config_services: ConfigService):
        self._services = config_services

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return value of key in any of the injected service configs."""
        for service in self._services:
            value = service.get(key)
            if value:
                if type(value) is dict or type(value) is list:
                    return deepcopy(value)

                return value

        return default


class ConfigMapService(ConfigService):
    """Kubernetes ConfigMap item implementing a ConfigService."""

    def __init__(self, volume: str):
        self._volume = volume

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return value of any variable."""
        try:
            with open(os.path.join(self._volume, key), "r") as f:
                return f.read()
        except FileNotFoundError:
            return default


class InterpolationConfigService(ConfigService):
    """Service with capacity of interpolation in variables."""

    _pattern = re.compile(r"\$\{(.+?)\}")

    def __init__(self, config_service: ConfigService):
        self._config = config_service

    def get(self, key: str, default: Any | None = None) -> Any:
        """Return value, if there are variables, they will be replaced."""
        value = self._config.get(key)
        if value is None:
            return default

        return self._construct_value(value)

    def _construct_value(self, value: Any):
        if type(value) is dict:
            result = {}
            for key, value_ in value.items():
                result[key] = self._construct_value(value_)
            return result

        if type(value) is str:
            if not self._pattern.search(value):
                return value

            value = self._pattern.sub(self._replacement, value)
            if value == "":
                return
            return value

        return value

    def _replacement(self, match):
        key = match.group(1)
        if self.get(key) is not None:
            return str(self.get(key))
