# CI definition (staged, not active)

`agl-adapters-tests.yml` is the adapter-plane CI job. It is kept here instead of
`.github/workflows/` because the push credential used for this branch has the
`repo` scope but **not** `workflow`; GitHub rejects any push that creates or
updates a file under `.github/workflows/` without that scope.

To activate it (requires a token/app with `workflow` scope, and user approval
per the workorder):

```bash
mkdir -p .github/workflows
git mv factory/ci/agl-adapters-tests.yml .github/workflows/agl-adapters-tests.yml
git commit -m "ci: activate adapter tests"
git push
```

The job is `pull_request` + `workflow_dispatch` only: no cron, no deployment,
no paid service. It runs `pytest -m "not network"`, so it needs no credentials.
