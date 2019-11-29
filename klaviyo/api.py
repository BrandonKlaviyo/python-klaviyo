import sys

from .lists import Lists
from .metrics import Metrics
from .profiles import Profiles
from .public import Public

class Klaviyo(object):
    def __init__(self, public_token=None, private_token=None):
        self.auth = {
            'public_token': public_token,
            'private_token': private_token
        }

    def __getattr__(self, item):
        return KlaviyoAPIResourceWrapper(item, self)

class KlaviyoAPIResourceWrapper(object):
    def __init__(self, resource_class, api, *args, **kwargs):
        """

        """
        self.api = api
        if isinstance(resource_class, str):
            self.resource_class = self.str_to_class(resource_class, api)
        else:
            self.resource_class = resource_class

    def __getattr__(self, item, *args, **kwargs):
        """

        """

        return lambda *args, **kwargs: getattr(self.resource_class, item)(*args, **kwargs)

    @classmethod
    def str_to_class(cls, str, api):
        """
        Transforms a string class name into a class object
        Assumes that the class is already loaded.
        """
        print ('string of instance - ', str)
        return getattr(sys.modules[__name__], str)(api.auth['public_token'], api.auth['private_token'])

