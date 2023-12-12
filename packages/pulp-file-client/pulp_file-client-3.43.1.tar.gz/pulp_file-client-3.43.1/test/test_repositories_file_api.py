# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_file
from pulpcore.client.pulp_file.api.repositories_file_api import RepositoriesFileApi  # noqa: E501
from pulpcore.client.pulp_file.rest import ApiException


class TestRepositoriesFileApi(unittest.TestCase):
    """RepositoriesFileApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_file.api.repositories_file_api.RepositoriesFileApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_role(self):
        """Test case for add_role

        Add a role  # noqa: E501
        """
        pass

    def test_create(self):
        """Test case for create

        Create a file repository  # noqa: E501
        """
        pass

    def test_delete(self):
        """Test case for delete

        Delete a file repository  # noqa: E501
        """
        pass

    def test_list(self):
        """Test case for list

        List file repositorys  # noqa: E501
        """
        pass

    def test_list_roles(self):
        """Test case for list_roles

        List roles  # noqa: E501
        """
        pass

    def test_modify(self):
        """Test case for modify

        Modify Repository Content  # noqa: E501
        """
        pass

    def test_my_permissions(self):
        """Test case for my_permissions

        List user permissions  # noqa: E501
        """
        pass

    def test_partial_update(self):
        """Test case for partial_update

        Update a file repository  # noqa: E501
        """
        pass

    def test_read(self):
        """Test case for read

        Inspect a file repository  # noqa: E501
        """
        pass

    def test_remove_role(self):
        """Test case for remove_role

        Remove a role  # noqa: E501
        """
        pass

    def test_set_label(self):
        """Test case for set_label

        Set a label  # noqa: E501
        """
        pass

    def test_sync(self):
        """Test case for sync

        Sync from a remote  # noqa: E501
        """
        pass

    def test_unset_label(self):
        """Test case for unset_label

        Unset a label  # noqa: E501
        """
        pass

    def test_update(self):
        """Test case for update

        Update a file repository  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
