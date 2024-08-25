#!/usr/bin/env python3
"""
Unit tests for utils module.

This module includes tests for the memoize decorator and
access_nested_map function, ensuring proper functionality
and correct behavior under various conditions.
"""

import unittest
from client import GithubOrgClient
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import memoize, access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """
    Tests for the access_nested_map function.

    This class includes tests to ensure the correct behavior
    of the access_nested_map function when given various
    nested map inputs and paths.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: dict,
                               path: tuple,
                               expected: any) -> None:
        """
        Tests access_nested_map with valid inputs.

        Args:
            nested_map (dict): The nested map to test.
            path (tuple): The path to access.
            expected (any): The expected result.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: dict,
                                         path: tuple) -> None:
        """
        Tests access_nested_map with invalid inputs.

        Args:
            nested_map (dict): The nested map to test.
            path (tuple): The path to access.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """
    Tests for the get_json function.

    This class includes tests to ensure the correct behavior
    of the get_json function when handling various URLs and
    expected payloads.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """
        Tests get_json with various URLs and payloads.

        Args:
            test_url (str): The URL to test.
            test_payload (dict): The expected JSON payload.
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Tests for the memoize decorator.

    This class includes tests to ensure that the memoize
    decorator properly caches results of method calls.
    """

    def test_memoize(self) -> None:
        """
        Tests that memoize decorator caches results of method calls.

        Uses a mock method to ensure that memoization works correctly
        by checking that the method is called only once despite
        multiple accesses.
        """
        class TestClass:
            def a_method(self) -> int:
                """Returns the number 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Returns the result of a_method."""
                return self.a_method()

        test_instance = TestClass()

        with patch.object(test_instance,
                          'a_method',
                          return_value=42) as mock_method:
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            mock_method.assert_called_once()
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.

    This class includes tests to ensure that the org method of
    GithubOrgClient returns the correct value and behaves as expected
    when interacting with the get_json method.
    """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): The name of the GitHub organization to test.
            mock_get_json (Mock): The mocked get_json function
        """
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        result = client.org

        # verify that the get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}'
            )

        self.assertEqual(result, {"name": org_name})


if __name__ == "__main__":
    unittest.main()
