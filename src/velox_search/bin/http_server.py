import sys
import argparse

from ..config import Config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file (in toml)")
    args = parser.parse_args()

    config = Config.load(args.config)

    print(config)

    sys.exit(0)
