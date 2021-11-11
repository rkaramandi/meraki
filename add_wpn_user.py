#
# add_wpn_user.py
#   Adds a user to WPN SSID. This code is a proof of concept and not intended for production use. Feel free to modify and adapt
# 
# Author: Rohan Karamandi <rkaraman@cisco.com>
#

import meraki
import pyqrcode as pq # Credit: https://www.kite.com/blog/python/creating-3d-printed-wifi-access-qr-codes-with-python/
from datetime import datetime, date
import time

USERNAME = "" # Username to create
PASSPHRASE = str(time.mktime(datetime.today().timetuple())) # Use epoch time for PoC
SSID_NUMBER = 0 # As a PoC this assumes SSID0
SSID_NAME = ""
DEFAULT_GP_NAME = "Default" # Group policy to clone settings from
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

# Find all GP's
GroupPols = dashboard.networks.getNetworkGroupPolicies(MERAKI_NETWORK_ID)

for GroupPol in GroupPols:
    # Look for default GP and clone
    if GroupPol["name"] == DEFAULT_GP_NAME:
        try: 
            NewGroupPol = dashboard.networks.createNetworkGroupPolicy(
                MERAKI_NETWORK_ID, 
                GP_PREFIX + USERNAME, 
                scheduling=GroupPol["scheduling"], 
                bandwidth=GroupPol["bandwidth"], 
                firewallAndTrafficShaping=GroupPol["firewallAndTrafficShaping"], 
                contentFiltering=GroupPol["contentFiltering"], 
                splashAuthSettings=GroupPol["splashAuthSettings"], 
                vlanTagging=GroupPol["vlanTagging"], 
                bonjourForwarding=GroupPol["bonjourForwarding"]
            )

        # Show error and clean up
        except Exception as e:
            print (e)
            exit ()

# Query for GP ID and Create iPSK to tie the two
GroupPols = dashboard.networks.getNetworkGroupPolicies(MERAKI_NETWORK_ID)

for GroupPol in GroupPols:
    # Look to make sure GP exists - get id back from it
    if GroupPol["name"] == GP_PREFIX + USERNAME:
        try:
            NewIdentityPsk = dashboard.wireless.createNetworkWirelessSsidIdentityPsk(
                MERAKI_NETWORK_ID, 
                SSID_NUMBER, 
                USERNAME, 
                GroupPol["groupPolicyId"], 
                passphrase = PASSPHRASE
            )

            # Output QR code and passphrase info
            qr = pq.create(f'WIFI:S:' + SSID_NAME + ';T:WPA;P:' + PASSPHRASE + ';;')
            print(qr.terminal())
            print ("Passphrase is: `" + PASSPHRASE + "` for user " + USERNAME)

        # Show error and clean up
        except Exception as e: 
            print (e)
            GroupPols = dashboard.networks.getNetworkGroupPolicies(MERAKI_NETWORK_ID)
            for GroupPol in GroupPols:
                if GroupPol["name"] == GP_PREFIX + USERNAME:
                    response = dashboard.networks.deleteNetworkGroupPolicy(
                        MERAKI_NETWORK_ID, 
                        GroupPol["groupPolicyId"]
                )
            exit()
