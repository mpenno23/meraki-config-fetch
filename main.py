import meraki
import os
import requests
import json
def get_config(API_KEY, network_id, output_file, dashboard):

    #PLEASE NOTE SOME OF THESE CALLS REQUIRE OTHER VARIABLES LISTED BELOW
    serial = 0
    port_id = 0
    static_delegated_prefix_id = 0
    rf_profile_id = 0
    static_route_id = 0
    custom_performance_class_id = 0
    vlan_id = 0

    api_calls = ["dashboard.appliance.getNetworkApplianceConnectivityMonitoringDestinations(network_id)"
        , "dashboard.appliance.getNetworkApplianceContentFiltering(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallCellularFirewallRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallFirewalledServices(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallFirewalledService(network_id, 'ICMP')"
        , "dashboard.appliance.getNetworkApplianceFirewallFirewalledService(network_id, 'SNMP')"
        , "dashboard.appliance.getNetworkApplianceFirewallFirewalledService(network_id, 'web')"
        , "dashboard.appliance.getNetworkApplianceFirewallInboundCellularFirewallRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallInboundFirewallRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallOneToManyNatRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallOneToOneNatRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id)"
        , "firewallOptions = dashboard.appliance.getNetworkApplianceFirewallSettings(network_id)"
        , "dashboard.appliance.getNetworkAppliancePorts(network_id)"
        , "dashboard.appliance.getNetworkAppliancePort(network_id, port_id)"
        , "dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatics(network_id)"
        , "dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatic(network_id, static_delegated_prefix_id)"
        , "dashboard.appliance.getDeviceApplianceRadioSettings(serial)"
        , "dashboard.appliance.getNetworkApplianceRfProfiles(network_id)"
        , "dashboard.appliance.getNetworkApplianceRfProfile(network_id, rf_profile_id)"
        , "dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)"
        , "dashboard.appliance.getOrganizationApplianceSecurityIntrusion(organization_id)"
        , "dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)"
        , "dashboard.appliance.getNetworkApplianceSingleLan(network_id)"
        , "dashboard.appliance.getNetworkApplianceSingleLan(network_id)"
        , "dashboard.appliance.getNetworkApplianceSsids(network_id)"
        , "dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)"
        , "dashboard.appliance.getNetworkApplianceStaticRoute(network_id, static_route_id)"
        , "dashboard.appliance.getNetworkApplianceTrafficShaping(network_id)"
        , "dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(network_id)"
        ,
                 "dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClass(network_id, custom_performance_class_id)"
        , "dashboard.appliance.getNetworkApplianceTrafficShapingRules(network_id)"
        , "dashboard.appliance.getNetworkApplianceTrafficShapingUplinkBandwidth(network_id)"
        , "dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(network_id)"
        ,
                 "dashboard.appliance.getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork(organization_id, total_pages='all')"
        , "dashboard.appliance.getDeviceApplianceUplinksSettings(serial)"
        , "dashboard.appliance.getNetworkApplianceVlans(network_id)"
        , "dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)"
        , "dashboard.appliance.getNetworkApplianceVlansSettings(network_id)"
        , "dashboard.appliance.getNetworkApplianceVpnBgp(network_id)"
        , "dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)"
        , "dashboard.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers(organization_id)"
        , "dashboard.appliance.getOrganizationApplianceVpnVpnFirewallRules(organization_id)"
        , "dashboard.appliance.getNetworkApplianceWarmSpare(network_id)"
                 ]
    outfile = ""
    for api_call in api_calls:
        try:
            config = eval(api_call)
        except:
            print("Error processing Request ", api_call)
        else:
            with open(output_file, "a") as outfile:
                json.dump(config, outfile, indent = 4)
                outfile.write("\n")

#close file when loop is done

# Press the green button in the gutter to run the script.

