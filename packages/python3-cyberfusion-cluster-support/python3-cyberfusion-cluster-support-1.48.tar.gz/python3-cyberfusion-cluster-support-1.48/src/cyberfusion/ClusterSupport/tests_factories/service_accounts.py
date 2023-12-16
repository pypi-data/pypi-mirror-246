"""Factories for API object."""

import factory
import factory.fuzzy

from cyberfusion.ClusterSupport.service_accounts import (
    ServiceAccount,
    ServiceAccountGroup,
)
from cyberfusion.ClusterSupport.tests_factories import BaseBackendFactory


class ServiceAccountFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccount

        exclude = ("site",)

    name = factory.Faker("domain_name")
    group = ServiceAccountGroup.MAIL_PROXY
    default_ipv6_ip_address = None
    default_ipv4_ip_address = None
    default_ipv6_netbox_id = None
    default_ipv4_netbox_id = None
    netbox_additional_prefix_ipv4_id = None
    netbox_fhrp_group_ipv6_id = None
    netbox_fhrp_group_ipv4_id = None
    netbox_additional_prefix_ipv6_id = None
    site = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites.SiteFactory",
    )
    site_id = factory.SelfAttribute("site.id")


class ServiceAccountInternetRouterFactory(BaseBackendFactory):
    """Factory for specific object."""

    class Meta:
        """Settings."""

        model = ServiceAccount

        exclude = ("site",)

    name = factory.Faker("domain_name")
    group = ServiceAccountGroup.INTERNET_ROUTER
    default_ipv6_ip_address = factory.Faker("ipv6")
    default_ipv4_ip_address = factory.Faker("ipv4")
    default_ipv6_netbox_id = factory.Faker("random_int", min=500, max=2000)
    default_ipv4_netbox_id = factory.Faker("random_int", min=500, max=2000)
    netbox_additional_prefix_ipv6_id = factory.Faker(
        "random_int", min=500, max=2000
    )
    netbox_additional_prefix_ipv4_id = factory.Faker(
        "random_int", min=500, max=2000
    )
    netbox_fhrp_group_ipv6_id = factory.Faker("random_int", min=500, max=2000)
    netbox_fhrp_group_ipv4_id = factory.Faker("random_int", min=500, max=2000)
    site = factory.SubFactory(
        "cyberfusion.ClusterSupport.tests_factories.sites.SiteFactory",
    )
    site_id = factory.SelfAttribute("site.id")
