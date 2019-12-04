from .api_helper import KlaviyoAPI


class Lists(KlaviyoAPI):
    LIST = 'list'
    LISTS = 'lists'
    SUBSCRIBE = 'subscribe'
    MEMBERS = 'members'
    ALL = 'all'

    def get_lists(self):
        """ Returns a list of Klaviyo lists """
        return self._v2_request(self.LISTS, self.HTTP_GET)
    
    def create_list(self, list_name):
        """
        This will create a new list in Klaviyo
        Args:
            list_name (str): A list name
        Returns:

        """
        return self._v2_request(self.LISTS, self.HTTP_POST, list_name)

    def get_list_by_id(self, list_id):
        """
        This will fetch a list by it's ID
        Args:
            list_id: str() the list id
        Returns:

        """
        return self._v2_request('{}/{}'.format(self.LIST, list_id), self.HTTP_GET)
    
    def update_list_name_by_id(self, list_id, list_name):
        """
        This allows you to update a list's name
        Args:
            list_id (str)
            list_name (str):
        Returns:

        """
        params = dict({
            'list_name': list_name
        })

        return self._v2_request('{}/{}'.format(self.LIST, list_id), self.HTTP_PUT, params)
        
    def delete_list(self, list_id):
        """
        Deletes a list by it's ID
        Args:
            list_id (str)
        Returns:


        """
        return self._v2_request('{}/{}'.format(self.LIST, list_id), self.HTTP_DELETE)

    def add_subscribers_to_list(self, list_id, profiles):
        """
        Uses the subscribe endpoint to subscribe user to list, this obeys the list settings
        Args:
            list_id (str): klaviyo list id
            profiles (dict): for POST -> data must be a list of objects
        Returns:

        """
        params = {
            "profiles": profiles
        }
        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.SUBSCRIBE), self.HTTP_POST, params)

    def add_members_to_list(self, list_id, profiles):
        """
        This will just add a user to a list regardless of the settings
        Args:
            list_id (str): klaviyo list id
            profiles (dict): for POST -> data must be a list of objects
        """
        params = {
            "profiles": profiles
        }
        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, self.MEMBERS), self.HTTP_POST, params)

    def get_subscription_status(self, list_id):
        """
        Args:

        Return:

        """
        pass

    def unsubscribe_from_list(self, list_id, emails, subscription_type='subscribe'):
        """

        Args:
            list_id: str() the list id
            subscription_type: str() subscribe or members depending on the action
            emails: a list of emails
        Returns

        """

        params = {
            'emails': emails
        }
        return self._v2_request('{}/{}/{}'.format(self.LIST, list_id, subscription_type), self.HTTP_DELETE, params)

    def list_exclusions(self, list_id, marker=None):
        """

        Args:
            list_id: str() the list id
            marker: int() optional returned from the previous get call
        Returns:

        """
        params = self._build_marker_param(marker)

        return self._v2_request('{}/{}/exclusions/{}'.format(self.LIST, list_id, self.ALL), params)

    def all_members(self, group_id, marker=None):
        """

        Args:
            id: str() the list id or the segment id
            marker: int() optional returned from the previous get call
        """
        params = self._build_marker_param(marker)

        return self._v2_request('group/{}/{}/{}'.format(group_id, self.MEMBERS, self.ALL), params)
