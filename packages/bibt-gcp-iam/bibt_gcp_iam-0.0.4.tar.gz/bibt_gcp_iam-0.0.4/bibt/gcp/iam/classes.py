import logging

from google.cloud import iam_credentials

# from google.api_core import exceptions as google_exceptions

# from google.oauth2 import credentials

_LOGGER = logging.getLogger(__name__)


class Client:
    """ """

    def __init__(self, credentials=None):
        self._client = iam_credentials.IAMCredentialsClient(credentials=credentials)
