# github_client.py
import os

import httpx

BASE_URL = "https://api.github.com"


def _headers():
    return {
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }


def list_open_issues(repo, label=None):
    params = {"state": "open"}
    if label:
        params["labels"] = label
    resp = httpx.get(f"{BASE_URL}/repos/{repo}/issues", headers=_headers(), params=params)
    resp.raise_for_status()
    return resp.json()


def get_issue(repo, issue_number):
    resp = httpx.get(f"{BASE_URL}/repos/{repo}/issues/{issue_number}", headers=_headers())
    resp.raise_for_status()
    return resp.json()


def add_issue_comment(repo, issue_number, body):
    resp = httpx.post(
        f"{BASE_URL}/repos/{repo}/issues/{issue_number}/comments",
        headers=_headers(),
        json={"body": body}
    )
    resp.raise_for_status()
    return resp.json()
