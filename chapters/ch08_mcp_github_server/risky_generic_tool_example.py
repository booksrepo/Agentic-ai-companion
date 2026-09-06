# risky_generic_tool_example.py
#
# DON'T do this — shown here specifically to demonstrate why not.
# A single, flexible tool feels efficient (one tool instead of three, and
# it can do anything the GitHub API can do). That flexibility is exactly
# the problem: if the underlying token has broader scopes than intended,
# this one tool can close issues, delete comments, modify repo settings,
# or push code — regardless of what you ever intended the agent to have
# access to. The tool's interface claims to be generic; its actual reach
# is bounded only by whatever the token underneath it can do.

import httpx

from github_client import BASE_URL, _headers


def call_github_api(method, path, json_body=None):
    resp = httpx.request(method, f"{BASE_URL}{path}", headers=_headers(), json=json_body)
    resp.raise_for_status()
    return resp.json()
