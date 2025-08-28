# GitHub Tools for Braintrust

A comprehensive set of GitHub API tools designed to work together for exploring repositories, issues, pull requests, and more. These tools are optimized for use with Braintrust's AI platform.

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)  
- [Tools Included](#tools-included)
- [Tool Chaining Examples](#tool-chaining-examples)
- [GitHub Token Setup](#github-token-setup-recommended)
- [Usage in Braintrust](#usage-in-braintrust)
- [Customizing Tools](#customizing-tools)
- [File Structure](#file-structure)
- [Security Notes](#security-notes)
- [Support](#support)

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd braintrust-playground/github_tools
```

### 2. Install Dependencies
For local development and deployment:
```bash
pip install -r requirements-dev.txt
```

**Requirements Files:**
- `requirements-dev.txt`: Contains `braintrust[cli]` for local development and deployment
- `requirements.txt`: Contains only runtime dependencies (`braintrust`, `requests`, `pydantic`) needed by the tools when running in Braintrust

### 3. Set Braintrust API Key (Required for Deployment)
```bash
export BRAINTRUST_API_KEY="your_braintrust_api_key"
```

Get your API key from: https://www.braintrust.dev/app/settings

### 4. Deploy to Braintrust
```bash
braintrust push github_tools.py --requirements requirements.txt
```

## Features

- **Chainable Tools**: Outputs from one tool provide perfect context for others
- **Comprehensive Coverage**: Search, explore, and analyze GitHub data
- **Rate Limit Aware**: Uses authenticated requests when `GITHUB_TOKEN` is provided
- **Rich Data Models**: Structured responses with all relevant information

## Tools Included

### 1. Search Repositories (`search-repositories`)
Search for repositories using powerful GitHub query syntax.

**Example queries:**
- `"language:python stars:>1000"` - Popular Python repos
- `"topic:machine-learning"` - ML-focused repositories  
- `"user:microsoft"` - Microsoft's repositories
- `"created:>2023-01-01"` - Recently created repos

### 2. Repository Details (`repository-details`)
Get comprehensive information about a specific repository.

**Use after:** Repository search to get detailed info about interesting repos.

### 3. List Issues (`list-issues`) 
List issues from a specific repository with filtering options.

**Filters:**
- State: open, closed, all
- Labels: specific labels
- Sort: created, updated, comments
- Date ranges

### 4. List Pull Requests (`list-pull-requests`)
List pull requests from a repository with filtering.

**Filters:**
- State: open, closed, all  
- Head/base branches
- Sort options

### 5. Search Issues (`search-issues`)
Search for issues across all of GitHub.

**Example queries:**
- `"is:open label:bug"` - Open bug issues
- `"repo:owner/repo state:open"` - Issues in specific repo
- `"assignee:username"` - Issues assigned to user

### 6. Repository Contents (`repository-contents`)
Browse repository files and folders.

**Use cases:**
- Explore project structure
- Get file contents
- Understand codebase organization

### 7. User Info (`user-info`)
Get information about GitHub users or organizations.

**Provides:**
- Profile information
- Statistics (repos, followers)
- Contact details

### 8. Repository Contributors (`repository-contributors`)
Get contributor information for a repository.

**Insights:**
- Community size
- Key contributors
- Contribution patterns

## Tool Chaining Examples

### Workflow 1: Research a Technology
1. **Search Repositories**: `"topic:react stars:>5000"`
2. **Repository Details**: Get details on top results
3. **List Issues**: Check what problems people face
4. **User Info**: Learn about maintainers

### Workflow 2: Project Analysis
1. **Repository Details**: Get comprehensive repo info
2. **Repository Contributors**: Understand the community
3. **List Pull Requests**: See recent development activity
4. **Repository Contents**: Explore code structure

### Workflow 3: Issue Investigation
1. **Search Issues**: Find relevant issues across GitHub
2. **Repository Details**: Get context on affected repos
3. **List Issues**: See related issues in same repo
4. **User Info**: Research issue authors

## GitHub Token Setup (Recommended)

### Set GitHub Token in Braintrust
Instead of setting environment variables locally, configure the `GITHUB_TOKEN` as an environment variable within the Braintrust platform:

1. Go to your Braintrust project settings
2. Navigate to the **Environment Variables** section  
3. Click **Add Environment Variable**
4. Set `GITHUB_TOKEN` as the key
5. Add your GitHub personal access token as the value
6. Save the configuration

This approach is more secure and ensures the token is available when tools run in Braintrust's environment.

**Rate Limits:**
- Without a token: 60 requests/hour (will hit limits quickly)
- With a token: 5,000 requests/hour (recommended for production)

**Getting a GitHub Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with appropriate permissions (public_repo for public repos)
3. Copy the token and add it to Braintrust environment variables

## Usage in Braintrust

### Quick Start with Pre-built Prompt
We've included a comprehensive GitHub Assistant prompt that works with these tools.

The prompt template is available in `github_assistant_prompt.md` - this contains detailed instructions on how to use all the GitHub tools effectively, including proper search query construction and tool chaining strategies.

### Manual Setup in UI
1. Go to your project's Tools page
2. Select the GitHub tools you want to use
3. Add them to your prompts
4. Use the prompt content from `github_assistant_prompt.md`

### GitHub Assistant Prompt Features

The included prompt (`github_assistant_prompt.md`) provides:

- **Comprehensive Tool Understanding**: Knows all 8 GitHub tools and their capabilities
- **Strategic Tool Chaining**: Uses tools in logical sequences for maximum insight
- **Proper Query Construction**: Includes critical guidance on GitHub search syntax
- **Flexible Question Handling**: Adapts to any GitHub-related question
- **Actionable Insights**: Provides analysis and recommendations, not just data

**Key Features:**
- Proper search query construction with GitHub syntax
- Tool chaining strategies for complex analysis
- Response guidelines for helpful, thorough answers
- Example workflows for common use cases

### In Code
```python
import braintrust

# The tools are automatically available after pushing
# Use them in prompts or eval scenarios
```

## Example LLM Conversations

### Research Assistant
**Human**: "Find popular Python web frameworks and analyze their recent issues"

**LLM using tools**:
1. Searches repositories: `"topic:web-framework language:python stars:>1000"`
2. Gets details on Flask, Django, FastAPI repos
3. Lists recent issues from each
4. Provides analysis of common problems and trends

### Code Explorer  
**Human**: "I want to understand how [repo] is structured and who maintains it"

**LLM using tools**:
1. Gets repository details
2. Lists contributors to understand maintainers
3. Browses repository contents to show structure
4. Gets user info on key contributors

## Rate Limits & Best Practices

- **With GitHub token**: 5,000 requests/hour
- **Without token**: 60 requests/hour  
- Tools include proper error handling for rate limits
- Use specific queries to reduce API calls needed
- **Set GITHUB_TOKEN in Braintrust environment variables** for production use
- For local testing without a token, expect to hit rate limits quickly

## Error Handling

All tools include comprehensive error handling for:
- Network issues
- API rate limits
- Invalid parameters
- Missing repositories/users
- Authentication problems

## File Structure

```
github_tools/
├── __init__.py                     # Package initialization
├── requirements.txt                # Runtime dependencies for Braintrust
├── requirements-dev.txt            # Development dependencies (braintrust[cli])
├── github_tools.py                 # Main file to deploy all tools
├── github_assistant_prompt.md      # Comprehensive prompt template
├── README.md                       # This documentation
└── Individual tool files:
    ├── search_repositories.py      # Search GitHub repositories
    ├── repository_details.py       # Get detailed repo information
    ├── list_issues.py              # List repository issues
    ├── list_pull_requests.py       # List repository PRs
    ├── search_issues.py            # Search issues across GitHub
    ├── repository_contents.py      # Browse repository files/folders
    ├── user_info.py                # Get user/organization info
    └── repository_contributors.py  # Get repository contributors
```

## Customizing Tools

### Adding New Tools
To add new GitHub API endpoints:

1. Create a new `.py` file following the existing pattern
2. Define Pydantic models for parameters 
3. Create the tool with `project.tools.create()`
4. Add import to `github_tools.py`
5. Update this README

### Removing Tools (Optional)
If you don't need all 8 tools, you can remove specific ones:

1. **Remove the import** from `github_tools.py`:
   ```python
   # Comment out or remove unwanted tools
   # from search_issues import search_issues
   # from repository_contributors import repository_contributors
   ```

2. **Remove from the `_tools` list** in `github_tools.py`:
   ```python
   _tools = [
       search_repositories,
       repository_details,
       list_issues,
       list_pull_requests,
       # search_issues,        # Removed
       repository_contents,
       user_info,
       # repository_contributors,  # Removed
   ]
   ```

3. **Redeploy** to Braintrust:
   ```bash
   braintrust push github_tools.py --requirements requirements.txt
   ```

**Note**: Removing tools will make them unavailable to your prompts. Make sure any prompts using those tools are updated accordingly.

## Security Notes

- **Never commit GitHub tokens to version control**
- **Use Braintrust environment variables** for sensitive data like tokens
- **Avoid setting tokens in local environment** for production deployments
- The tools run in Braintrust's secure sandbox environment
- All API requests use HTTPS
- Braintrust manages environment variables securely in their platform

## Support

For issues with these tools:
1. Check GitHub API status
2. Verify your token has necessary permissions  
3. Review Braintrust logs for detailed error messages
4. Check rate limit headers in responses
5. Ensure you're using the correct deployment command with requirements: `braintrust push github_tools.py --requirements requirements.txt`
