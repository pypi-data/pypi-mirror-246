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


class UpstreamPulp(object):
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
        'name': 'str',
        'base_url': 'str',
        'api_root': 'str',
        'domain': 'str',
        'ca_cert': 'str',
        'client_cert': 'str',
        'client_key': 'str',
        'tls_validation': 'bool',
        'username': 'str',
        'password': 'str',
        'pulp_label_select': 'str'
    }

    attribute_map = {
        'name': 'name',
        'base_url': 'base_url',
        'api_root': 'api_root',
        'domain': 'domain',
        'ca_cert': 'ca_cert',
        'client_cert': 'client_cert',
        'client_key': 'client_key',
        'tls_validation': 'tls_validation',
        'username': 'username',
        'password': 'password',
        'pulp_label_select': 'pulp_label_select'
    }

    def __init__(self, name=None, base_url=None, api_root=None, domain=None, ca_cert=None, client_cert=None, client_key=None, tls_validation=None, username=None, password=None, pulp_label_select=None, local_vars_configuration=None):  # noqa: E501
        """UpstreamPulp - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._base_url = None
        self._api_root = None
        self._domain = None
        self._ca_cert = None
        self._client_cert = None
        self._client_key = None
        self._tls_validation = None
        self._username = None
        self._password = None
        self._pulp_label_select = None
        self.discriminator = None

        self.name = name
        self.base_url = base_url
        self.api_root = api_root
        self.domain = domain
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.client_key = client_key
        if tls_validation is not None:
            self.tls_validation = tls_validation
        self.username = username
        self.password = password
        self.pulp_label_select = pulp_label_select

    @property
    def name(self):
        """Gets the name of this UpstreamPulp.  # noqa: E501

        A unique name for this Pulp server.  # noqa: E501

        :return: The name of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpstreamPulp.

        A unique name for this Pulp server.  # noqa: E501

        :param name: The name of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def base_url(self):
        """Gets the base_url of this UpstreamPulp.  # noqa: E501

        The transport, hostname, and an optional port of the Pulp server. e.g. https://example.com  # noqa: E501

        :return: The base_url of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        """Sets the base_url of this UpstreamPulp.

        The transport, hostname, and an optional port of the Pulp server. e.g. https://example.com  # noqa: E501

        :param base_url: The base_url of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and base_url is None:  # noqa: E501
            raise ValueError("Invalid value for `base_url`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                base_url is not None and len(base_url) < 1):
            raise ValueError("Invalid value for `base_url`, length must be greater than or equal to `1`")  # noqa: E501

        self._base_url = base_url

    @property
    def api_root(self):
        """Gets the api_root of this UpstreamPulp.  # noqa: E501

        The API root. Defaults to '/pulp/'.  # noqa: E501

        :return: The api_root of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._api_root

    @api_root.setter
    def api_root(self, api_root):
        """Sets the api_root of this UpstreamPulp.

        The API root. Defaults to '/pulp/'.  # noqa: E501

        :param api_root: The api_root of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and api_root is None:  # noqa: E501
            raise ValueError("Invalid value for `api_root`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                api_root is not None and len(api_root) < 1):
            raise ValueError("Invalid value for `api_root`, length must be greater than or equal to `1`")  # noqa: E501

        self._api_root = api_root

    @property
    def domain(self):
        """Gets the domain of this UpstreamPulp.  # noqa: E501

        The domain of the Pulp server if enabled.  # noqa: E501

        :return: The domain of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this UpstreamPulp.

        The domain of the Pulp server if enabled.  # noqa: E501

        :param domain: The domain of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                domain is not None and len(domain) < 1):
            raise ValueError("Invalid value for `domain`, length must be greater than or equal to `1`")  # noqa: E501

        self._domain = domain

    @property
    def ca_cert(self):
        """Gets the ca_cert of this UpstreamPulp.  # noqa: E501

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :return: The ca_cert of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._ca_cert

    @ca_cert.setter
    def ca_cert(self, ca_cert):
        """Sets the ca_cert of this UpstreamPulp.

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :param ca_cert: The ca_cert of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                ca_cert is not None and len(ca_cert) < 1):
            raise ValueError("Invalid value for `ca_cert`, length must be greater than or equal to `1`")  # noqa: E501

        self._ca_cert = ca_cert

    @property
    def client_cert(self):
        """Gets the client_cert of this UpstreamPulp.  # noqa: E501

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :return: The client_cert of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._client_cert

    @client_cert.setter
    def client_cert(self, client_cert):
        """Sets the client_cert of this UpstreamPulp.

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :param client_cert: The client_cert of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                client_cert is not None and len(client_cert) < 1):
            raise ValueError("Invalid value for `client_cert`, length must be greater than or equal to `1`")  # noqa: E501

        self._client_cert = client_cert

    @property
    def client_key(self):
        """Gets the client_key of this UpstreamPulp.  # noqa: E501

        A PEM encoded private key used for authentication.  # noqa: E501

        :return: The client_key of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._client_key

    @client_key.setter
    def client_key(self, client_key):
        """Sets the client_key of this UpstreamPulp.

        A PEM encoded private key used for authentication.  # noqa: E501

        :param client_key: The client_key of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                client_key is not None and len(client_key) < 1):
            raise ValueError("Invalid value for `client_key`, length must be greater than or equal to `1`")  # noqa: E501

        self._client_key = client_key

    @property
    def tls_validation(self):
        """Gets the tls_validation of this UpstreamPulp.  # noqa: E501

        If True, TLS peer validation must be performed.  # noqa: E501

        :return: The tls_validation of this UpstreamPulp.  # noqa: E501
        :rtype: bool
        """
        return self._tls_validation

    @tls_validation.setter
    def tls_validation(self, tls_validation):
        """Sets the tls_validation of this UpstreamPulp.

        If True, TLS peer validation must be performed.  # noqa: E501

        :param tls_validation: The tls_validation of this UpstreamPulp.  # noqa: E501
        :type: bool
        """

        self._tls_validation = tls_validation

    @property
    def username(self):
        """Gets the username of this UpstreamPulp.  # noqa: E501

        The username to be used for authentication when syncing.  # noqa: E501

        :return: The username of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this UpstreamPulp.

        The username to be used for authentication when syncing.  # noqa: E501

        :param username: The username of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                username is not None and len(username) < 1):
            raise ValueError("Invalid value for `username`, length must be greater than or equal to `1`")  # noqa: E501

        self._username = username

    @property
    def password(self):
        """Gets the password of this UpstreamPulp.  # noqa: E501

        The password to be used for authentication when syncing. Extra leading and trailing whitespace characters are not trimmed.  # noqa: E501

        :return: The password of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this UpstreamPulp.

        The password to be used for authentication when syncing. Extra leading and trailing whitespace characters are not trimmed.  # noqa: E501

        :param password: The password of this UpstreamPulp.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                password is not None and len(password) < 1):
            raise ValueError("Invalid value for `password`, length must be greater than or equal to `1`")  # noqa: E501

        self._password = password

    @property
    def pulp_label_select(self):
        """Gets the pulp_label_select of this UpstreamPulp.  # noqa: E501

        One or more comma separated labels that will be used to filter distributions on the upstream Pulp. E.g. \"foo=bar,key=val\" or \"foo,key\"  # noqa: E501

        :return: The pulp_label_select of this UpstreamPulp.  # noqa: E501
        :rtype: str
        """
        return self._pulp_label_select

    @pulp_label_select.setter
    def pulp_label_select(self, pulp_label_select):
        """Sets the pulp_label_select of this UpstreamPulp.

        One or more comma separated labels that will be used to filter distributions on the upstream Pulp. E.g. \"foo=bar,key=val\" or \"foo,key\"  # noqa: E501

        :param pulp_label_select: The pulp_label_select of this UpstreamPulp.  # noqa: E501
        :type: str
        """

        self._pulp_label_select = pulp_label_select

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
        if not isinstance(other, UpstreamPulp):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpstreamPulp):
            return True

        return self.to_dict() != other.to_dict()
