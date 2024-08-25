#!/usr/bin/env python3
"""
Unittests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json', return_value={"login": "mock_org"})
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): The organization name to test.
            mock_get_json (MagicMock): Mocked version of get_json.
        """
        # Create an instance of GithubOrgClient with the provided org_name
        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org

        # Check that get_json was called once with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Check that the returned value is as expected
        self.assertEqual(result, {"login": "mock_org"})


if __name__ == "__main__":
    unittest.main()
