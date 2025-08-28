"""
GitHub Repository Contributors Tool for Braintrust

This tool gets the list of contributors to a repository.
Useful for understanding project community and activity.
"""

import os
from typing import List, Optional

import braintrust
import requests
from pydantic import BaseModel


class RepositoryContributorsParams(BaseModel):
    owner: str
    repo: str
    anon: Optional[bool] = False  # Include anonymous contributors
    per_page: Optional[int] = 30  # max 100
    page: Optional[int] = 1


class Contributor(BaseModel):
    login: Optional[str]  # None for anonymous contributors
    id: Optional[int]
    avatar_url: str
    gravatar_id: Optional[str]
    url: Optional[str]
    html_url: Optional[str]
    followers_url: Optional[str]
    following_url: Optional[str]
    repos_url: Optional[str]
    type: Optional[str]  # "User" or None for anonymous
    site_admin: Optional[bool]
    contributions: int
    name: Optional[str]  # For anonymous contributors
    email: Optional[str]  # For anonymous contributors


class RepositoryContributorsResponse(BaseModel):
    contributors: List[Contributor]
    total_count: int
    repository: str


def get_repository_contributors_handler(
    owner: str, repo: str, anon: bool = False, per_page: int = 30, page: int = 1
):
    """Get repository contributors using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"

    # Build query parameters
    query_params = {"per_page": per_page, "page": page}

    if anon:
        query_params["anon"] = 1

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

repository_contributors = project.tools.create(
    name="Get Repository Contributors",
    slug="repository-contributors",
    description="""
    Get the list of contributors to a GitHub repository.
    
    Use this tool to:
    - Understand project community size and activity
    - Identify key contributors and maintainers
    - Assess project health through contributor diversity
    - Find experts for specific repositories
    
    The response includes:
    - Contributor profiles and GitHub links
    - Number of contributions per person
    - Both registered users and anonymous contributors
    
    This information helps evaluate:
    - Project sustainability
    - Community engagement
    - Expertise levels
    - Potential collaboration opportunities
    """,
    handler=get_repository_contributors_handler,
    parameters=RepositoryContributorsParams,
    if_exists="replace",
)
