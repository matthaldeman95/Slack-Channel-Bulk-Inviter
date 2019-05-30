## Slack channel bulk inviter

A small CLI app written in Python to invite a group of users into a channel using their email addresses.

## Setup

Install Python 3 and pip.  Clone the reop and `cd` to it, then install dependencies:

        pip install -r requirements.txt

You will need to create a Slack app at api.slack.com with the following OAuth scopes:

- `channels:read` and `channels:write` (For public channels)
- `groups:read` and `groups:write` (For private channels)
- `users:read.email` (Always needed)

And specify "http://localhost" as your OAuth redirect URI.

Once you have your client ID and secret, paste them into the "credentials_empty.json" and rename it to "credentials.json".  Leave the access token value blank, as that will be filled in once you receive an access token.

**Disclaimer** This is an extremely insecure way of storing your tokens!!!  Your tokens are stored in plain text in a file.  I take no responsibility for your leaked tokens.  I highly suggest you modify the `load_credentials()` and `write_credentials()` methods in the `SlackOAuthClient` class to store the credentials in a safer way.

Then just run `python main.py`.  It will open a browser window to navigate you through the OAuth flow; after you authorize your app and are redirected to the `localhost` redirect URI, your full URL should include a `code=` param.  Copy the entire URL and paste it back into the prompt to have the code parsed out, and the rest of the OAuth flow completed.  

After OAuth completes, the main routine will run.

## Usage

Run `python main.py` to start, then follow the prompts to specify the channel type, channel name, and the list of users you want to invite (either in the form of a file or a comma separated string of emails)