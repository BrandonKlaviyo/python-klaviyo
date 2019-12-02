## What is Klaviyo?

Klaviyo is a real-time service for understanding your customers by aggregating all your customer data, identifying important groups of customers and then taking action.
http://www.klaviyo.com/

## What does this package do?

* Track customers and events directly from your backend.
* Track customers and events via JavaScript using a Django middleware.


## How to install?

    easy_install klaviyo

or

    pip install klaviyo


## API Examples

After installing the klaviyo package you can initiate it using your public token which is for track events or identifying profiles and/or your private api key to utilize the metrics and list apis.

    import klaviyo

    client = klaviyo.api.Klaviyo(public_token=PUBLIC_TOKEN, private_token=PRIVATE_TOKEN)

You can then easily use Klaviyo to track events or identify people.  Note, track and identify requests take your public token.

    # Track an event...
    client.track('Filled out profile', email='someone@mailinator.com', properties={
        'Added social accounts' : False,
    })
    
    # you can also add profile properties
    client.track(
      'Filled out profile', 
      email='someone@mailinator.com', 
      properties={
        'Added social accounts' : False,
      }, 
      customer_properties={
        '$first_name': 'Thomas',
        '$last_name': 'Jefferson'
      }
    )

    # ...or just add a property to someone
    client.identify(email='thomas.jefferson@mailinator.com', properties={
        '$first_name': 'Thomas',
        '$last_name': 'Jefferson',
        'Plan' : 'Premium',
    })

You can get metrics, a timeline of events and export analytics for a metric.  See here for more https://www.klaviyo.com/docs/api/metrics

    # return all metrics
    client.get_metrics()
    
    # you can paginate through using the page offset and count param
    client.get_metrics(page=1, count=50)
    
    # return a timeline of all metrics
    # default params for getting metrics - since=None; count=100;  sort='desc'
    client.get_metrics_timeline()
    
    # add a since param to get data 
    # you can paginate through using a Unix timestamp or a UUID obtained from the next attribute
    client.get_metrics_timeline(since=since)
    
    # you can query for a specific metric id
    client.get_metric_timeline_by_id(metric_id)
    
    # you can export metric data https://www.klaviyo.com/docs/api/metrics#metric-export
    params:
        start_date
        end_date
        unit
        measurement
        where 
        by
        count

    client.metric_export(metric_id)

You can create, update, read, and delete lists.  See here for more information https://www.klaviyo.com/docs/api/v2/lists

    # to get all lists
    client.Lists.get_lists()
    
    # to add a new list
    client.Lists.create_list(list_name)
    
    # get list details
    client.Lists.get_list_by_id(list_id)
    
    # update list name
    client.Lists.update_list_name_by_id(
      list_id, 
      list_name='NEW_LIST_NAME',
    )
    
    # delete a list
    client.Lists.delete_list(list_id)

Note in the list_subscription call, subscription_type is either subscribe or members.  Please refer to the docs to see which method is correct https://www.klaviyo.com/docs/api/v2/lists#post-subscribe and https://www.klaviyo.com/docs/api/v2/lists#post-members

    # subscribe members to a list and check if they're in a list
    client.Lists.add_subscribers_to_list(list_id, profiles)
    
    # you can unsubscribe customers from a list
    client.Lists.unsubscribe_from_list(list_id, subscription_type, emails)
    
    # get exclusion emails from a list - marker is used for paginating
    client.Lists.list_exclusions(list_id, marker=None)
    
    # get all members in a group or list
    client.Lists.all_members(group_id)
    
You can fetch profile information given the profile ID

    # get profile by profile_id
    client.Profiles.get_profile(profile_id)
    
    # get all metrics for a profile with the default kwargs
    # to paginate the responses you will get a UUID returned from the response, see here for more information
    # https://www.klaviyo.com/docs/api/people#metrics-timeline
    client.Profiles.get_profile_metrics_timeline(profile_id, since=None, count=100, sort='desc')

    # get all metrics for a profile with the default kwargs
    # to paginate the responses you will get a UUID returned from the response, see here for more information
    # https://www.klaviyo.com/docs/api/people#metrics-timeline
    client.Profiles.get_profile_metric_timeline(profile_id, metric_id, since=None, count=100, sort='desc')

## How to use it with a Django application?

To automatically insert the Klaviyo script in your Django app, you need to make a few changes to your settings.py file. First,
add the following setting:

    KLAVIYO_API_TOKEN = 'YOUR_KLAVIYO_API_TOKEN'

then add the Klaviyo middleware at the top of the `MIDDLEWARE_CLASSES`:

    MIDDLEWARE_CLASSES = [
        'klaviyo.middleware.KlaviyoSnippetMiddleware',
        # Other classes
    ]

This will automatically insert the Klaviyo script at the bottom on your HTML page, right before the closing `body` tag.