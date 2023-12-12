# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulpcore.configuration import Configuration


class UserRole(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'role': 'str',
        'content_object': 'str',
        'domain': 'str'
    }

    attribute_map = {
        'role': 'role',
        'content_object': 'content_object',
        'domain': 'domain'
    }

    def __init__(self, role=None, content_object=None, domain=None, local_vars_configuration=None):  # noqa: E501
        """UserRole - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._role = None
        self._content_object = None
        self._domain = None
        self.discriminator = None

        self.role = role
        self.content_object = content_object
        self.domain = domain

    @property
    def role(self):
        """Gets the role of this UserRole.  # noqa: E501


        :return: The role of this UserRole.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this UserRole.


        :param role: The role of this UserRole.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and role is None:  # noqa: E501
            raise ValueError("Invalid value for `role`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                role is not None and len(role) < 1):
            raise ValueError("Invalid value for `role`, length must be greater than or equal to `1`")  # noqa: E501

        self._role = role

    @property
    def content_object(self):
        """Gets the content_object of this UserRole.  # noqa: E501

        pulp_href of the object for which role permissions should be asserted. If set to 'null', permissions will act on either domain or model-level.  # noqa: E501

        :return: The content_object of this UserRole.  # noqa: E501
        :rtype: str
        """
        return self._content_object

    @content_object.setter
    def content_object(self, content_object):
        """Sets the content_object of this UserRole.

        pulp_href of the object for which role permissions should be asserted. If set to 'null', permissions will act on either domain or model-level.  # noqa: E501

        :param content_object: The content_object of this UserRole.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                content_object is not None and len(content_object) < 1):
            raise ValueError("Invalid value for `content_object`, length must be greater than or equal to `1`")  # noqa: E501

        self._content_object = content_object

    @property
    def domain(self):
        """Gets the domain of this UserRole.  # noqa: E501

        Domain this role should be applied on, mutually exclusive with content_object.  # noqa: E501

        :return: The domain of this UserRole.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this UserRole.

        Domain this role should be applied on, mutually exclusive with content_object.  # noqa: E501

        :param domain: The domain of this UserRole.  # noqa: E501
        :type: str
        """

        self._domain = domain

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UserRole):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserRole):
            return True

        return self.to_dict() != other.to_dict()
