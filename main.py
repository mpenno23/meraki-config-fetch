import meraki
import os
import json

from dotenv import load_dotenv


def get_config(network_id, output_file, dashboard, organization_id):
    # PLEASE NOTE SOME OF THESE CALLS REQUIRE OTHER VARIABLES LISTED BELOW
    serial = 0
    port_id = 0
    static_delegated_prefix_id = 0
    rf_profile_id = 0
    static_route_id = 0
    custom_performance_class_id = 0
    vlan_id = 0

    # list of API calls to GET information from the MX
    api_calls = [("getNetworkApplianceConnectivityMonitoringDestinations", (network_id,)),
                 ("getNetworkApplianceContentFiltering", (network_id,)),
                 ("getNetworkApplianceFirewallCellularFirewallRules", (network_id,)),
                 ("getNetworkApplianceFirewallFirewalledServices", (network_id,)),
                 ("getNetworkApplianceFirewallFirewalledService", (network_id, 'ICMP')),
                 ("getNetworkApplianceFirewallFirewalledService", (network_id, 'SNMP')),
                 ("getNetworkApplianceFirewallFirewalledService", (network_id, 'web')),
                 ("getNetworkApplianceFirewallInboundCellularFirewallRules", (network_id,)),
                 ("getNetworkApplianceFirewallInboundFirewallRules", (network_id,)),
                 ("getNetworkApplianceFirewallL3FirewallRules", (network_id,)),
                 ("getNetworkApplianceFirewallL7FirewallRules", (network_id,)),
                 ("getNetworkApplianceFirewallL7FirewallRulesApplicationCategories", (network_id,)),
                 ("getNetworkApplianceFirewallOneToManyNatRules", (network_id,)),
                 ("getNetworkApplianceFirewallOneToOneNatRules", (network_id,)),
                 ("getNetworkApplianceFirewallPortForwardingRules", (network_id,)),
                 ("getNetworkApplianceFirewallSettings", (network_id,)),  # Removed "firewallOptions = "
                 ("getNetworkAppliancePorts", (network_id,)),
                 ("getNetworkAppliancePort", (network_id, port_id)),  # Assuming port_id is defined
                 ("getNetworkAppliancePrefixesDelegatedStatics", (network_id,)),
                 ("getNetworkAppliancePrefixesDelegatedStatic", (network_id, static_delegated_prefix_id)),
                 # Assuming static_delegated_prefix_id is defined
                 ("getDeviceApplianceRadioSettings", (serial,)),  # Assuming serial is defined
                 ("getNetworkApplianceRfProfiles", (network_id,)),
                 ("getNetworkApplianceRfProfile", (network_id, rf_profile_id)),  # Assuming rf_profile_id is defined
                 ("getNetworkApplianceSecurityIntrusion", (network_id,)),
                 ("getOrganizationApplianceSecurityIntrusion", (organization_id,)),
                 ("getNetworkApplianceSecurityMalware", (network_id,)),
                 ("getNetworkApplianceSingleLan", (network_id,)),
                 ("getNetworkApplianceSsids", (network_id,)),
                 ("getNetworkApplianceStaticRoutes", (network_id,)),
                 ("getNetworkApplianceStaticRoute", (network_id, static_route_id)),
                 ("getNetworkApplianceTrafficShaping", (network_id,)),
                 ("getNetworkApplianceTrafficShapingCustomPerformanceClasses", (network_id,)),
                 ("getNetworkApplianceTrafficShapingCustomPerformanceClass", (network_id, custom_performance_class_id)),
                 ("getNetworkApplianceTrafficShapingRules", (network_id,)),
                 ("getNetworkApplianceTrafficShapingUplinkBandwidth", (network_id,)),
                 ("getNetworkApplianceTrafficShapingUplinkSelection", (network_id,)),
                 ("getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork", (organization_id, 'all')),
                 ("getDeviceApplianceUplinksSettings", (serial,)),
                 ("getNetworkApplianceVlans", (network_id,)),
                 ("getNetworkApplianceVlan", (network_id, vlan_id)),
                 ("getNetworkApplianceVlansSettings", (network_id,)),
                 ("getNetworkApplianceVpnBgp", (network_id,)),
                 ("getNetworkApplianceVpnSiteToSiteVpn", (network_id,)),
                 ("getOrganizationApplianceVpnThirdPartyVPNPeers", (organization_id,)),
                 ("getOrganizationApplianceVpnVpnFirewallRules", (organization_id,)),
                 ("getNetworkApplianceWarmSpare", (network_id,))]

    with open(output_file, "w") as outfile:
        for api_call in api_calls:
            method_name, args = api_call
            try:  # evaluating the calls
                method_to_call = getattr(dashboard.appliance, method_name)
                config = method_to_call(*args)
            except Exception as e:  # if an error is raised print error + api call
                print(f"Error processing Request {api_call}, error: {e}")
            else:  # otherwise we write to the json file with the output of the call
                json.dump(config, outfile, indent=4)
                outfile.write("\n")


