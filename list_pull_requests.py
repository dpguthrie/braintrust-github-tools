"""
GitHub List Pull Requests Tool for Braintrust

This tool lists pull requests from a specific repository.
Works with repository information from search or details tools.
"""

import os
from typing import List, Optional

import braintrust
import requests
from pydantic import BaseModel


class ListPullRequestsParams(BaseModel):
    owner: str
    repo: str
    state: Optional[str] = "open"  # open, closed, all
    head: Optional[str] = None  # Filter by head branch
    base: Optional[str] = None  # Filter by base branch
    sort: Optional[str] = "created"  # created, updated, popularity
    direction: Optional[str] = "desc"  # asc, desc
    per_page: Optional[int] = 30  # max 100
    page: Optional[int] = 1


class PullRequestUser(BaseModel):
    login: str
    id: int
    avatar_url: str
    html_url: str


class PullRequestBranch(BaseModel):
    label: str
    ref: str
    sha: str
    user: PullRequestUser
    repo: Optional[dict]


class PullRequestLabel(BaseModel):
    id: int
    name: str
    color: str
    description: Optional[str]


class PullRequest(BaseModel):
    id: int
    number: int
    title: str
    user: PullRequestUser
    labels: List[PullRequestLabel]
    state: str
    locked: bool
    assignee: Optional[PullRequestUser]
    assignees: List[PullRequestUser]
    milestone: Optional[dict]
    comments: int
    review_comments: int
    maintainer_can_modify: bool
    commits: int
    additions: int
    deletions: int
    changed_files: int
    created_at: str
    updated_at: str
    closed_at: Optional[str]
    merged_at: Optional[str]
    merge_commit_sha: Optional[str]
    draft: bool
    head: PullRequestBranch
    base: PullRequestBranch
    body: Optional[str]
    html_url: str
    diff_url: str
    patch_url: str


class ListPullRequestsResponse(BaseModel):
    pull_requests: List[PullRequest]
    total_count: int


def list_pull_requests_handler(
    owner: str,
    repo: str,
    state: str = "open",
    head: str | None = None,
    base: str | None = None,
    sort: str = "created",
    direction: str = "desc",
    per_page: int = 30,
    page: int = 1,
):
    """List repository pull requests using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    # Build query parameters
    query_params = {
        "state": state,
        "sort": sort,
        "direction": direction,
        "per_page": per_page,
        "page": page,
    }

    if head:
        query_params["head"] = head
    if base:
        query_params["base"] = base

    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()

        # Return the raw JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"GitHub API request failed: {str(e)}")
    except KeyError as e:
        raise Exception(f"Unexpected response format: {str(e)}")


project = braintrust.projects.create(name="github-tools")

list_pull_requests = project.tools.create(
    name="List Repository Pull Requests",
    slug="list-pull-requests",
    description="""
    List pull requests from a GitHub repository with filtering options.
    
    Use this tool after getting repository information to explore PRs.
    
    Filter options:
    - state: open, closed, or all pull requests
    - head: filter by head branch (e.g., "feature-branch")
    - base: filter by base branch (e.g., "main", "develop")
    - sort: order by created, updated, or popularity
    
    The output includes PR details that help understand:
    - Active development work
    - Code review process
    - Contribution patterns
    - Branch strategies
    
    Use individual PR numbers for detailed analysis of changes.
    """,
    handler=list_pull_requests_handler,
    parameters=ListPullRequestsParams,
    if_exists="replace",
)
