"""
GitHub Repository Search Tool for Braintrust

This tool searches for repositories on GitHub based on various criteria.
The output provides repository details that can be used by other tools.
"""

import os
from typing import List, Optional

import braintrust
import requests
from pydantic import BaseModel


class RepositorySearchParams(BaseModel):
    query: str
    sort: Optional[str] = "stars"  # stars, forks, help-wanted-issues, updated
    order: Optional[str] = "desc"  # asc, desc
    per_page: Optional[int] = 10  # max 100
    page: Optional[int] = 1


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    owner: dict
    description: Optional[str]
    html_url: str
    clone_url: str
    stargazers_count: int
    forks_count: int
    language: Optional[str]
    topics: List[str]
    created_at: str
    updated_at: str
    default_branch: str


class SearchRepositoriesResponse(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[Repository]


def search_repositories_handler(
    query: str,
    sort: str = "stars",
    order: str = "desc",
    per_page: int = 10,
    page: int = 1,
):
    """Search for repositories using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the search URL
    url = "https://api.github.com/search/repositories"

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

search_repositories = project.tools.create(
    name="Search GitHub Repositories",
    slug="search-repositories",
    description="""
    Search for repositories on GitHub based on query parameters.
    
    Query examples:
    - "language:python stars:>1000" - Python repos with >1000 stars
    - "topic:machine-learning" - Repos tagged with machine-learning
    - "user:microsoft" - Repositories owned by Microsoft
    - "org:google" - Repositories owned by Google organization
    - "created:>2023-01-01" - Repos created after Jan 1, 2023
    
    Results include repository details that can be used with other GitHub tools
    like listing issues, PRs, or getting repository contents.
    """,
    handler=search_repositories_handler,
    parameters=RepositorySearchParams,
    if_exists="replace",
)
