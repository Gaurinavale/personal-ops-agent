import os
from dotenv import load_dotenv
from github import Github
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Personal Ops - GitHub")

# Authenticate once using your Personal Access Token
_client = Github(os.getenv("GITHUB_TOKEN"))


@mcp.tool()
def list_issues(repo: str, state: str = "open") -> list[dict]:
    """
    List issues from a GitHub repository.

    Args:
        repo: Repository in 'username/repo-name' format, e.g. 'Gaurinavale/personal-ops-agent'.
        state: 'open', 'closed', or 'all'.
    """
    repository = _client.get_repo(repo)
    issues = repository.get_issues(state=state)
    return [
        {"number": issue.number, "title": issue.title, "state": issue.state}
        for issue in issues
    ]


@mcp.tool()
def create_issue(repo: str, title: str, body: str = "") -> dict:
    """
    Create a new issue on a GitHub repository.

    Args:
        repo: Repository in 'username/repo-name' format.
        title: Title of the issue.
        body: Optional description text for the issue.
    """
    repository = _client.get_repo(repo)
    issue = repository.create_issue(title=title, body=body)
    return {"success": True, "issue_number": issue.number, "url": issue.html_url}