# Final Verification Wave Checklist

This file lists the final verification steps required before declaring the plan COMPLETE.

Essential checks (must all PASS):

1. Unit tests
   - Command: `pytest -q`
   - Expected: all tests pass (exit 0)

2. LSP / Type checks
   - Command: run your preferred language server or `ruff` / `mypy` if configured
   - Expected: no new diagnostics in modified files

3. CI
   - The GitHub Actions workflow `.github/workflows/ci.yml` should pass on PR

4. E2E against NetBox LXC 1038
   - Create, update, delete, search, changelogs tests must pass against the real instance

5. Packaging / Docker
   - Build the Docker image locally and validate entrypoint

6. MetaMCP integration on LXC 1043
   - Install as mcp-netbox user and verify registration

Reviewer tasks (F1-F4):
- F1: Functionality reviewer — confirm 7 MCP tools are registered and operational
- F2: Security reviewer — confirm tokens not exposed, input sanitization, rate limits
- F3: QA reviewer — run E2E scripts and validate results
- F4: Ops reviewer — validate deployment steps and MetaMCP integration

When ALL items above are APPROVED, mark `pass-final-wave` TODO as completed.
