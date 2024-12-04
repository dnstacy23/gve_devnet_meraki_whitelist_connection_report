# GVE DevNet Meraki Whitelist Connection Report
This repository contains the source code of a Python script that can create a report regarding the network clients that have been whitelisted on the dashboard. The script then gets the allow list from the Meraki dashboard and creates a spreadsheet from the results with columns for the MAC address of the client, IP address of the client, date and time the client last connected, whether the client is currently online or offline, and the name of the network the client is connected to.

> Note: Currently, the code is set to retrieve the clients that have been seen in the network in the past 31 days. The maximum lookback period is 31 days from the day the script is run. To change the lookback period, change the timespan parameter on line 51 for the getNetworkPoliciesByClient API call.

## Contacts
* Danielle Stacy

## Solution Components
* Python 3.12
* Meraki SDK
* Excel

## Prerequisites
#### Meraki API Keys
In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:
1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.

> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization). 

> Note: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).

#### Organization ID and Network Names
Before running the code, you must know which Meraki organiation and which networks in that organization you will be configuring. You will need to record the name of the networks and the organization ID in the Installation/Configuration section. To find the organization ID, follow these steps:
1. Login to the Meraki dashboard
2. In the left-hand menu, select the dropdown menu of organizations. Then choose the name of the organization that you want to write a report for
3. Once you are brought to the Organization Summary page, scroll to the bottom of the page. Here, you should find login and session information. At the very bottom of the page, it will list the hosting information of your Meraki organization, which should include your organization ID
4. Copy and save the organization ID in a safe place

## Installation/Configuration
1. Clone this repository with `git clone [repository name]`. To find the repository name, click the green `Code` button above the repository files. Then, the dropdown menu will show the https domain name. Click the copy button to the right of the domain name to get the value to replace [repository name] placeholder.
![/IMAGES/git-clone.png](/IMAGES/git-clone.png)
1. Add Meraki API key, organization ID, and network names to environment variables
```python
API_KEY = "enter API key here"
ORG_ID = "enter organization ID here"
NETWORK_NAMES = '["enter network names here", "separated by commas"]'
```
3. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
4. Install the requirements with `pip3 install -r requirements.txt`

## Usage
To run the program, use the command:
```
$ python3 whitelist_report.py
```

Once the script is finished running, it will have created a spreadsheet named whitelist_connection_report.xlsx

![/IMAGES/whitelist_connection_report.png](/IMAGES/whitelist_connection_report.png)

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
