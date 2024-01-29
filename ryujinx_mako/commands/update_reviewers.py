from argparse import ArgumentParser, Namespace
from pathlib import Path
from github.PullRequest import PullRequest
from github.Repository import Repository
from github.GithubException import GithubException

import yaml

from ryujinx_mako.commands._subcommand import GithubSubcommand


class UpdateReviewers(GithubSubcommand):
    @staticmethod
    def name() -> str:
        return "update-reviewers"

    @staticmethod
    def description() -> str:
        return "Update reviewers for the specified PR"

    @staticmethod
    def get_existing_reviews(pull_request: PullRequest) -> set[str]:
        existing = set()

        requested_users, requested_teams = pull_request.get_review_requests()
        for user in requested_users:
            existing.add(user.login)
        for team in requested_teams:
            existing.add(f"@{team.slug}")

        for review in pull_request.get_reviews():
            existing.add(review.user.login)

        return existing

    def __init__(self, parser: ArgumentParser):
        self._reviewers = set()
        self._team_reviewers = set()

        parser.add_argument(
            "repo_path",
            type=str,
            help="full name of the GitHub repository (format: OWNER/REPO)",
        )
        parser.add_argument(
            "pr_number", type=int, help="the number of the pull request to check"
        )
        parser.add_argument(
            "config_path",
            type=Path,
            help="the path to the reviewers config file",
        )

        super().__init__(parser)

    @property
    def reviewers_lower(self) -> list[str]:
        return [x.lower() for x in self._reviewers]

    def _remove_reviewer(self, reviewer: str):
        reviewer_element = None
        if reviewer.startswith("@"):
            reviewer_lower = reviewer.lower()[1:]
            reviewers_list = self._team_reviewers
        else:
            reviewer_lower = reviewer.lower()
            reviewers_list = self._reviewers

        for element in reviewers_list:
            if element.lower() == reviewer_lower:
                reviewer_element = element
                break

        if not reviewer_element:
            raise KeyError(reviewer)

        reviewers_list.remove(reviewer_element)

    def add_reviewers(self, new_entries: list[str]):
        for reviewer in new_entries:
            if reviewer.startswith("@"):
                self._team_reviewers.add(reviewer[1:])
            else:
                self._reviewers.add(reviewer)

    def update_reviewers(self, config, repo: Repository, pr_number: int) -> int:
        pull_request = repo.get_pull(pr_number)

        if not pull_request:
            self.logger.error(f"Unknown PR #{pr_number}")
            return 1

        if pull_request.draft:
            self.logger.warning("Not assigning reviewers for draft PRs")
            return 0

        pull_request_author = pull_request.user.login

        for label in pull_request.labels:
            if label.name in config:
                self.add_reviewers(config[label.name])

        if "default" in config:
            self.add_reviewers(config["default"])

        if pull_request_author.lower() in self.reviewers_lower:
            self._remove_reviewer(pull_request_author)

        for existing_reviewer in self.get_existing_reviews(pull_request):
            if (
                existing_reviewer.startswith("@")
                and existing_reviewer[1:] in self._team_reviewers
            ) or (
                not existing_reviewer.startswith("@")
                and existing_reviewer.lower() in self.reviewers_lower
            ):
                self._remove_reviewer(existing_reviewer)

        try:
            reviewers = list(self._reviewers)
            team_reviewers = list(self._team_reviewers)

            if len(reviewers) == 0 and len(team_reviewers) == 0:
                self.logger.info("No new reviewers to assign.")
                return 0

            self.logger.info(
                f"Attempting to assign reviewers ({reviewers}) "
                f"and team_reviewers ({team_reviewers})"
            )
            pull_request.create_review_request(reviewers, team_reviewers)
            return 0
        except GithubException:
            self.logger.exception(f"Cannot assign review request for PR #{pr_number}")
            return 1

    def run(self, args: Namespace):
        repo = self.github.get_repo(args.repo_path)

        if not repo:
            self.logger.error("Repository not found!")
            exit(1)

        if not args.config_path.exists():
            self.logger.error(f"Config '{args.config_path}' not found!")
            exit(1)

        with open(args.config_path, "r") as file:
            config = yaml.safe_load(file)

        exit(self.update_reviewers(config, repo, args.pr_number))