if __name__ == '__main__':

    #you can set up environment variables by going to your CLI and inputting "export VARIABLE_NAME=<VALUE>"
    #load api key
    API_KEY = os.environ.get("MERAKI_API_KEY")
    dashboard = meraki.DashboardAPI(API_KEY)

    org_id = os.environ.get("ORG_ID")

    #call API that returns networks in an org
    network_id_raw = dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')

    #split that input by network
    i = 0
    network_ids = []
    output_file = ""
    for entry in network_id_raw:
        network = entry["id"]
        if "appliance" not in entry['productTypes']:
            print("Your network does not contain a security appliance, skipping")
            continue
        output_file = entry["name"] + ".json"
        network_ids.append(network)
        get_config(API_KEY, network, output_file, dashboard)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""
    connectivityMonitoring = dashboard.appliance.getNetworkApplianceConnectivityMonitoringDestinations(network_id)
    contentFiltering = dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
    cellularFirewall = dashboard.appliance.getNetworkApplianceFirewallCellularFirewallRules(network_id)
    webFirewall = dashboard.appliance.getNetworkApplianceFirewallFirewalledServices(network_id)

    #firewall that governs access to services on the MX such as ICMP pings to the public IP, SNMP, and "web" which is access to the local status page
    serviceFirewall = dashboard.appliance.getNetworkApplianceFirewallFirewalledService(network_id, 'ICMP')
    serviceFirewall2 = dashboard.appliance.getNetworkApplianceFirewallFirewalledService(network_id, 'SNMP')
    serviceFirewall3 = dashboard.appliance.getNetworkApplianceFirewallFirewalledService(network_id, 'web')

    #Inbound Rules
    inboundCellRules = dashboard.appliance.getNetworkApplianceFirewallInboundCellularFirewallRules(network_id)
    inboundFirewallRules = dashboard.appliance.getNetworkApplianceFirewallInboundFirewallRules(network_id)

    #Layer 3 and Layer 7 Firewall Rules
    l3Firewall =dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
    l7Firewall = dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
    l7Categories = dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(network_id)

    #NAT, Port Forwarding
    onetoManyNAT = dashboard.appliance.getNetworkApplianceFirewallOneToManyNatRules(network_id)
    onetoOneNAT = dashboard.appliance.getNetworkApplianceFirewallOneToOneNatRules(network_id)
    portForwarding = dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id)

    #Specific Firewall Options (such as IP Spoof Protection)
    firewallOptions = dashboard.appliance.getNetworkApplianceFirewallSettings(network_id)

    #MX Port Settings
    port_id = 1
    allPorts = dashboard.appliance.getNetworkAppliancePorts(network_id) #returns settings for all ports
    onePort = dashboard.appliance.getNetworkAppliancePort(network_id, port_id) #returns settings for a specific port #

    #Network Prefixes
    static_delegated_prefix_id = 0
    prefixes = dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatics(network_id) #List static delegated prefixes for a network
    staticPrefix = dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatic(network_id, static_delegated_prefix_id) #Return a static delegated prefix from a network

    #Radio Settings for a Wireless MX
    serial = 0 #example Q2AA-AAAA-AAAA
    wireless = dashboard.appliance.getDeviceApplianceRadioSettings(serial)

    #RF Profiles
    networkRFProfiles = dashboard.appliance.getNetworkApplianceRfProfiles(network_id) #list RF profiles
    specificRFProfile = response = dashboard.appliance.getNetworkApplianceRfProfile(network_id, rf_profile_id) #returns a specific RF profile

    #Security - IDS/IPS & AMP
    ids_ips = dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id) #returns ips/ids settingd
    ids_ips_rules = dashboard.appliance.getOrganizationApplianceSecurityIntrusion(organization_id) #returns ids/ips rules
    amp = dashboard.appliance.getNetworkApplianceSecurityMalware(network_id) #returns amp

    #Single LAN config
    singleLAN = dashboard.appliance.getNetworkApplianceSingleLan(network_id) 

    #Get SSIDs on wireless MX
    mxSSIDs = dashboard.appliance.getNetworkApplianceSsids(network_id)

    #List static routes
    staticRouteList = dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)

    #return specific static route
    specificRoute = dashboard.appliance.getNetworkApplianceStaticRoute(network_id, static_route_id)

    #display traffic shaping rules
    trafficShaping = dashboard.appliance.getNetworkApplianceTrafficShaping(network_id)

    #List all custom performance classes for an MX network
    perfTrafficShaping = dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(network_id)

    #Return a custom performance class for an MX network
    perfShapingClass = dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClass(network_id, custom_performance_class_id)

    #display traffic shaping settings
    settingsTrafficShaping = dashboard.appliance.getNetworkApplianceTrafficShapingRules(network_id)

    #Returns the uplink bandwidth limits for your MX network. This may not reflect the affected device's hardware capabilities.
    #For more information on your device's hardware capabilities, please consult our MX Family Datasheet -
    #[https://meraki.cisco.com/product-collateral/mx-family-datasheet/?file]

    uplinkLimit = dashboard.appliance.getNetworkApplianceTrafficShapingUplinkBandwidth(network_id)

    #Uplink Select, WAN 1 or WAN 2
    uplink = dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(network_id)

    #VPN exclusion rules traffic shaping
    vpnExclusionShaping = dashboard.appliance.getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork(organization_id, total_pages='all')

    #Return uplink settings from appliance status
    uplinkSettings = dashboard.appliance.getDeviceApplianceUplinksSettings(serial)


    #List VLANs in an MX network
    VLANs = dashboard.appliance.getNetworkApplianceVlans(network_id)

    #Return a VLAN
    oneVLAN = dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)

    #Get VLAN settings (if VLANs are enabled or disabled)
    onoffVLANs = dashboard.appliance.getNetworkApplianceVlansSettings(network_id)

    #Return hub BGP config
    hubBGP = dashboard.appliance.getNetworkApplianceVpnBgp(network_id)


    #Site-to-site settings
    siteToSiteVPN = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)

    #3rd party VPNs
    thirdPartyVPNs = dashboard.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers(organization_id)

    #VPN firewall rules
    VPNFirewall = dashboard.appliance.getOrganizationApplianceVpnVpnFirewallRules(organization_id)

    #Warm Spare Info
    warmSpare = dashboard.appliance.getNetworkApplianceWarmSpare(network_id)
    """
