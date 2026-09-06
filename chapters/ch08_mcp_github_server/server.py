# server.py
#
# Three narrow, specific MCP tools — deliberately not one generic
# call_github_api tool. See the "Break It" section in the README for why
# that design choice matters as much as the credential scoping below it.

import os

import github_client
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("github-issues")
REPO = os.environ["GITHUB_REPO"]

MAX_BODY_LENGTH = 2000


@mcp.tool()
def list_issues(label: str = "") -> list[dict]:
    """List open issues in the configured repository, optionally filtered by label."""
    issues = github_client.list_open_issues(REPO, label=label or None)
    return [{"number": i["number"], "title": i["title"], "labels": [l["name"] for l in i["labels"]]} for i in issues]


@mcp.tool()
def read_issue(issue_number: int) -> dict:
    """Read the title and body of a specific issue by number."""
    issue = github_client.get_issue(REPO, issue_number)
    body = issue["body"] or ""
    truncated = len(body) > MAX_BODY_LENGTH
    return {
        "number": issue["number"],
        "title": issue["title"],
        # Sanitize and bound what comes back from a tool, not just what
        # goes into it — an issue body is untrusted content, the same
        # threat model as a PR diff (Chapter 6).
        "body": body[:MAX_BODY_LENGTH],
        "truncated": truncated
    }


@mcp.tool()
def comment_on_issue(issue_number: int, comment: str) -> dict:
    """Add a comment to a specific issue by number."""
    try:
        result = github_client.add_issue_comment(REPO, issue_number, comment)
        return {"success": True, "comment_id": result["id"], "url": result["html_url"]}
    except Exception as e:
        return {"success": False, "error": f"GitHub API error: {e} — check that issue #{issue_number} exists in {REPO}."}


if __name__ == "__main__":
    mcp.run()
