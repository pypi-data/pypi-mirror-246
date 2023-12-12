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
import datetime

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.models.remote_response_hidden_fields import RemoteResponseHiddenFields  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException

class TestRemoteResponseHiddenFields(unittest.TestCase):
    """RemoteResponseHiddenFields unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RemoteResponseHiddenFields
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulpcore.models.remote_response_hidden_fields.RemoteResponseHiddenFields()  # noqa: E501
        if include_optional :
            return RemoteResponseHiddenFields(
                name = '0', 
                is_set = True
            )
        else :
            return RemoteResponseHiddenFields(
        )

    def testRemoteResponseHiddenFields(self):
        """Test RemoteResponseHiddenFields"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
