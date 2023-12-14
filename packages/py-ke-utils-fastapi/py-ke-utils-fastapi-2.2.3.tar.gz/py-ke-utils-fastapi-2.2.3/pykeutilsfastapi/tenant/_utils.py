import logging
import re
from pyframelessutils.token_utilities import token_parser


def tenant_extractor(token: str, default_tenant: str = 'public'):
    """
    Function to extract tenant from Origin/Header or assign default
    :param token: token to fetch tenant from
    :param default_tenant: default tenant value
    :return:
    """
    subdomain = default_tenant

    if match := re.search(
            r"/realms/([^/]+)",
            token_parser(token, "iss"),
    ):
        subdomain = match[1]
    logging.info("Tenant selected: %s", subdomain)
    return subdomain
