"""
Class that handles OAuth credential generation
"""

import json
import webbrowser
from builtins import input
from exceptions import *
import requests

class SlackOAuthClient:
    """
    Class that handles OAuth credential generation
    """
    def __init__(self, credentials_file):
        """Load credentials"""
        self.client_id = ""
        self.client_secret = ""
        self.access_token = ""
        self.credentials_file = credentials_file
        self.auth_url = "https://slack.com/oauth/authorize"
        self.token_url = "https://slack.com/api/oauth.access"
        self.load_credentials()

    def load_credentials(self):
        """Read credentials from provided JSON file"""
        try:
            with open(self.credentials_file) as infile:
                credentials = json.load(infile)
        except IOError:
            raise CredentialFileNotFound("No credentials.json file found in working directory")
        try:
            self.client_id = credentials['client_id']
            self.client_secret = credentials['client_secret']
            self.access_token = credentials['access_token']
        except KeyError:
            raise InvalidCredentialsFile("Invalid credential file.  Ask Matthew for help.")
        if not self.access_token:
            self.get_new_tokens()

    def write_credentials(self):
        """Dump credentials to credentials.json file"""
        try:
            with open(self.credentials_file, 'w') as outfile:
                credentials = {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "access_token": self.access_token
                }
                json.dump(credentials, outfile, indent=4)
        except IOError:
            raise CredentialFileNotFound("No credentials.json file found in working directory")

    def get_new_tokens(self):
        """
        This is used to generate a completely new access token, should not be used frequently
        """
        url = self.auth_url
        url += "?client_id=" + self.client_id
        url += "&scope=channels:read,groups:read,users:read,users:read.email"
        url += "&redirect_uri=http://localhost"
        print("Now opening web browser to authentication page.")
        print("Approve the required permissions and you will be redirected.")
        webbrowser.open(url)
        print("After authorizing, you should be redirected to a URL, like:  ")
        print("localhost/?code-xxxxxx")
        print("Copy this entire URL and paste it here:  ")
        code_url = input("URL:  ")
        try:
            code = code_url.split("localhost/?code=")[1].split("&")[0]
        except:
            raise InvalidCodeUrl("Error with parsing that URL.  Talk to Matthew.")
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": "http://localhost"
        }
        response = requests.post(self.token_url, params=params)
        response.raise_for_status()
        r_json = response.json()
        try:
            self.access_token = r_json['access_token']
        except KeyError:
            raise InvalidAuthenticationResponse("Unable to get an access token.")
        self.write_credentials()

    @staticmethod
    def request(method, url, headers, params=None, data=None):
        """Handler for HTTP requests"""
        if method.lower() == 'get':
            response = requests.get(url, headers=headers, params=params)
        elif method.lower() == 'post':
            response = requests.post(url, headers=headers, params=params, data=data)
        elif method.lower() == 'put':
            response = requests.put(url, headers=headers, params=params, data=data)
        else:
            raise InvalidHttpMethod()
        response.raise_for_status()
        return response.json()
