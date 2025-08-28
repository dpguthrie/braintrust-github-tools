"""
GitHub List Issues Tool for Braintrust

This tool lists issues from a specific repository.
Works with repository information from search or details tools.
"""

import os
from typing import List, Optional

import braintrust
import requests
from pydantic import BaseModel


class ListIssuesParams(BaseModel):
    owner: str
    repo: str
    state: Optional[str] = "open"  # open, closed, all
    labels: Optional[str] = None  # comma-separated list
    sort: Optional[str] = "created"  # created, updated, comments
    direction: Optional[str] = "desc"  # asc, desc
    since: Optional[str] = None  # ISO 8601 format
    per_page: Optional[int] = 30  # max 100
    page: Optional[int] = 1


class IssueUser(BaseModel):
    login: str
    id: int
    avatar_url: str
    html_url: str


class IssueLabel(BaseModel):
    id: int
    name: str
    color: str
    description: Optional[str]


class Issue(BaseModel):
    id: int
    number: int
    title: str
    user: IssueUser
    labels: List[IssueLabel]
    state: str
    assignee: Optional[IssueUser]
    assignees: List[IssueUser]
    milestone: Optional[dict]
    comments: int
    created_at: str
    updated_at: str
    closed_at: Optional[str]
    body: Optional[str]
    html_url: str
    pull_request: Optional[dict]  # Present if this is a PR


class ListIssuesResponse(BaseModel):
    issues: List[Issue]
    total_count: int


def list_issues_handler(
    owner: str,
    repo: str,
    state: str = "open",
    labels: str | None = None,
    sort: str = "created",
    direction: str = "desc",
    since: str | None = None,
    per_page: int = 30,
    page: int = 1,
):
    """List repository issues using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    # Build query parameters
    query_params = {
        "state": state,
        "sort": sort,
        "direction": direction,
        "per_page": per_page,
        "page": page,
    }

    if labels:
        query_params["labels"] = labels
    if since:
        query_params["since"] = since

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

list_issues = project.tools.create(
    name="List Repository Issues",
    slug="list-issues",
    description="""
    List issues from a GitHub repository with filtering options.
    
    Use this tool after getting repository information to explore issues.
    
    Filter options:
    - state: open, closed, or all issues
    - labels: filter by specific labels (comma-separated)
    - sort: order by created, updated, or comments
    - since: only issues updated after this date
    
    The output includes issue details that can help understand:
    - What problems the repository is solving
    - Community engagement level
    - Areas needing attention
    
    Use individual issue numbers with other tools for detailed analysis.
    """,
    handler=list_issues_handler,
    parameters=ListIssuesParams,
    if_exists="replace",
)
