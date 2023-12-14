"""Git routines and tools."""
import re

import rich
import typer
from github import Auth, Github
from github.Commit import Commit
from github.Repository import Repository
from typer import Option
from typing_extensions import Annotated

from stability_matrix_tools.models.keyring_config import ConfigKey, KeyringConfig
from stability_matrix_tools.models.settings import env

app = typer.Typer(no_args_is_help=True)
cp = rich.print

ConfirmType = Annotated[bool, Option("--yes", "-y", help="Confirm")]


class GitContext:
    def __init__(self):
        """Initialize a new GitContext."""
        cfg = KeyringConfig.load_from_keyring()
        token = cfg.get_with_prompt(ConfigKey.GITHUB_TOKEN)

        self.gh = Github(auth=Auth.Token(token))
        self.gh_user = self.gh.get_user()

    def get_private_repo(self):
        return self.gh.get_repo(
            env.git_repo_private.removeprefix("https://github.com/"), lazy=True
        )

    def get_fork_repo(self):
        return self.gh.get_repo(
            env.git_repo_fork.removeprefix("https://github.com/"), lazy=True
        )

    def get_public_repo(self):
        return self.gh.get_repo(
            env.git_repo_public.removeprefix("https://github.com/"), lazy=True
        )

    def get_repo_from_url(self, url: str):
        result = re.match(r"(?:https?://github.com/)?(.+?)/(.+?)(?:\.git)?$", url)
        # Only get the first 2 groups
        owner, name = result.groups()[:2]
        return self.gh.get_repo(
            f"{owner}/{name}", lazy=True
        )

    @staticmethod
    def compare(base_repo: Repository, base: Commit, head_repo: Repository, head: Commit):
        head_part = f"{head_repo.owner.login}:{head_repo.name}:{head.sha}"
        return base_repo.compare(base.sha, head_part)


def format_repo(repo: str | Repository) -> str:
    """Format a repo for printing."""
    if isinstance(repo, Repository):
        return repo.url.removeprefix("https://github.com/")
    else:
        return repo.removeprefix("https://github.com/").strip("/")


@app.command()
def auth():
    """Test GitHub authentication."""
    ctx = GitContext()

    cp(f"Authenticated with GitHub as: {ctx.gh_user.login}")


def pr_merge_branch(repo_url: str, from_branch: str, to_branch: str):
    """Creates a PR to merge a repo's branch into another branch."""
    ctx = GitContext()

    repo = ctx.get_repo_from_url(repo_url)
    repo_str = format_repo(repo)

    source = repo.get_branch(from_branch)

    # create a new branch from private/main
    merge_branch_name = f"merge-{from_branch}-to-{to_branch}-{source.commit.sha[:7]}"
    repo.create_git_ref(
        ref=f"refs/heads/{merge_branch_name}",
        sha=source.commit.sha,
    )

    cp(f"Creating branch: {repo_str}/{merge_branch_name} from {repo_str}/{from_branch} @ {source.commit.sha[:7]}")
    cp(f"Creating PR: {repo_str}/{merge_branch_name} -> {repo_str}/{to_branch}")

    # create a PR from private/main to private/dev
    pr = repo.create_pull(
        title=f"Merge {from_branch} to {to_branch}",
        body="",
        base=to_branch,
        head=merge_branch_name,
    )

    cp(f"✅  Created PR: [cyan link={pr.url}]{pr.title} #{pr.number}[/cyan link]")


def pr_merge_repo(from_repo_url: str, from_branch_name: str, to_repo_url: str, to_branch_name: str):
    """Creates a PR to merge a repo's branch into another repo's branch."""
    ctx = GitContext()

    from_repo = ctx.get_repo_from_url(from_repo_url)
    from_repo_str = format_repo(from_repo)
    from_branch = from_repo.get_branch(from_branch_name)
    from_branch_str = f"{from_repo_str}:{from_branch_name}"

    to_repo = ctx.get_repo_from_url(to_repo_url)
    to_repo_str = format_repo(to_repo)
    to_branch = to_repo.get_branch(to_branch_name)
    to_branch_str = f"{to_repo_str}:{to_branch_name}"

    # create a new branch in target repo
    merge_branch_name = f"merge-{from_branch_str}-to-{to_branch_name}-{from_branch.commit.sha[:7]}"

    cp(f"Creating branch: {to_repo_str}:{merge_branch_name} from {to_repo_str}:{to_branch_name} "
       f"@ {to_branch.commit.sha[:7]}")

    to_repo.create_git_ref(
        ref=f"refs/heads/{merge_branch_name}",
        sha=to_branch.commit.sha,
    )

    # merge from_repo:from_branch into to_repo:merge_branch_name
    cp(f"Merging {from_branch_str} into {to_repo_str}:{merge_branch_name}")
    to_repo.merge(from_branch.commit.sha, merge_branch_name)

    # cp(f"Creating branch: {from_repo_str}/{merge_branch_name} from {from_repo_str}/{from_branch_name} @ {from_branch.commit.sha[:7]}")
    cp(f"Creating PR: {from_branch_str} -> {to_branch_str}")

    pr = to_repo.create_pull(
        title=f"Merge {from_branch_str} to {to_branch_str}",
        body="",
        base=to_branch_name,
        head=from_branch_str,
    )

    cp(f"✅  Created PR: [cyan link={pr.url}]{pr.title} #{pr.number}[/cyan link]")


@app.command()
def main_to_dev(repo_url: str):
    """Creates a PR to merge a repo's main branch into dev branch."""
    pr_merge_branch(repo_url, "main", "dev")


@app.command()
def dev_to_main(repo_url: str):
    """Creates a PR to merge a repo's main branch into dev branch."""
    pr_merge_branch(repo_url, "dev", "main")


@app.command()
def private_main_to_dev():
    """Creates a PR to merge private/main into private/dev."""
    main_to_dev(env.git_repo_private)


@app.command()
def private_dev_to_main():
    """Creates a PR to merge private/dev into private/main."""
    dev_to_main(env.git_repo_private)


@app.command()
def fork_to_private():
    """Creates a PR to merge fork/main into private/main."""
    pr_merge_repo(env.git_repo_fork, "main", env.git_repo_private, "main")