def run():
    # you can set up environment variables by going to your CLI and inputting "export VARIABLE_NAME=<VALUE>"
    # load api key
    load_dotenv(override=True, dotenv_path=".env")  # take environment variables from .env.
    api_key = os.environ.get("MERAKI_API_KEY")
    dashboard = meraki.DashboardAPI(api_key)

    org_id = os.environ.get("ORG_ID")

    # call API that returns networks in an org
    network_id_raw = dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')

    # split that input by network
    network_ids = []  # keep track of your network names
    output_file = ""  # initialize output file variable
    for entry in network_id_raw:
        network = entry["id"]
        if "appliance" not in entry['productTypes']:  # exclude networks without security appliances
            print("Your network does not contain a security appliance, skipping")
            continue
        output_file = entry["name"] + ".jsonl"
        network_ids.append(network)
        get_config(network, output_file, dashboard, org_id)


if __name__ == '__main__':
    run()

"""
    connectivityMonitoring = getNetworkApplianceConnectivityMonitoringDestinations(network_id)
    contentFiltering = getNetworkApplianceContentFiltering(network_id)
    cellularFirewall = getNetworkApplianceFirewallCellularFirewallRules(network_id)
    webFirewall = getNetworkApplianceFirewallFirewalledServices(network_id)

    #firewall that governs access to services on the MX such as ICMP pings to the public IP, SNMP, and "web" which is access to the local status page
    serviceFirewall = getNetworkApplianceFirewallFirewalledService(network_id, 'ICMP')
    serviceFirewall2 = getNetworkApplianceFirewallFirewalledService(network_id, 'SNMP')
    serviceFirewall3 = getNetworkApplianceFirewallFirewalledService(network_id, 'web')

    #Inbound Rules
    inboundCellRules = getNetworkApplianceFirewallInboundCellularFirewallRules(network_id)
    inboundFirewallRules = getNetworkApplianceFirewallInboundFirewallRules(network_id)

    #Layer 3 and Layer 7 Firewall Rules
    l3Firewall =getNetworkApplianceFirewallL3FirewallRules(network_id)
    l7Firewall = getNetworkApplianceFirewallL7FirewallRules(network_id)
    l7Categories = getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(network_id)

    #NAT, Port Forwarding
    onetoManyNAT = getNetworkApplianceFirewallOneToManyNatRules(network_id)
    onetoOneNAT = getNetworkApplianceFirewallOneToOneNatRules(network_id)
    portForwarding = getNetworkApplianceFirewallPortForwardingRules(network_id)

    #Specific Firewall Options (such as IP Spoof Protection)
    firewallOptions = getNetworkApplianceFirewallSettings(network_id)

    #MX Port Settings
    port_id = 1
    allPorts = getNetworkAppliancePorts(network_id) #returns settings for all ports
    onePort = getNetworkAppliancePort(network_id, port_id) #returns settings for a specific port #

    #Network Prefixes
    static_delegated_prefix_id = 0
    prefixes = getNetworkAppliancePrefixesDelegatedStatics(network_id) #List static delegated prefixes for a network
    staticPrefix = getNetworkAppliancePrefixesDelegatedStatic(network_id, static_delegated_prefix_id) #Return a static delegated prefix from a network

    #Radio Settings for a Wireless MX
    serial = 0 #example Q2AA-AAAA-AAAA
    wireless = getDeviceApplianceRadioSettings(serial)

    #RF Profiles
    networkRFProfiles = getNetworkApplianceRfProfiles(network_id) #list RF profiles
    specificRFProfile = response = getNetworkApplianceRfProfile(network_id, rf_profile_id) #returns a specific RF profile

    #Security - IDS/IPS & AMP
    ids_ips = getNetworkApplianceSecurityIntrusion(network_id) #returns ips/ids settingd
    ids_ips_rules = getOrganizationApplianceSecurityIntrusion(organization_id) #returns ids/ips rules
    amp = getNetworkApplianceSecurityMalware(network_id) #returns amp

    #Single LAN config
    singleLAN = getNetworkApplianceSingleLan(network_id) 

    #Get SSIDs on wireless MX
    mxSSIDs = getNetworkApplianceSsids(network_id)

    #List static routes
    staticRouteList = getNetworkApplianceStaticRoutes(network_id)

    #return specific static route
    specificRoute = getNetworkApplianceStaticRoute(network_id, static_route_id)

    #display traffic shaping rules
    trafficShaping = getNetworkApplianceTrafficShaping(network_id)

    #List all custom performance classes for an MX network
    perfTrafficShaping = getNetworkApplianceTrafficShapingCustomPerformanceClasses(network_id)

    #Return a custom performance class for an MX network
    perfShapingClass = getNetworkApplianceTrafficShapingCustomPerformanceClass(network_id, custom_performance_class_id)

    #display traffic shaping settings
    settingsTrafficShaping = getNetworkApplianceTrafficShapingRules(network_id)

    #Returns the uplink bandwidth limits for your MX network. This may not reflect the affected device's hardware capabilities.
    #For more information on your device's hardware capabilities, please consult our MX Family Datasheet -
    #[https://meraki.cisco.com/product-collateral/mx-family-datasheet/?file]

    uplinkLimit = getNetworkApplianceTrafficShapingUplinkBandwidth(network_id)

    #Uplink Select, WAN 1 or WAN 2
    uplink = getNetworkApplianceTrafficShapingUplinkSelection(network_id)

    #VPN exclusion rules traffic shaping
    vpnExclusionShaping = getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork(organization_id, total_pages='all')

    #Return uplink settings from appliance status
    uplinkSettings = getDeviceApplianceUplinksSettings(serial)


    #List VLANs in an MX network
    VLANs = getNetworkApplianceVlans(network_id)

    #Return a VLAN
    oneVLAN = getNetworkApplianceVlan(network_id, vlan_id)

    #Get VLAN settings (if VLANs are enabled or disabled)
    onoffVLANs = getNetworkApplianceVlansSettings(network_id)

    #Return hub BGP config
    hubBGP = getNetworkApplianceVpnBgp(network_id)


    #Site-to-site settings
    siteToSiteVPN = getNetworkApplianceVpnSiteToSiteVpn(network_id)

    #3rd party VPNs
    thirdPartyVPNs = getOrganizationApplianceVpnThirdPartyVPNPeers(organization_id)

    #VPN firewall rules
    VPNFirewall = getOrganizationApplianceVpnVpnFirewallRules(organization_id)

    #Warm Spare Info
    warmSpare = getNetworkApplianceWarmSpare(network_id)
    """
