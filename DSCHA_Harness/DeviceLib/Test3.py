import requests

url = "http://127.0.0.1:8000/api/v1/UDPTraffics/12/"
post_args = {"is_start": False}
r = requests.patch(url,
                   json=post_args)

#
# r = requests.get(url)

print (r.status_code)
print(r.text)