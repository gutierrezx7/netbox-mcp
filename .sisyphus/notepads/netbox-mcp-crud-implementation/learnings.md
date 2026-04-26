## Learnings Log

- [2026-04-26T20:05:10Z] Updated `.gitignore` to include Python-specific patterns, virtual environments, IDE configurations, build artifacts, OS files, and Sisyphus temporary files. This ensures that unnecessary files are not tracked by Git, keeping the repository clean. The file `.env` is ignored, and no tracked secrets were found to require history rewriting.

## 2026-04-26 10:30:00 - pyproject.toml added

Added pyproject.toml to the repository root. This file defines project metadata, build system requirements, and dependencies. It includes runtime dependencies like pydantic and httpx, development dependencies such as pytest, black, and ruff, and sets up an entrypoint script 'netbox-mcp' to run the server. This configuration allows the package to be installed and executed correctly.

## 2026-04-26 11:00:00 - T1.3: NETBOX_OBJECT_TYPES implementation

Created `src/netbox_mcp_server/types.py` containing the `NETBOX_OBJECT_TYPES` mapping, which includes over 50 entries for various NetBox object types and their corresponding API endpoint paths across DCIM, IPAM, Circuits, Tenancy, Virtualization, Extras, and Wireless modules. A docstring explaining its usage and an example were included.

Created `tests/test_types.py` with unit tests to verify the structure of `NETBOX_OBJECT_TYPES`. The tests check for the presence of key expected types and ensure that endpoint paths are correctly formatted and non-empty.

**Uncertainties:**
- Verification of tests and `lsp_diagnostics` could not be performed in this environment due to the lack of a Python interpreter and language server. This has been noted in `issues.md`. Manual verification will be required on a suitable environment.

## Decisions Log

- **NETBOX_OBJECT_TYPES structure**: Chose a `Dict[str, str]` mapping object type strings (e.g., 'dcim.sites') to endpoint path strings (e.g., 'dcim/sites') for direct translation. This provides a clear and deterministic way to access endpoint paths.
