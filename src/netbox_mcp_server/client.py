import time
import typing
import requests
from netbox_mcp_server.config import get_settings

class NetBoxRestClient:
    """
    A REST client for interacting with the NetBox API.

    Handles authentication, request methods, timeouts, retries, and rate limiting.
    """

    def __init__(self, base_url: str, token: str, timeout: int = 10, rate_limit: int = 1, ssl_verify: bool = True):
        """
        Initializes the NetBoxRestClient.

        Args:
            base_url: The base URL of the NetBox API.
            token: The API token for authentication.
            timeout: The request timeout in seconds. Defaults to 10.
            rate_limit: The minimum delay in seconds between requests. Defaults to 1.
        """
        self.base_url = base_url
        self.token = token
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.ssl_verify = ssl_verify
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.last_request_time = 0

    def _apply_rate_limiting(self):
        """Ensures the rate limit is respected between requests."""
        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < self.rate_limit:
            time.sleep(self.rate_limit - elapsed_time)
        self.last_request_time = time.time()

    def request(self, method: str, path: str, json: typing.Optional[dict] = None, params: typing.Optional[dict] = None) -> requests.Response:
        """
        Performs an HTTP request to the NetBox API with retry logic.

        Args:
            method: The HTTP method (e.g., "GET", "POST", "PATCH", "DELETE").
            path: The API path (e.g., "/dcim/sites/").
            json: The JSON payload for the request.
            params: The URL parameters for the request.

        Returns:
            The requests.Response object.

        Raises:
            requests.exceptions.RequestException: If the request fails after retries.
        """
        url = f"{self.base_url}{path}"
        retries = 3
        response = None  # Initialize response to None
        for attempt in range(retries):
            self._apply_rate_limiting()
            try:
                response = self.session.request(
                    method,
                    url,
                    json=json,
                    params=params,
                    timeout=self.timeout,
                    verify=self.ssl_verify,
                )
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                return response
            except requests.exceptions.RequestException as e:
                # Check if response is defined and if it's a retryable status code
                if attempt < retries - 1 and response is not None and response.status_code >= 500:
                    # Retry on server errors (5xx)
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    # If response is not defined, or it's not a retryable error, or max retries reached, raise the exception.
                    # This also covers connection errors where 'response' is not available.
                    raise e

    def get(self, path: str, params: typing.Optional[dict] = None) -> requests.Response:
        """Sends a GET request."""
        return self.request("GET", path, params=params)

    def post(self, path: str, json: dict) -> requests.Response:
        """Sends a POST request."""
        return self.request("POST", path, json=json)

    def patch(self, path: str, json: dict) -> requests.Response:
        """Sends a PATCH request."""
        return self.request("PATCH", path, json=json)

    def delete(self, path: str) -> requests.Response:
        """Sends a DELETE request."""
        return self.request("DELETE", path)

# Example usage (for demonstration, not part of the final code)
# if __name__ == "__main__":
#     settings = get_settings()
#     client = NetBoxRestClient(
#         base_url=settings.NETBOX_API_URL,
#         token=settings.NETBOX_API_TOKEN,
#         timeout=settings.NETBOX_API_TIMEOUT,
#         rate_limit=settings.NETBOX_API_RATE_LIMIT
#     )
#     try:
#         response = client.get("/dcim/sites/")
#         print(response.json())
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
