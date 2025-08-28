"""
GitHub Repository Details Tool for Braintrust

This tool gets detailed information about a specific GitHub repository.
Takes owner/repo from search results or direct input.
"""

import os
from typing import List, Optional

import braintrust
import requests
from pydantic import BaseModel


class RepositoryDetailsParams(BaseModel):
    owner: str
    repo: str


class RepositoryDetails(BaseModel):
    id: int
    name: str
    full_name: str
    owner: dict
    description: Optional[str]
    html_url: str
    clone_url: str
    ssh_url: str
    git_url: str
    homepage: Optional[str]
    size: int
    stargazers_count: int
    watchers_count: int
    forks_count: int
    language: Optional[str]
    topics: List[str]
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[dict]
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    visibility: str
    default_branch: str
    created_at: str
    updated_at: str
    pushed_at: str
    permissions: Optional[dict]


def get_repository_details_handler(owner: str, repo: str):
    """Get detailed repository information using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the API URL
    url = f"https://api.github.com/repos/{owner}/{repo}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Return the raw JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"GitHub API request failed: {str(e)}")
    except KeyError as e:
        raise Exception(f"Unexpected response format: {str(e)}")


project = braintrust.projects.create(name="github-tools")

repository_details = project.tools.create(
    name="Get Repository Details",
    slug="repository-details",
    description="""
    Get detailed information about a specific GitHub repository.
    
    Use this tool with repository owner and name from search results
    or when you need comprehensive information about a repository.
    
    The output includes:
    - Repository metadata (stars, forks, size, language)
    - URLs for cloning and browsing
    - License information
    - Permission details
    - Topics and description
    
    This information can be used to determine which other tools to use
    (e.g., if open_issues_count > 0, use list-issues tool).
    """,
    handler=get_repository_details_handler,
    parameters=RepositoryDetailsParams,
    if_exists="replace",
)
