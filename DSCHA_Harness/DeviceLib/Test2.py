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

# # Create Device Group
# url_endpoint = "/mgmt/tm/cm/device-group"
# post_args = {"name": "dsc1-dg",
#              "auto-sync": "enabled",
#              "type": "sync-failover"}


# # Add device to device group (patch)
# url_endpoint = "/mgmt/tm/cm/device-group/dsc1-dg"
# post_args = {"devices": ["B2.f5net.com"]}


# # Remove device from device group (delete)
# url_endpoint = "/mgmt/tm/cm/device-group/dsc1-dg/devices/B2.f5net.com"


# # Delete device group (delete)
# url_endpoint = "/mgmt/tm/cm/device-group/dsc1-dg"


# Apply config sync
url_endpoint = '/mgmt/tm/cm/config-sync'
post_args = {'command': 'run',
             'options': [{'to-group': 'dsc1-dg'}]}

s = requests.Session()
s.auth = (login, password)
s.verify = False

# Post Data
r = requests.Request('POST',
                     'https://' + mgmt_ip + url_endpoint,
                     auth=HTTPBasicAuth(login, password),
                     json=post_args)


# # Patch data
# r = requests.Request('PATCH',
#                      'https://' + mgmt_ip + url_endpoint,
#                      auth=HTTPBasicAuth(login, password),
#                      json=post_args)

prepared = r.prepare()

print('posting to url: ' + 'https://' + mgmt_ip + url_endpoint)
pretty_print_post(prepared)

response = s.send(prepared)

print('POST response: ' + response.text)

pprint(response.json())



# # Get data
# url_endpoint = "/mgmt/tm/cm/device-group/dsc1-dg/devices"
# s.headers.update({'Content-Type': 'application/json'})
# response = s.get('https://' + mgmt_ip + url_endpoint)
# members = []
# for entry in response.json()['items']:
#     members.append(entry['name'])
# print(members)

