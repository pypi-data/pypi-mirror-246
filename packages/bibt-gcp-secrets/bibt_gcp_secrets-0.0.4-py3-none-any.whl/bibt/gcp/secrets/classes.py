import logging

from google.cloud import secretmanager

_LOGGER = logging.getLogger(__name__)


class Client:
    """ """

    def __init__(self, credentials=None):
        self._client = secretmanager.SecretManagerServiceClient(credentials=credentials)
