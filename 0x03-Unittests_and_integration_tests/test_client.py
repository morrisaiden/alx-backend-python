#!/usr/bin/env python3
"""
Unittests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
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

        client = GithubOrgClient(org_name)

        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, {"login": "mock_org"})

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that GithubOrgClient._public_repos_url returns the correct URL
        based on the mocked org payload.
        """

        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/mock_org/repos"
            }

        client = GithubOrgClient("mock_org")

        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/mock_org/repos")


if __name__ == "__main__":
    unittest.main()
