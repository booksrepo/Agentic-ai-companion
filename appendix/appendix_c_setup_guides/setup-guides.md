# Appendix C: Tool-Agnostic Setup Guides

This book used GitHub Actions, Terraform, and Anthropic's API for concrete
examples. The underlying concepts transfer directly — here's a quick
translation layer for other stacks.

## CI/CD Platform Equivalents (for Chapter 2 and beyond)

**Workflow definition file**

| Platform | Location |
|---|---|
| GitHub Actions | `.github/workflows/*.yml` |
| GitLab CI | `.gitlab-ci.yml` |
| Azure DevOps | `azure-pipelines.yml` |
| CircleCI | `.circleci/config.yml` |

**Triggering on a pull request**

| Platform | Mechanism |
|---|---|
| GitHub Actions | `on: pull_request` |
| GitLab CI | `rules:` with `merge_request_event` |
| Azure DevOps | a `pr:` trigger block |
| CircleCI | a `workflows` entry with a branch/filter condition |

**Defining a job**

| Platform | Mechanism |
|---|---|
| GitHub Actions | `jobs:` |
| GitLab CI | `stages:`, with jobs listed under each stage |
| Azure DevOps | `jobs:` nested under a stage |
| CircleCI | `jobs:` |

**Injecting a secret**

| Platform | Mechanism |
|---|---|
| GitHub Actions | `secrets.NAME` |
| GitLab CI | masked/protected variables |
| Azure DevOps | Azure Key Vault or pipeline variables |
| CircleCI | contexts or environment variables |

The structural concepts from Chapter 2 — trigger, build, test, analyze,
deploy — map onto all four platforms identically; only the YAML shape
differs.

## IaC Tool Equivalents (for Chapter 2's Terraform demo)

**Terraform** (as shown in Chapter 2):

```hcl
resource "local_file" "greeting" {
  filename = "${path.module}/greeting.txt"
  content  = "Hello from Terraform.\n"
}
```

**Bicep** (Azure-native) — same declarative idea, different syntax and
provider surface:

```bicep
resource greetingBlob 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: 'greeting-container'
  // ...properties describing desired state, reconciled by Azure Resource Manager
}
```

**Pulumi** (code-based IaC) — declarative outcome, imperative-looking
syntax:

```python
import pulumi_local as local

greeting = local.File("greeting", filename="greeting.txt", content="Hello from Pulumi.\n")
```

All three follow the same plan-before-apply discipline from Chapter 2
(Pulumi calls it `preview`; Bicep's is a "what-if" deployment) — the
specific command name changes, the "review before you commit" habit
doesn't.

## LLM API Equivalents (for Chapters 4 through 10)

This book's examples used Anthropic's Messages API. The same tool-use loop
pattern (Chapter 8) applies with any provider supporting function/tool
calling — the request and response shapes differ in field names, but the
perceive-decide-act-observe loop is identical. Check your provider's
current documentation for exact schema names before adapting this book's
code samples directly.
