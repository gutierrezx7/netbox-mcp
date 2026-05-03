import typing

NETBOX_OBJECT_TYPES: typing.Dict[str, str] = {
    # DCIM
    "dcim.sites": "dcim/sites",
    "dcim.racks": "dcim/racks",
    "dcim.devices": "dcim/devices",
    "dcim.device-roles": "dcim/device-roles",
    "dcim.device-types": "dcim/device-types",
    "dcim.manufacturers": "dcim/manufacturers",
    "dcim.platforms": "dcim/platforms",
    "dcim.cables": "dcim/cables",
    "dcim.cable-lengths": "dcim/cable-lengths",
    "dcim.console-servers": "dcim/console-servers",
    "dcim.console-server-ports": "dcim/console-server-ports",
    "dcim.power-panels": "dcim/power-panels",
    "dcim.power-feeds": "dcim/power-feeds",
    "dcim.power-outlets": "dcim/power-outlets",
    "dcim.power-ports": "dcim/power-ports",
    "dcim.front-ports": "dcim/front-ports",
    "dcim.rear-ports": "dcim/rear-ports",
    "dcim.interface-connections": "dcim/interface-connections",
    "dcim.locations": "dcim/locations",
    "dcim.modules": "dcim/modules",
    "dcim.inventory-items": "dcim/inventory-items",
    "dcim.certificates": "dcim/certificates",
    "dcim.certificate-templates": "dcim/certificate-templates",
    "dcim.device-bays": "dcim/device-bays",
    "dcim.rack-groups": "dcim/rack-groups",
    "dcim.rack-roles": "dcim/rack-roles",

    # IPAM
    "ipam.ip-addresses": "ipam/ip-addresses",
    "ipam.ip-ranges": "ipam/ip-ranges",
    "ipam.prefixes": "ipam/prefixes",
    "ipam.vlans": "ipam/vlans",
    "ipam.vrfs": "ipam/vrfs",
    "ipam.aggregates": "ipam/aggregates",
    "ipam.rirs": "ipam/rirs",
    "ipam.fhrp-groups": "ipam/fhrp-groups",
    "ipam.vlan-groups": "ipam/vlan-groups",

    # Circuits
    "circuits.circuit-types": "circuits/circuit-types",
    "circuits.circuits": "circuits/circuits",
    "circuits.provider-networks": "circuits/provider-networks",
    "circuits.providers": "circuits/providers",

    # Tenancy
    "tenancy.tenants": "tenancy/tenants",
    "tenancy.tenant-groups": "tenancy/tenant-groups",

    # Virtualization
    "virtualization.cluster-types": "virtualization/cluster-types",
    "virtualization.clusters": "virtualization/clusters",
    "virtualization.virtual-machines": "virtualization/virtual-machines",
    "virtualization.services": "virtualization/services",
    "virtualization.platforms": "virtualization/platforms",

    # Extras
    "extras.tags": "extras/tags",
    "extras.custom-fields": "extras/custom-fields",
    "extras.custom-links": "extras/custom-links",
    "extras.export-templates": "extras/export-templates",
    "extras.image-attachments": "extras/image-attachments",
    "extras.job-results": "extras/job-results",
    "extras.reports": "extras/reports",
    "extras.statuses": "extras/statuses",

    # Wireless
    "wireless.wireless-lans": "wireless/wireless-lans",
    "wireless.wireless-links": "wireless/wireless-links",
}
