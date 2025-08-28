"""
GitHub Repository Contents Tool for Braintrust

This tool gets the contents of a repository directory or file.
Useful for exploring repository structure and understanding codebases.
"""

import os
from typing import List, Optional

import braintrust
import requests
from pydantic import BaseModel


class RepositoryContentsParams(BaseModel):
    owner: str
    repo: str
    path: Optional[str] = ""  # Default to root directory
    ref: Optional[str] = None  # Branch, tag, or commit SHA


class ContentItem(BaseModel):
    name: str
    path: str
    sha: str
    size: int
    url: str
    html_url: str
    git_url: str
    download_url: Optional[str]
    type: str  # "file" or "dir"
    content: Optional[str] = None  # Base64 encoded content for files
    encoding: Optional[str] = None  # Usually "base64" for files


class RepositoryContentsResponse(BaseModel):
    contents: List[ContentItem]
    path: str
    repository: str


def get_repository_contents_handler(
    owner: str, repo: str, path: str = "", ref: str | None = None
):
    """Get repository contents using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    # Build query parameters
    query_params = {}
    if ref:
        query_params["ref"] = ref

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

repository_contents = project.tools.create(
    name="Get Repository Contents",
    slug="repository-contents",
    description="""
    Get the contents of a repository directory or file.
    
    Use this tool to:
    - Explore repository structure
    - Browse folders and files
    - Get file contents for analysis
    - Understand project organization
    
    Parameters:
    - path: Directory or file path (empty for root)
    - ref: Specific branch, tag, or commit (defaults to default branch)
    
    For files, content is returned base64-encoded.
    For directories, returns list of items in that directory.
    
    This helps understand what tools or approaches might be needed
    for further analysis of the codebase.
    """,
    handler=get_repository_contents_handler,
    parameters=RepositoryContentsParams,
    if_exists="replace",
)
