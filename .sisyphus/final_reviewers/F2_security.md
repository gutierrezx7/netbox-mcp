# F2 — Security Reviewer

Goal: Verify that secrets are not exposed, inputs are sanitized, and guardrails enforced.

Checks to perform:

1. Search for accidental secrets in commits and tracked files:

   ```bash
   git grep -n "NETBOX_TOKEN" || true
   git grep -n "TOKEN" || true
   ```

2. Verify .gitignore contains `.env` and other secrets are not tracked:

   ```bash
   git status --porcelain
   git ls-files | rg "\.env|secret|credential" || true
   ```

3. Static review of validators and client code:

   - Ensure `validate_object_type` uses allowlist from types.py
   - Ensure `parse_lookup_expressions` enforces max lengths
   - Ensure client does not log tokens and uses Authorization header only

Deliverables:
- Findings report (pass/fail) and any file paths with issues.
