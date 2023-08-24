import logging
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace

from github import Github
from github.Auth import AppAuth

from ryujinx_mako._const import APP_ID, PRIVATE_KEY, INSTALLATION_ID, SCRIPT_NAME


class Subcommand(ABC):
    @abstractmethod
    def __init__(self, parser: ArgumentParser):
        parser.set_defaults(func=self.run)

    @property
    def logger(self):
        return logging.getLogger(SCRIPT_NAME).getChild(
            type(self).name().replace("-", "_")
        )

    @abstractmethod
    def run(self, args: Namespace):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def name() -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def description() -> str:
        raise NotImplementedError()


class GithubSubcommand(Subcommand, ABC):
    _github = Github(
        auth=AppAuth(APP_ID, PRIVATE_KEY).get_installation_auth(INSTALLATION_ID)
    )

    @property
    def github(self):
        return type(self)._github
