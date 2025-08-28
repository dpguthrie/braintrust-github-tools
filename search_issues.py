"""
GitHub Search Issues Tool for Braintrust

This tool searches for issues across GitHub repositories.
More powerful than listing issues from a single repo.
"""

import os
from typing import List, Optional

import braintrust
import requests
from pydantic import BaseModel


class SearchIssuesParams(BaseModel):
    query: str
    sort: Optional[str] = "created"  # created, updated, comments
    order: Optional[str] = "desc"  # asc, desc
    per_page: Optional[int] = 30  # max 100
    page: Optional[int] = 1


class SearchIssueUser(BaseModel):
    login: str
    id: int
    avatar_url: str
    html_url: str


class SearchIssueLabel(BaseModel):
    id: int
    name: str
    color: str
    description: Optional[str]


class SearchIssue(BaseModel):
    id: int
    number: int
    title: str
    user: SearchIssueUser
    labels: List[SearchIssueLabel]
    state: str
    assignee: Optional[SearchIssueUser]
    assignees: List[SearchIssueUser]
    milestone: Optional[dict]
    comments: int
    created_at: str
    updated_at: str
    closed_at: Optional[str]
    body: Optional[str]
    html_url: str
    repository_url: str
    score: float  # Search relevance score
    pull_request: Optional[dict]  # Present if this is a PR


class SearchIssuesResponse(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[SearchIssue]


def search_issues_handler(
    query: str,
    sort: str = "created",
    order: str = "desc",
    per_page: int = 30,
    page: int = 1,
):
    """Search for issues using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the search URL
    url = "https://api.github.com/search/issues"

    query_params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": per_page,
        "page": page,
    }

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

search_issues = project.tools.create(
    name="Search GitHub Issues",
    slug="search-issues",
    description="""
    Search for issues across GitHub repositories using powerful query syntax.
    
    Query examples:
    - "is:open label:bug" - Open issues with bug label
    - "is:closed author:username" - Closed issues by specific author
    - "repo:owner/repo state:open" - Open issues in specific repo
    - "assignee:username" - Issues assigned to specific user
    - "milestone:v1.0" - Issues in specific milestone
    - "created:>2023-01-01" - Issues created after date
    - "language:python type:issue" - Issues in Python repositories
    - "involves:username" - Issues involving specific user
    
    More powerful than listing issues from a single repository.
    Results include repository context and can guide further exploration.
    """,
    handler=search_issues_handler,
    parameters=SearchIssuesParams,
    if_exists="replace",
)
