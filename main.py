import sys
import json
from builtins import input
from exceptions import *
from progress.bar import Bar
from SlackAPIClient import SlackAPIClient

from time import sleep

def print_spacer():
    print('\n---------------------------------\n')

def main():
    c = SlackAPIClient(credentials_file="credentials.json")
    
    print_spacer()
    channel_private_input = input("Is the channel private?  Type y for yes, any other character for no:  ")
    channel_private = channel_private_input.strip().lower() == "y"
    
    print_spacer()
    channel_name = input("Enter the name of the channel:  ")
    print("Finding channel...")
    channel_id = c.find_channel(channel_name, channel_private)
    
    print_spacer()
    print("Either paste a comma-separated list of email addresses into this prompt, or provide the name of a file in your current working directory that contains email addresses of the target users, one email address per line.  ")
    user_list_input = input("Response:  ")
    try:
        with open(user_list_input) as infile:
            user_list = infile.read().split('\n')
    except IOError:
        user_list = user_list_input.split(',')
    user_list = [u.strip().lower() for u in user_list if u]
    user_list = user_list[0:500]
    print_spacer()
    print(f"Found {len(user_list)} emails in that list")
    if len(user_list) <= 0:
        raise InvalidUserList("0 users found in list provided, unable to take any action")

    ### Get user with progress bar
    bar = Bar('Looking up users', max=len(user_list), suffix='%(percent).1f%% - %(eta)ds')
    users_found, users_not_found = list(), list()
    for u in user_list:
        bar.next()
        result = c.find_user(u)
        if result:
            users_found.append({
                "id": result,
                "email": u
            })
        else:
            users_not_found.append(u)

    print_spacer()
    print(f"\nFound {len(users_found)} matching accounts.")
    if len(users_found) <= 0:
        raise InvalidUserList("0 users found with matching Slack accounts, unable to take any action")
    if len(users_not_found) > 0:
        print_spacer()
        print(f"Unable to find {len(users_not_found)} account(s), would you like to see a list?  ")
        see_list = input("Type y for yes, any other character for no:  ")
        if see_list.strip().lower() == "y":
            print("Accounts not found:  ")
            for u in users_not_found:
                print(u)
    print_spacer()

    print(f"All set to invite {len(users_found)} users to channel #{channel_name}?")
    print("Type y for yes, any other character to abort and reconsider the permanence of what you're about to do.")
    ready = input("Cleared for takeoff?  ")
    if ready.strip().lower() != "y":
        print("Aborting")
        sys.exit(0)

    bar = Bar('Sending invites', max=len(users_found), suffix='%(percent).1f%% - %(eta)ds')
    successes = 0
    failures = list()
    for u in users_found:
        try:
            c.invite_to_channel(u['id'], channel_id, channel_private)
            successes += 1
        except SlackAPIError as e:
            failures.append({
                "user": u['email'],
                "error": str(e)
            })
    print_spacer()
    print(f"{successes} users invited successfully")
    if len(failures) == 0:
        print("No failures!")
    else:
        print(f"There were {len(failures)} errors")
        with open('errors.json', 'w') as outfile:
            json.dump(failures, outfile, indent=4)
        print("An error log has been written to this directory, called errors.json")
    print("Bye for now!")


if __name__ == "__main__":
    main()