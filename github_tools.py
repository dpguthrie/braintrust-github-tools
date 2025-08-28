"""
GitHub Tools for Braintrust

This file imports and registers all GitHub API tools for deployment to Braintrust.
Run `braintrust push github_tools.py` to deploy all tools at once.

Tools included:
1. search-repositories: Search for repositories by query
2. repository-details: Get detailed info about a specific repository
3. list-issues: List issues from a repository
4. list-pull-requests: List pull requests from a repository
5. search-issues: Search for issues across repositories
6. repository-contents: Browse repository files and folders
7. user-info: Get user/organization information
8. repository-contributors: Get repository contributor list

These tools work together - outputs from one provide context for others.
For example: search-repositories → repository-details → list-issues
"""

# Import all the individual tools
from list_issues import list_issues
from list_pull_requests import list_pull_requests
from repository_contents import repository_contents
from repository_contributors import repository_contributors
from repository_details import repository_details
from search_issues import search_issues
from search_repositories import search_repositories
from user_info import user_info

# All tools are automatically registered when imported
# since each module calls project.tools.create()

# Keep references to avoid unused import warnings
_tools = [
    search_repositories,
    repository_details,
    list_issues,
    list_pull_requests,
    search_issues,
    repository_contents,
    user_info,
    repository_contributors,
]

print("GitHub Tools loaded successfully!")
print("\nAvailable tools:")
print("1. search-repositories - Search for repositories")
print("2. repository-details - Get repository details")
print("3. list-issues - List repository issues")
print("4. list-pull-requests - List repository PRs")
print("5. search-issues - Search issues globally")
print("6. repository-contents - Browse repository contents")
print("7. user-info - Get user/org information")
print("8. repository-contributors - Get contributor list")
print("\nTo deploy: braintrust push github_tools.py")
print(
    "\nNote: Set GITHUB_TOKEN as environment variable in Braintrust for authenticated requests"
)
