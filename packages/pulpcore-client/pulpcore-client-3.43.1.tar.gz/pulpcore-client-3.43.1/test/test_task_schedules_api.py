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

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.api.task_schedules_api import TaskSchedulesApi  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException


class TestTaskSchedulesApi(unittest.TestCase):
    """TaskSchedulesApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulpcore.api.task_schedules_api.TaskSchedulesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_role(self):
        """Test case for add_role

        Add a role  # noqa: E501
        """
        pass

    def test_list(self):
        """Test case for list

        List task schedules  # noqa: E501
        """
        pass

    def test_list_roles(self):
        """Test case for list_roles

        List roles  # noqa: E501
        """
        pass

    def test_my_permissions(self):
        """Test case for my_permissions

        List user permissions  # noqa: E501
        """
        pass

    def test_read(self):
        """Test case for read

        Inspect a task schedule  # noqa: E501
        """
        pass

    def test_remove_role(self):
        """Test case for remove_role

        Remove a role  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
