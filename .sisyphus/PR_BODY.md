PR Title: feat(netbox-mcp): Full CRUD MCP Server (config, search, CRUD, changelogs, docs)

Summary
-------
This branch implements a full MCP server for NetBox with the following key additions:

- Configuration: pydantic-based Settings and get_settings() (src/netbox_mcp_server/config.py)
- Object type mapping: NETBOX_OBJECT_TYPES (src/netbox_mcp_server/types.py)
- HTTP client: NetBoxRestClient with retries, rate limiting, and safe exception handling (src/netbox_mcp_server/client.py)
- Validators: filter/lookup validation utilities (src/netbox_mcp_server/validators.py)
- Search: netbox_search_objects aggregation helper (src/netbox_mcp_server/search.py)
- Objects API helpers: list and get-by-id (src/netbox_mcp_server/objects.py)
- CRUD helpers: create/update/delete single & bulk with tests (src/netbox_mcp_server/crud.py)
- Changelogs retrieval helper (src/netbox_mcp_server/changelogs.py)
- Unit tests for modules under tests/*
- Documentation: README, CONTRIBUTING, CHANGELOG, LICENSE, .env.example, Dockerfile
- CI: GitHub Actions workflow to run pytest (.github/workflows/ci.yml)

Files Changed / Added (high level)
---------------------------------
See git log for full history. Notable files:
- src/netbox_mcp_server/{config,types,client,validators,search,objects,crud,changelogs}.py
- tests/{test_config.py,test_client.py,test_types.py,test_search.py,test_validators.py,test_get_objects.py,test_get_object_by_id.py,test_crud_create.py,test_crud_update_delete.py,test_changelogs.py}
- README.md, CONTRIBUTING.md, CHANGELOG.md, LICENSE
- .env.example, Dockerfile
- .github/workflows/ci.yml

Verification (Reviewer Steps)
----------------------------
Prereqs: Python 3.11+, pip, (optionally Docker for container check)

1. Install deps:
   python -m pip install -r requirements.txt

2. Run unit tests (recommended to run full suite):
   pytest -q

3. Lint/typechecks (optional):
   ruff check .

4. Smoke test core flows (non-destructive):
   - Use the example in README to instantiate NetBoxRestClient and call netbox_get_objects (requires NETBOX_URL and NETBOX_TOKEN)

5. CI: The workflow .github/workflows/ci.yml runs pytest on PRs and commits.

Reviewer Guidance
------------------
F1 (Functionality): Run unit tests and smoke tests; confirm MCP tools behavior.
F2 (Security): Search for secrets, confirm .gitignore and validators enforce constraints.
F3 (QA): Run E2E harness against NetBox LXC (if available) — create/update/delete/search/changelogs.
F4 (Ops): Build Docker image and validate entrypoint.

Notes & Blockers
----------------
- This workspace lacked an executable Python interpreter and LSP during implementation; I could NOT run pytest or lsp_diagnostics here. Tests were added but must be executed locally or in CI. See .sisyphus/notepads/netbox-mcp-crud-implementation/issues.md for details.

If you want me to push and open a PR, provide the remote URL and target branch name and I will create the branch, push, and open a PR with this body. I will NOT push without explicit permission.
