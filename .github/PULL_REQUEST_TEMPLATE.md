# Pull Request

## Summary
Describe the changes introduced by this PR in one or two sentences.

## What changed
- Implementation details
- Files added/modified

## Verification
Steps to run locally:

1. Install deps: `python -m pip install -r requirements.txt`
2. Run unit tests: `./scripts/run_tests.sh`
3. (Optional) Run E2E scaffold: `./scripts/run_e2e.sh` (requires NETBOX_URL and NETBOX_TOKEN)

## Reviewer Checklist
- [ ] F1 Functionality: unit tests and smoke checks
- [ ] F2 Security: secret scan, validators
- [ ] F3 QA: E2E scripts (if infra available)
- [ ] F4 Ops: Docker build & deploy guidance

Add any notes for reviewers below.
