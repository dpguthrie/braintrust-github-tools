"""
GitHub User/Organization Info Tool for Braintrust

This tool gets information about GitHub users or organizations.
Useful for understanding repository owners and contributors.
"""

import os
from typing import Optional

import braintrust
import requests
from pydantic import BaseModel


class UserInfoParams(BaseModel):
    username: str


class UserInfo(BaseModel):
    login: str
    id: int
    avatar_url: str
    gravatar_id: Optional[str]
    url: str
    html_url: str
    followers_url: str
    following_url: str
    repos_url: str
    type: str  # "User" or "Organization"
    site_admin: bool
    name: Optional[str]
    company: Optional[str]
    blog: Optional[str]
    location: Optional[str]
    email: Optional[str]
    hireable: Optional[bool]
    bio: Optional[str]
    twitter_username: Optional[str]
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str


def get_user_info_handler(username: str):
    """Get user/organization information using GitHub API"""

    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Braintrust-GitHub-Tools",
    }

    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Build the API URL
    url = f"https://api.github.com/users/{username}"

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

user_info = project.tools.create(
    name="Get User/Organization Info",
    slug="user-info",
    description="""
    Get detailed information about a GitHub user or organization.
    
    Use this tool to:
    - Learn about repository owners from search results
    - Understand contributor backgrounds
    - Get context about organizations
    - Find contact information and social links
    
    The response includes:
    - Profile information (name, bio, location)
    - Statistics (repos, followers, following)
    - Contact details (email, blog, Twitter)
    - Account type (User vs Organization)
    
    This context helps understand the credibility and focus
    of repositories and their maintainers.
    """,
    handler=get_user_info_handler,
    parameters=UserInfoParams,
    if_exists="replace",
)
