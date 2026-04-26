import unittest
from unittest.mock import patch, MagicMock
import requests
import time

from netbox_mcp_server.client import NetBoxRestClient

class TestNetBoxRestClient(unittest.TestCase):

    def setUp(self):
        """Set up a mock session and client for tests."""
        self.base_url = "http://netbox.example.com"
        self.token = "test_token"
        self.client = NetBoxRestClient(self.base_url, self.token, timeout=5, rate_limit=0) # rate_limit=0 for faster tests
        self.client.session = MagicMock(requests.Session) # Mock the session object

    @patch('requests.Session.request')
    def test_authorization_header_injected(self, mock_request):
        """Verify that the Authorization header is correctly injected."""
        mock_response = MagicMock(requests.Response)
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        self.client.get("/api/dcim/sites/")

        mock_request.assert_called_once()
        # Check if the call to session.request included the correct Authorization header
        call_args, call_kwargs = mock_request.call_args
        self.assertIn('headers', call_kwargs)
        self.assertEqual(call_kwargs['headers'].get('Authorization'), f"Token {self.token}")

    @patch('requests.Session.request')
    def test_retry_on_5xx_then_success(self, mock_request):
        """Verify that the client retries on 5xx errors and succeeds on the next attempt."""
        mock_response_500 = MagicMock(requests.Response)
        mock_response_500.status_code = 503
        mock_response_500.raise_for_status.side_effect = requests.exceptions.HTTPError("503 Service Unavailable")

        mock_response_200 = MagicMock(requests.Response)
        mock_response_200.status_code = 200
        mock_response_200.raise_for_status.return_value = None

        # Configure mock_request to return 503 twice, then 200
        mock_request.side_effect = [mock_response_500, mock_response_500, mock_response_200]

        # Use a patch for time.sleep to prevent actual delays during test
        with patch('time.sleep') as mock_sleep:
            response = self.client.get("/api/dcim/sites/")

            self.assertEqual(response.status_code, 200)
            # Should be called 3 times (initial + 2 retries)
            self.assertEqual(mock_request.call_count, 3)
            # Verify that time.sleep was called for backoff
            self.assertEqual(mock_sleep.call_count, 2) # Called twice for the two retries

    @patch('requests.Session.request')
    def test_connection_error_handling(self, mock_request):
        """Verify that connection errors are raised without accessing undefined response."""
        # Configure mock_request to raise a ConnectionError
        mock_request.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        # Expecting a RequestException to be raised
        with self.assertRaises(requests.exceptions.RequestException) as cm:
            self.client.get("/api/dcim/sites/")

        self.assertEqual(str(cm.exception), "Failed to connect")
        mock_request.assert_called_once() # Should only attempt the request once before raising

    @patch('requests.Session.request')
    def test_non_retryable_error_handling(self, mock_request):
        """Verify that non-5xx errors (e.g., 404) are not retried."""
        mock_response_404 = MagicMock(requests.Response)
        mock_response_404.status_code = 404
        mock_response_404.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

        mock_request.return_value = mock_response_404

        with self.assertRaises(requests.exceptions.HTTPError) as cm:
            self.client.get("/api/dcim/sites/")

        self.assertEqual(str(cm.exception), "404 Not Found")
        mock_request.assert_called_once() # Should only attempt the request once

if __name__ == '__main__':
    unittest.main()
