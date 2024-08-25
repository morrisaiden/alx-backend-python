#!/usr/bin/env python3
"""
Unittests for the GithubOrgClient class.
"""

import unittest
from unittest import TestCase
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from urllib.error import HTTPError
from parameterized import parameterized_class


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
        
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)])
    def test_has_license(self, repo, license_key, ret):
        """Method to test GithubOrgClient.has_license function"""

        client = GithubOrgClient("Test value")
        res = client.has_license(repo, license_key)
        self.assertEqual(ret, res)


@parameterized_class(("org_payload", "repos_payload", "expected_repos",
                     "apache2_repos"), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(TestCase):
    """Class that defines attributes to test client.GithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """Method to prepare test fixture"""

        cls.get_patcher = patch('requests.get', side_effect=HTTPError)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Method called after test method has been called"""

        cls.get_patcher.stop()

    def test_public_repos(self):
        """Method to test GithubOrgClient.public_repos function"""

        res = GithubOrgClient("Test value")
        self.assertTrue(res)


if __name__ == "__main__":
    unittest.main()
