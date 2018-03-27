import requests
import urllib3
from pprint import pprint
from requests.auth import HTTPBasicAuth


def pretty_print_post(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

# urllib3.disable_warnings()
login = "admin"
password = "admin"
mgmt_ip = "10.255.87.99"

# # For traffic group creation
# url_endpoint = "/mgmt/tm/cm/traffic-group"
# post_args = {"name": "app1-tg"}


# # For pool creation
# url_endpoint = "/mgmt/tm/ltm/pool"
# post_args = {"name": "app1-pool",
#              "members": ["10.2.1.100:11242"],
#              "monitor": "udp"}

# # For virtual server creation
# url_endpoint = "/mgmt/tm/ltm/virtual"
# post_args = {"name": "app1-virtual",
#              "pool": "app1-pool",
#              "destination": "10.1.2.10:14589",
#              "ipProtocol": "udp",
#              "sourceAddressTranslation": {"type": "automap"}}


# # Assign traffic group to virtual address
# url_endpoint = "/mgmt/tm/ltm/virtual-address/10.1.2.10"
# post_args = {"trafficGroup": "app1-tg"}


# Delete virtual server
url_endpoint = "/mgmt/tm/ltm/virtual/TestApp1-virtual"

s = requests.Session()
s.auth = (login, password)
s.verify = False

# # Post Data
# r = requests.Request('POST',
#                      'https://' + mgmt_ip + url_endpoint,
#                      auth=HTTPBasicAuth(login, password),
#                      json=post_args)


# # Patch data
# r = requests.Request('PATCH',
#                      'https://' + mgmt_ip + url_endpoint,
#                      auth=HTTPBasicAuth(login, password),
#                      json=post_args)
#
# prepared = r.prepare()
#
# print('posting to url: ' + 'https://' + mgmt_ip + url_endpoint)
# pretty_print_post(prepared)
#
# response = s.send(prepared)


# Delete data
response = s.delete('https://' + mgmt_ip + url_endpoint)
print('DELETE response: ' + response.text)


# Get data
# url_endpoint = "/mgmt/tm/cm/device"
# s.headers.update({'Content-Type': 'application/json'})
# response = s.get('https://' + mgmt_ip + url_endpoint)
#
# print('POST response: ' + response.text)
#
# pprint(response.json()['items'][0]['hostname'])