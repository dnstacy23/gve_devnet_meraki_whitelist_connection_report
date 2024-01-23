#!/usr/bin/env python3
"""
Copyright (c) 2024 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import meraki
import pandas as pd
import sys
import os
import datetime
import json
from dotenv import load_dotenv


def get_network_id(dashboard, org_id, net_name):
    """
    Connect to the Meraki dashboard and retrieve the networks of the org
    Then find the network id corresponding to the network name provided
    in the environment variables
    :return: string containing the network id or None if no id found
    """
    networks = dashboard.organizations.getOrganizationNetworks(org_id)

    for network in networks:
        if network["name"] == net_name:
            return network["id"]

    return None

def get_allow_list_clients(dashboard, net_id):
    """
    Connect to the Meraki dashboard and retrieve all the clients that have
    connected to  the network in the last 31 days as well as which policies
    they have been assigned
    :return: list containing the client ids of clients on the whitelist
    """
    #timespan is given in seconds, the max value is 2678400, equivalent to 31 day
    client_policies = dashboard.networks.getNetworkPoliciesByClient(net_id,
                                                                    timespan=2678400,
                                                                    total_pages="all")
    allow_list_clients = []
    for client in client_policies:
        client_id = client["clientId"]
        policies = client["assigned"]
        for policy in policies:
            if policy["name"] == "Allowed":
                allow_list_clients.append(client_id)

    return allow_list_clients

def get_network_client_info(dashboard, net_id, net_name, allow_list):
    """
    Connect to the Meraki dashboard and get the client details of each
    client on the whitelist
    Then add the MAC address, IP address, last seen date and time,
    online status, and network name of the client to a dictionary
    Then add that dictionary to a list
    :return: list of dictionaries representing each client on the whitelist
    """
    allowed_clients_info = []
    for client in allow_list:
        client_info = dashboard.networks.getNetworkClient(net_id, client)
        last_seen_datetime = datetime.datetime.fromtimestamp(client_info["lastSeen"])
        new_client_info = {
            "mac": client_info["mac"],
            "ip": client_info["ip"],
            "last_seen": last_seen_datetime,
            "status": client_info["status"],
            "network": net_name
        }
        allowed_clients_info.append(new_client_info)

    return allowed_clients_info

def main(argv):
    # retrieve the environmental variables
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    ORG_ID = os.getenv("ORG_ID")
    NETWORK_NAMES = json.loads(os.getenv("NETWORK_NAMES"))

    # connect to the Meraki dashboard
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

    # find the network id corresponding to the network name given in the environmental variables
    net_id_to_name = {}
    for name in NETWORK_NAMES:
        net_id = get_network_id(dashboard, ORG_ID, name)
        if net_id is None:
            print(f"There was not a network ID found associated with the network name {name}")
        else:
            net_id_to_name[net_id] = name

    # for each network, find the network client details of each client on the whitelist
    allowed_clients_info = []
    for net_id in net_id_to_name:
        allow_list_clients = get_allow_list_clients(dashboard, net_id)
        allowed_clients_info.extend(get_network_client_info(dashboard, net_id,
                                                            net_id_to_name[net_id],
                                                            allow_list_clients))

    # create an Excel spreadsheet that contains the details of the whitelisted clients
    with pd.ExcelWriter("whitelist_connection_report.xlsx") as writer:
        whitelist_df = pd.DataFrame.from_dict(allowed_clients_info)
        whitelist_df.to_excel(writer, index=False)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
