from klaviyo.resources.api import Klaviyo

class Campaigns(KlaviyoAPI):
    CAMPAIGN = 'campaign'
    CAMPAIGNS = 'campaigns'
    SEND = 'send'
    SCHEDULE = 'schedule'
    CANCEL = 'cancel'
    CLONE = 'clone'
    RECIPIENTS = 'recipients'
    
    
    def get_campaigns(self, page=0, count=50):
        """
        https://www.klaviyo.com/docs/api/campaigns#campaigns
        Fetch campaigns from an account
        Args:
            page (int): page number for pagination
            count (int): total count for response, max is 100
        Returns:
            
        """
        params = {
            'page': page,
            'sort': count,
        }

        params = self._filter_params(params)
        path = '{}'.format(self.CAMPAIGNS)

        return self._v1_request(url, self.HTTP_GET, params)

    def create_campaign(
        self, 
        list_id,
        template_id,
        from_email,
        from_name,
        subject,
        name=None,
        use_smart_sending=True,
        add_google_analytics=False
        ):
        """
        https://www.klaviyo.com/docs/api/campaigns#create-campaign
        Args:
            list_id (str): The ID of the List object you will send this campaign to
            template_id (str): The ID of the Email Template object that will be the content of this campaign. Note the Email Template is copied when creating this campaign, so future changes to that Email Template will not alter the content of this campaign
            from_email (str): The email address your email will be sent from and will be used in the reply-to header
            from_name (str): The name or label associated with the email address you're sending from.
            subject (str): The subject line of the email
            name (str): Optional - Name for the campaign or default to subject line
            use_smart_sending (bool): If set, limits the number of emails sent to an individual within a short period. If not specified, defaults to True
            add_google_analytics (bool): If specified, adds Google Analytics tracking tags to links. If not specified, defaults to False
        Returns:
            (dict): information about the created campagin
        """
        params = {
            'list_id': template_id,
            'from_email': from_email,
            'from_name': from_name,
            'subject': subject,
            'name': name,
            'use_smart_sending': use_smart_sending,
            'add_google_analytics': add_google_analytics,
        }

        params = self._filter_params(params)
        url = '{}'.format(self.CAMPAIGNS)

        return self._v1_request(url, self.HTTP_POST, params)
        
        
        
