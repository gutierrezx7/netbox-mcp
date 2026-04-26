## Learnings Log

- [2026-04-26T20:05:10Z] Updated `.gitignore` to include Python-specific patterns, virtual environments, IDE configurations, build artifacts, OS files, and Sisyphus temporary files. This ensures that unnecessary files are not tracked by Git, keeping the repository clean. The file `.env` is ignored, and no tracked secrets were found to require history rewriting.

## 2026-04-26 10:30:00 - pyproject.toml added

Added pyproject.toml to the repository root. This file defines project metadata, build system requirements, and dependencies. It includes runtime dependencies like pydantic and httpx, development dependencies such as pytest, black, and ruff, and sets up an entrypoint script 'netbox-mcp' to run the server. This configuration allows the package to be installed and executed correctly.


- [2026-04-26T20:40:00Z] Subagent created `src/netbox_mcp_server/config.py` and `tests/test_config.py`.
  - Observations: The Settings class uses pydantic.BaseSettings via `pydantic_settings` import and provides a cached `get_settings(cli_args=None)` accessor. Tests exercise env var loading and CLI overrides.
  - Blocker: Unable to run pytest or lsp_diagnostics in this environment — Python interpreter and language server are not installed. Verification (tests and LSP checks) could not be executed here. See issues.md for details.
