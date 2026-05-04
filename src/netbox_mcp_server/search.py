"""Search utilities for NetBox MCP.

Provides netbox_search_objects which performs a simple global search across
multiple NetBox object endpoints using the provided NetBoxRestClient.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Dict, Any, Tuple

from .types import NETBOX_OBJECT_TYPES


def _search_endpoint(
    client, obj_type: str, endpoint: str, q: str, limit: int
) -> Tuple[int, List[Dict[str, Any]]]:
    """Fetch search results from a single NetBox endpoint (parallel worker).

    Uses client.session directly to bypass rate limiting — GET search is
    read-only and does not need throttling.

    Args:
        client: NetBoxRestClient instance.
        obj_type: dotted object type key (e.g. 'dcim.sites').
        endpoint: URL path segment (e.g. 'dcim/sites').
        q: search query string.
        limit: max results per endpoint.

    Returns:
        Tuple of (count, list_of_annotated_results). Returns (0, []) on failure.
    """
    path = f"/{endpoint}/"
    params = {"q": q, "limit": limit, "offset": 0}
    try:
        url = f"{client.base_url}{path}"
        resp = client.session.get(
            url,
            params=params,
            timeout=client.timeout,
            verify=client.ssl_verify,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return (0, [])

    results = data.get("results") or []
    count = data.get("count") or len(results)

    annotated = []
    for item in results:
        item["_mcp_object_type"] = obj_type
        annotated.append(item)

    return (count, annotated)


def netbox_search_objects(client, q: str, limit: int = 50, offset: int = 0, object_type: Optional[str] = None) -> Dict[str, Any]:
    """Search across NetBox object endpoints (parallel execution).

    Fetches all matching endpoints concurrently via ThreadPoolExecutor,
    bypassing the client's per-request rate limiting since GET search is
    read-only.

    Args:
        client: an instance of NetBoxRestClient (or compatible) with a `get(path, params)` method.
        q: search query string
        limit: maximum number of items to return overall (best-effort)
        offset: offset into the aggregated results (best-effort)
        object_type: optional specific object type key (e.g. 'dcim.sites') to limit the search

    Returns:
        A dict with keys: total (int), results (list of items with additional metadata)
    """
    endpoints = {}
    if object_type:
        if object_type not in NETBOX_OBJECT_TYPES:
            raise ValueError(f"unknown object_type: {object_type}")
        endpoints[object_type] = NETBOX_OBJECT_TYPES[object_type]
    else:
        endpoints = NETBOX_OBJECT_TYPES.copy()

    aggregated: List[Dict[str, Any]] = []
    total = 0

    with ThreadPoolExecutor(max_workers=10) as pool:
        future_map = {
            pool.submit(_search_endpoint, client, ot, ep, q, limit): ot
            for ot, ep in endpoints.items()
        }

        for future in as_completed(future_map):
            count, results = future.result()
            total += count
            aggregated.extend(results)

            # Early stop once we've accumulated enough results.
            # Cannot cancel already-running threads, but we stop consuming.
            if len(aggregated) >= (offset + limit):
                break

    # apply offset and limit to aggregated results
    sliced = aggregated[offset: offset + limit]

    return {"total": total, "results": sliced}
