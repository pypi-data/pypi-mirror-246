# coding: utf-8

import types
import six

from fecloudsdkcore.region.region import Region
from fecloudsdkcore.region.provider import RegionProviderChain

class KmsRegion:
    _PROVIDER = RegionProviderChain.get_default_region_provider_chain("KMS")

    EU_WEST_0 = Region("eu-west-0",
                        "https://kms.eu-west-0.prod-cloud-ocb.orange-business.com")

    static_fields = {
        "eu-west-0": EU_WEST_0,
    }

    @classmethod
    def value_of(cls, region_id, static_fields=None):
        if not region_id:
            raise KeyError("Unexpected empty parameter: region_id.")

        fields = static_fields if static_fields else cls.static_fields

        region = cls._PROVIDER.get_region(region_id)
        if region:
            return region

        if region_id in fields:
            return fields.get(region_id)

        raise KeyError("Unexpected region_id: " + region_id)


