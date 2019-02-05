"""
Class that handles all Slack API methods
Subclasses the SlackOAuthClient parent class
"""

from exceptions import *
from SlackOAuthClient import SlackOAuthClient

class SlackAPIClient(SlackOAuthClient):
    """
    Class that handles all Slack API methods
    Subclasses the SlackOAuthClient parent class
    """

    def __init__(self, credentials_file):
        """Call parent class init to generate OAuth tokens"""
        SlackOAuthClient.__init__(self, credentials_file=credentials_file)
        self.base_url = "https://slack.com/api/"
        self.headers = {"Authorization": "Bearer " + self.access_token}

    def find_channel(self, channel_name, is_private):
        """
        Pass in the channel's name and a boolean for whether it is expected to be private
        Returns the channel ID if found, raise a ChannelNotFound exception otherwise
        """
        url = self.base_url
        url += "conversations.list"
        params = {
            "limit": 1000,
            "types": "private_channel" if is_private else "public_channel"
        }
        while True:
            response = self.request("GET", url, params=params, headers=self.headers)
            if not response['ok']:
                raise SlackAPIError(response['error'])
            results = response['channels']
            for result in results:
                if result['name'] == channel_name:
                    return result['id']
            if "response_metadata" in response.keys():
                metadata = response['response_metadata']
                if "next_cursor" in metadata.keys():
                    cursor = metadata['next_cursor']
                    if cursor:
                        params['cursor'] = cursor
                    else:
                        break
                else:
                    break
            else:
                break
        raise ChannelNotFound()

    def find_user(self, email):
        """
        Query the API for a user with the provided email address
        """
        url = self.base_url + "users.lookupByEmail"
        params = {"email": email}
        response = self.request("GET", url, headers=self.headers, params=params)
        if not response['ok']:
            if response['error'] == "users_not_found":
                return None
            raise SlackAPIError(response['error'])
        return response['user']['id']

    def invite_to_channel(self, user_id, channel_id, is_private):
        """
        Invite the specified user to the specified channel
        """
        url = self.base_url
        url += "conversations.invite"
        params = {
            "users": user_id,
            "channel": channel_id
        }
        response = self.request("POST", url, headers=self.headers, params=params)
        if not response['ok']:
            raise SlackAPIError(response['error'])
        else:
            return
