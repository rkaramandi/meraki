#
# remove_wpn_user.py
#   Removes a user from a WPN SSID. This code is a proof of concept and not intended for production use. Feel free to modify and adapt
# 
# Author: Rohan Karamandi <rkaraman@cisco.com>
#

import meraki

USERNAME = "" # Username to delete
SSID_NUMBER = 0 # As a PoC this assumes SSID0
GP_PREFIX = "GP_" # Prefix to append before new GP's
MERAKI_NETWORK_ID = '' # Network ID of your network
MERAKI_DASHBOARD_API_KEY = '' # LEAVE THIS BLANK - Set it in env variable instead


# Create connection to dashboard
dashboard = meraki.DashboardAPI(
    MERAKI_DASHBOARD_API_KEY,
    output_log=True,
    log_path='logs/',
    print_console=False
)

# Find iPSK
IdentityPsks = dashboard.wireless.getNetworkWirelessSsidIdentityPsks(MERAKI_NETWORK_ID, SSID_NUMBER)

for IdentityPsk in IdentityPsks:
    # Look for specific iPSK and delete
    if IdentityPsk["name"] == USERNAME:
        try: 
            dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk(
                MERAKI_NETWORK_ID, 
                SSID_NUMBER, 
                IdentityPsk["id"]
            )
            print ("Deleted iPSK " + IdentityPsk["name"] + " with ID " + IdentityPsk["id"] )
        except Exception as e:
            print (e)

# Find Group Policy
GroupPols = dashboard.networks.getNetworkGroupPolicies(MERAKI_NETWORK_ID)

for GroupPol in GroupPols:
    # Look for specific GP and delete
    if GroupPol["name"] == GP_PREFIX + USERNAME:
        try:
            response = dashboard.networks.deleteNetworkGroupPolicy(
                MERAKI_NETWORK_ID, 
                GroupPol["groupPolicyId"]
            )
            print ("Deleted Group Policy " + GroupPol["name"] + " with ID " + GroupPol["groupPolicyId"] )
        except Exception as e:
            print (e)
