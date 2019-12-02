from abc import ABC
import base64
import datetime
import json
import time

import requests
import simplejson

try:
   from urllib.parse import urlencode
except ImportError:
   from urllib import urlencode

from klaviyo import __version__


class KlaviyoException(Exception):
    pass


class KlaviyoAuthenticationError(KlaviyoException):
    pass


class KlaviyoRateLimitException(KlaviyoException):
    pass


class KlaviyoAPI(ABC):
    KLAVIYO_API_SERVER = 'https://a.klaviyo.com/api'
    KLAVIYO_DATA_VARIABLE = 'data'
    V1_API = 'v1'
    V2_API = 'v2'

    # HTTP METHODS
    HTTP_DELETE = 'delete'
    HTTP_GET = 'get'
    HTTP_POST = 'post'
    HTTP_PUT = 'put'

    # TYPE OF API METHOD
    PRIVATE = 'private'
    PUBLIC = 'public'

    # UNIVERSAL KEYS
    METRIC = 'metric'
    METRICS = 'metrics'
    TIMELINE = 'timeline'

    def __init__(self, public_token=None, private_token=None, api_server=KLAVIYO_API_SERVER):
        self.public_token = public_token
        self.private_token = private_token
        self.api_server = api_server

        # if you only need to do one type of request, it's not required to have both private and public.. but we need at least 1 token
        if not self.public_token and not self.private_token:
            raise KlaviyoException('You must provide a public or private api token')

    ######################
    # HELPER FUNCTIONS
    ######################
    @staticmethod
    def _normalize_timestamp(timestamp):
        if isinstance(timestamp, datetime.datetime):
            timestamp = time.mktime(timestamp.timetuple())
        return timestamp

    @staticmethod
    def _filter_params(params):
        """ To make sre we're passing in params with values """
        return dict((k, v) for k, v in params.items() if v is not None)

    @staticmethod
    def _build_marker_param(marker):
        """ A helper for the marker param """
        params = {}
        if marker:
            params['marker'] = marker
        return params

    def _build_query_string(self, params, is_test):
        return urlencode({
            self.KLAVIYO_DATA_VARIABLE: base64.b64encode(json.dumps(params).encode('utf-8')),
            'test': 1 if is_test else 0,
        })

    #####################
    # API HELPER FUNCTIONS
    #####################
    def __is_valid_request_option(self, request_type=PRIVATE):
        """
        Making sure the appropriate credentials are there
        Args:
            request_type (str): the type of method (private/public)
        """
        if request_type == self.PUBLIC and not self.public_token:
            raise KlaviyoException('Public token is not defined')

        if request_type == self.PRIVATE and not self.private_token:
            raise KlaviyoException('Private token is not defined')

    def _v2_request(self, path, method, params={}):
        """
        A method that handles the v2 api requests
        Args:
            path (str): url we make a request to
            method (str): http method
            params (dict):
        Returns:
            (dict or arr): response from Klaviyo API
        """

        url = '{}/{}/{}'.format(
            self.api_server,
            self.V2_API,
            path,
        )

        params.update({
            'api_key': self.private_token
        })
        params = json.dumps(params)

        return self.__request(method, url, params)

    def _v1_request(self, path, method, params={}):
        """
        """
        url = '{}/{}/{}'.format(
            self.api_server,
            self.V1_API,
            path,
        )
        formatted_url = '{}?api_key={}'.format(url, self.private_token)

        return self.__request(method, formatted_url, params)

    def _pubic_request(self, path, querystring):
        """
        This handles track and identify calls, always a get request
        Args:
            path (str): track or identify
            querystring (str): urlencoded & b64 encoded string
        Returns:
            (str): 1 or 0 (pass/fail)
        """

        url = '{}/{}?{}'.format(self.api_server, path, querystring)
        return self.__request(self.HTTP_GET, url, request_type='public')

    def __request(self, method, url, params={}, request_type='private'):
        """
        The method that executes the request being made
        Args:
            method (str): the type of HTTP request
            url (str): the url to make the request to
            params (dict or json): the body of the request
        Returns:
            (str, dict): public returns 1 or 0  (pass/fail)
                        v1/v2 returns dict
        """
        self.__is_valid_request_option(request_type=request_type)
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Klaviyo-Python/{}'.format(__version__)
        }

        response = getattr(requests, method.lower())(url, headers=headers, data=params)

        return self.__handle_response(response, request_type)

    def __handle_response(self, response, request_type):
        """
        A Helper to either return either a response or a handled exception
        """
        if response.status_code == 403:
            raise KlaviyoAuthenticationError('The api key specified is not valid')
        elif response.status_code == 429:
            raise KlaviyoRateLimitException(response.json())

        # return the json response from a private call
        if request_type == self.PRIVATE:
            try:
                return response.json()
            except (simplejson.JSONDecodeError, ValueError) as e:
                raise KlaviyoException('Request did not return json: {}'.format(e))

        # we return the str 1 or 0 for track/identify calls
        elif request_type == self.PUBLIC:
            return response.text

