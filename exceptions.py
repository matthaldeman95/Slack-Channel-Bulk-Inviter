"""Exceptions"""

class CredentialFileNotFound(Exception):
    """Thrown when the credentials file does yet exist"""

class InvalidCredentialsFile(Exception):
    """Thrown if the credentials file cannot be parsed"""

class InvalidCodeUrl(Exception):
    """Thrown if the URL pasted in did not contain a valid auth code"""

class InvalidAuthenticationResponse(Exception):
    """Thrown if the OAuth flow failed"""

class InvalidHttpMethod(Exception):
    """Thrown if an illegal HTTP verb was requested"""

class SlackAPIError(Exception):
    """Thrown if the Slack API returns an error"""

class ChannelNotFound(Exception):
    """Thrown if the specified channel could not be found"""

class InvalidUserList(Exception):
    """Thrown if zero valid/existing accounts were found"""
