import os
from velox_search.config import (
    Config,
    HttpServerConfig,
    LoggingConfig,
    SearchAlgorithm,
    SearchConfig,
)


def get_config(wordlist: str, algorithm: SearchAlgorithm, limit: int) -> Config:
    return Config(
        http_server=HttpServerConfig(listen_addr="127.0.0.1", listen_port=10000),
        search=SearchConfig(
            wordlist=os.path.join(os.path.dirname(__file__), f"../data/{wordlist}"),
            algorithm=algorithm,
            limit=limit,
        ),
        logging=LoggingConfig(level="INFO"),
    )
