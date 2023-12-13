#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

import requests
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ScodocAPI():
    def __init__(self, url=None, login=None, password=None, departement=None):
        self.url = os.path.join(url, "ScoDoc")
        self.login = login
        self.password = password
        self.token = None
        self.departement = departement

    def __str__(self):
        return f'{self.login}@{self.url}'

    def call(self, path, post=False):
        if not self.token:
            # print("get token")
            self.get_token()

        url = self.url

        if self.departement:
            url = os.path.join(url, self.departement)

        url = os.path.join(url, "api")
        url = os.path.join(url, path)


        if post:
            # print(f"[POST] {url} ({self.token})")
            response = requests.post(url, headers = {"Authorization": f"Bearer {self.token}"}, verify=False)
        else:
            # print(f"[GET] {url} ({self.token})")
            response = requests.get(url, headers = {"Authorization": f"Bearer {self.token}"}, verify=False)

        response.raise_for_status()
        return response.json()

    def get_token(self):
        url = os.path.join(self.url, "api", "tokens")
        auth = (self.login, self.password)
        # print(f"[POST] {url} {auth}")
        response = requests.post(url, auth=auth, verify=False)
        response.raise_for_status()
        self.token = response.json()["token"]

    def ping(self):
        print("ping?")
        r = self.call("etudiants/courants")
        print("pong!")
