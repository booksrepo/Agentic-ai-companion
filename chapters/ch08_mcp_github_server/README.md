# Chapter 8 — Standardizing Context and Actions With MCP

A small MCP server exposing three narrow GitHub tools, plus a client that
runs the full perceive-decide-act-observe loop against them.

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install mcp httpx anthropic
```

Create a **fine-grained** GitHub Personal Access Token scoped to exactly one
repository, with only `Issues: Read and write` — not a classic token with
full repo access.

```bash
export GITHUB_TOKEN="your-fine-grained-token"
export GITHUB_REPO="your-username/your-repo"
```

## Try it

```bash
mcp dev server.py       # interactive inspector — confirm tools work before any LLM is involved
```

Then drive it from an agent:

```python
import asyncio
from agent_client import run_task

print(asyncio.run(run_task("Summarize all open issues labeled 'bug'.")))
```

Watch it call `list_issues(label="bug")`, then `read_issue` on each returned
number, before producing a final summary — genuinely composing multiple
tool calls from a high-level instruction, still entirely Level 0 since
nothing here writes anything back yet.

## Break It

Ask the agent: *"Post a comment saying 'thanks for the report' on issue
9999."* If issue 9999 doesn't exist, the naive version of `comment_on_issue`
lets the underlying HTTP error propagate — potentially crashing the server
process, or returning an opaque error the agent can't reason about.

`risky_generic_tool_example.py` shows the other way this can go wrong: one
generic `call_github_api(method, path, json_body)` tool instead of three
narrow ones. It's tempting — fewer tools, more flexibility — but the blast
radius of a hallucinated or successfully prompt-injected call is now as
large as whatever the token can do, not the narrow action a well-designed
tool interface would have limited it to.

## Fix It / Guardrails

1. **`comment_on_issue`** in `server.py` catches the failure and returns a
   structured, informative error the agent can actually reason about,
   instead of taking down the whole server over one bad argument.
2. **Build narrow, specific tools, deliberately, as a design principle.**
   Three tools that each do exactly one thing are dramatically safer than
   one tool that can do anything — the shape of a tool interface is itself
   a security boundary, independent of the credential behind it.
3. **Scope the credential to match the narrowest tool interface**, not the
   other way around. The fine-grained token above cannot delete the repo,
   push code, or touch any other repo, no matter what the LLM attempts or
   what gets injected into a tool call — a second, independent boundary
   underneath the interface.
4. **`MAX_BODY_LENGTH` in `read_issue`** sanitizes and bounds what comes
   back from a tool, not just what goes in — an issue body is untrusted
   content, the same threat model as a PR diff in Chapter 6.

## Exercises

- Walk through why a single generic `call_github_api` tool is riskier than
  three narrow, specific tools, even backed by the exact same credential.
- Add a fourth narrow tool (e.g. `close_issue`) and decide, explicitly, what
  the minimum credential scope for it should be.
