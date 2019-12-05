from .api_helper import KlaviyoAPI

class Profiles(KlaviyoAPI):
    PERSON = 'person'

    def get_profile(self, profile_id):
        """
        https://www.klaviyo.com/docs/api/people#person
        Get a profile by it's ID
        Args:
            profile_id (str): profile id for a profile
        Returns:
            (dict): profile properties
        """
        return self._v1_request('{}/{}'.format(self.PERSON, profile_id), self.HTTP_GET)

    def get_profile_metrics_timeline(self, profile_id, since=None, count=100, sort='desc'):
        """
        https://www.klaviyo.com/docs/api/people#metrics-timeline
        Gets a timeline of events on a profile
        Args:
            profile_id (str): unique id for profile
            since (unix timestamp int or uuid str): a timestamp or uuid
            count (int): the batch of records the response should return
            sort (str): the order in which results should be returned
        Returns:
            (dict): event data related to a profile
        """
        params = {
            self.COUNT: count,
            self.SORT: sort,
            self.SINCE: since,
        }
        filtered_params = self._filter_params(params)

        return self._v1_request('{}/{}/{}/{}'.format(
                self.PERSON,
                profile_id,
                self.METRICS,
                self.TIMELINE
            ),
            self.HTTP_GET,
            filtered_params
        )

    def get_profile_metrics_timeline_by_id(self, profile_id, metric_id, since=None, count=100, sort='desc'):
        """
        https://www.klaviyo.com/docs/api/people#metric-timeline
        Gets a profiles event data for one metric
        Args:
            profile_id (str): unique id for profile
            metric_id (str): unique id for metric
            since (unix timestamp int or uuid str): a timestamp or uuid
            count (int): the batch of records the response should return
            sort (str): the order in which results should be returned
        Returns:
            (dict): information about the specified metric id for the profile
        """
        params = {
            self.COUNT: count,
            self.SORT: sort,
            self.SINCE: since,
        }
        filtered_params = self._filter_params(params)

        return self._v1_request('{}/{}/{}/{}/{}'.format(
                self.PERSON,
                profile_id,
                self.METRIC,
                metric_id,
                self.TIMELINE
            ),
            self.HTTP_GET,
            filtered_params
        )
