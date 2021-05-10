import requests
import urllib.parse
import posixpath

class RtrtClient:
    """
    A client to perform rest api calls to rtrt web-site
    """
    def __init__(self, config:dict={}):
        self.endpoint = config.get("url")
        self.appid = config.get("appid")
        self.token = config.get("token")

    def get_events(self):
        params = {}
        self.auth(params)
        response = requests.get(link(self.endpoint, "events"), params=params)
        events = response.json().get('list')
        names = [x.get('name') for x in events]
        return names

    def get_categories(self, event):
        params = {}
        self.auth(params)
        response = requests.get(link(self.endpoint, "events", event, "categories"), params=params)

        return response.json()['list']

    def get_participants(self, event, category):
        params = {"max": 100}
        self.auth(params)
        response = requests.get(
            link(self.endpoint,
                 "events", event,
                 "categories", category),
            params=params)

        return response.json()['list']

    def get_profile(self, event, profile_id):
        params = {}
        self.auth(params)
        response = requests.get(
            link(self.endpoint,
                 "events", event,
                 "profiles", profile_id),
            params=params)

        return response.json()['list']

    def get_results(self, event, profile_id):
        params = {}
        self.auth(params)
        response = requests.get(
            link(self.endpoint,
                 "events", event,
                 "profiles", profile_id,
                 "splits"),
            params=params)
        return response.json().get('list')

    def auth(self, params):
        params["appid"] = self.appid
        params["token"] = self.token


def link(*parts) -> str:
    if len(parts) < 2:
        return "".join(parts)

    #print(list(parts[1:]))
    res = urllib.parse.urljoin(parts[0], posixpath.join(*list(parts[1:])))

    return res

link ("http://h1.com", "p1", "p2", "P3","t.txt")
