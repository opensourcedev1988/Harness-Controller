import requests
from requests.auth import HTTPBasicAuth
from DSCHA_Harness.settings import DEBUG


def rest_post(url_endpoint, post_args, login="admin", password="admin"):
    s = requests.Session()
    s.auth = (login, password)
    s.verify = False
    r = requests.Request('POST',
                         'https://' + url_endpoint,
                         auth=HTTPBasicAuth(login, password),
                         json=post_args)
    prepared = r.prepare()

    if DEBUG:
        print('posting to url: ' + 'https://' + url_endpoint)
        pretty_print_post(prepared)

    response = s.send(prepared)

    if DEBUG:
        print('POST response: ' + response.text)

    return response


def rest_patch(url_endpoint, post_args, login="admin", password="admin"):
    s = requests.Session()
    s.auth = (login, password)
    s.verify = False
    r = requests.Request('PATCH',
                         'https://' + url_endpoint,
                         auth=HTTPBasicAuth(login, password),
                         json=post_args)
    prepared = r.prepare()

    if DEBUG:
        print('patching to url: ' + 'https://' + url_endpoint)
        pretty_print_post(prepared)

    response = s.send(prepared)

    if DEBUG:
        print('PATCH response: ' + response.text)

    return response


def rest_get(url_endpoint, login="admin", password="admin"):

    s = requests.Session()
    s.auth = (login, password)
    s.verify = False
    s.headers.update({'Content-Type': 'application/json'})
    response = s.get('https://' + url_endpoint)
    if DEBUG:
        print('GET response: ' + response.text)
    return response


def rest_delete(url_endpoint, login="admin", password="admin"):

    s = requests.Session()
    s.auth = (login, password)
    s.verify = False
    response = s.delete('https://' + url_endpoint)
    if DEBUG:
        print('DELETE response: ' + response.text)
    return response


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