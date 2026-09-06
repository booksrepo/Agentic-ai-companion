# Chapter 2 — The Missing Fundamentals: Git, CI/CD, and IaC Refresher

No AI in this chapter on purpose. Everything after this depends on you being
able to read and explain a pipeline or an infrastructure plan *before* an
agent starts touching either one.

## What's here

`ci-fundamentals-demo/` is a minimal, working project:

- `app.py` / `test_app.py` — a trivial function and its test, wired into CI.
- `.github/workflows/ci.yml` — runs `pytest` on every push and PR.
- `terraform/main.tf` — a single declarative resource (`local_file`) used to
  demonstrate `plan` vs `apply`.

## Try it yourself

```bash
cd ci-fundamentals-demo
git init
git add .
git commit -m "Add app, tests, and CI workflow"
```

Push it to a repo of your own and confirm the workflow goes green.

```bash
cd terraform
terraform init
terraform plan    # shows what WOULD change, without changing anything
terraform apply   # actually creates greeting.txt
terraform apply   # run again — Terraform reports "No changes"
```

## Break It / Fix It

1. **Break the pipeline.** Open `ci.yml` and indent the `run: pytest -v` line
   one level too deep, nesting it incorrectly under `name:` instead of as a
   sibling key. Push the change and watch it fail.
2. **Break the infrastructure.** Delete `greeting.txt` directly
   (`rm greeting.txt`) without telling Terraform, then run `terraform plan`.
   Notice Terraform detects the drift between declared and actual state.
3. **Fix the smallest thing that resolves the specific symptom.** Fix the
   YAML indentation, rerun the pipeline, and confirm the test step actually
   executes (not just that the job is green). Run `terraform apply` again and
   confirm `greeting.txt` reappears.

## Checkpoint

You should be comfortable with: branching off `main`, committing in logical
units, writing a PR description that explains *why* not just *what*, reading
an unfamiliar CI workflow file and explaining it in plain English, and
explaining why `terraform plan` matters even though `apply` is the step that
actually changes anything. If any of that's shaky, this is the chapter to
revisit before moving on — every later chapter assumes it.

See also: `appendix/appendix_c_setup_guides/setup-guides.md` for GitLab CI,
Azure DevOps, CircleCI, Bicep, and Pulumi equivalents of everything here.
