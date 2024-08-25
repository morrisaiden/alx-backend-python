#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.

This module contains tests to verify that the GithubOrgClient class
properly fetches organization data using the get_json method and
returns the correct values.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.

    This class includes tests to ensure that the org method of
    GithubOrgClient returns the correct value and behaves as expected
    when interacting with the get_json method.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): The name of the GitHub organization to test.
            mock_get_json (Mock): The mocked get_json function.

        This method verifies that the org method of GithubOrgClient
        returns the correct data and that get_json is called once with
        the expected URL.
        """
        mock_get_json.return_value = {"name": org_name}

        client = GithubOrgClient(org_name)

        result = client.org

        # Verify that get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}'
        )

        # Verify that the result is correct
        self.assertEqual(result, {"name": org_name})


if __name__ == "__main__":
    unittest.main()
