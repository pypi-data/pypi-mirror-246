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
from pulpcore.client.pulpcore.models.domain import Domain  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException

class TestDomain(unittest.TestCase):
    """Domain unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Domain
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulpcore.models.domain.Domain()  # noqa: E501
        if include_optional :
            return Domain(
                name = 'a', 
                description = '0', 
                storage_class = null, 
                storage_settings = None, 
                redirect_to_object_storage = True, 
                hide_guarded_distributions = True
            )
        else :
            return Domain(
                name = 'a',
                storage_class = null,
                storage_settings = None,
        )

    def testDomain(self):
        """Test Domain"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
