from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum, auto
import tomllib
from typing import Any, Optional, Type
import sys

DEFAULT_CONFIG_PATH = "/etc/velox-search.conf.toml"


class ConfigLoader:
    """
    Abstract class only used for typing
    """

    @staticmethod
    @abstractmethod
    def load(data: dict[str, Any]) -> Any:
        raise NotImplementedError


@dataclass
class LoggingConfig(ConfigLoader):
    level: str

    @staticmethod
    def load(data: dict[str, Any]) -> "LoggingConfig":
        valid_levels = ["debug", "info", "warning", "error", "critical"]

        if not isinstance(data.get("level"), str):
            raise ValueError("Missing or invalid value logging.level")

        level = data["level"].lower()
        if not level in valid_levels:
            raise ValueError(
                f"Invalid logging.level `{level}`. Valid levels are: {', '.join(valid_levels)}"
            )

        return LoggingConfig(level=level)


class SearchAlgorithm(StrEnum):
    Naive = auto()
    Bisect = auto()
    Tree = auto()
    BisectTree = auto()


@dataclass
class HttpServerConfig(ConfigLoader):
    listen_addr: str
    listen_port: int

    @staticmethod
    def load(data: dict[str, Any]) -> "HttpServerConfig":
        if not isinstance(data.get("listen_addr"), str):
            raise ValueError("Missing or invalid value http_server.listen_addr")

        if not isinstance(data.get("listen_port"), int):
            raise ValueError("Missing or invalid value http_server.listen_port")

        return HttpServerConfig(
            listen_addr=data["listen_addr"], listen_port=data["listen_port"]
        )


@dataclass
class SearchConfig(ConfigLoader):
    wordlist: str
    algorithm: SearchAlgorithm

    @staticmethod
    def load(data: dict[str, Any]) -> "SearchConfig":
        if not isinstance(data.get("wordlist"), str):
            raise ValueError("Missing or invalid value search.wordlist")

        if not isinstance(data.get("algorithm"), str):
            raise ValueError("Missing or invalid value search.algorithm")

        try:
            algorithm = SearchAlgorithm(data["algorithm"].lower())
        except:
            raise ValueError(
                f"Invalid search.algorithm `{data['algorithm']}`. Valid algorithms are: "
                f"{', '.join((algorithm.value for algorithm in SearchAlgorithm))}"
            )

        return SearchConfig(
            wordlist=data["wordlist"], algorithm=SearchAlgorithm(algorithm)
        )


@dataclass
class Config:
    http_server: HttpServerConfig
    search: SearchConfig
    logging: LoggingConfig

    @staticmethod
    def _load_file(config_file: str) -> "Config":
        with open(config_file, "rb") as fd:
            data = tomllib.load(fd)

            config_sections: dict[str, Type[ConfigLoader]] = {
                "http_server": HttpServerConfig,
                "search": SearchConfig,
                "logging": LoggingConfig,
            }

            config_dict: dict[str, Any] = {}
            for name, class_handler in config_sections.items():
                if data.get(name) is None:
                    raise ValueError(f"Missing section [{name}]")

                if not isinstance(data[name], dict):
                    raise ValueError(f"Invalid section [{name}]")

                config_dict[name] = class_handler.load(data[name])

        return Config(**config_dict)

    @staticmethod
    def load(file: Optional[str]) -> "Config":
        # Config files to be loaded, sorted by "try" order
        # The first existing config file is used, following files are ignored
        config_files = [file] if file is not None else []
        config_files.append(
            DEFAULT_CONFIG_PATH,
        )

        for config_file in config_files:
            try:
                return Config._load_file(config_file)
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"Failed to load config file {config_file}: {e}", file=sys.stderr)
                raise

        raise ValueError(
            f"Could not find any configuration file. Tried {', '.join(config_files)}"
        )
