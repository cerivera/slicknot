import json
import settings
import requests
import csv
import StringIO
import re
import time
import redis
import mandrill

CACHE_EXPIRE_SECONDS = 60*60*24

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY) 


# TODO Don't fetch if you've already processed the latest results
def fetch_deals(kimono_endpoint):
    print("Fetching deals: %s" % kimono_endpoint)
    response = requests.get(kimono_endpoint)
    _json = json.loads(response.text)

    
    collection = _json['results']['collection1'] if 'collection1' in _json['results'] else _json['results']['collection2']

    for deal in collection:
        text = deal['title']['text'].strip()
        link = deal['title']['href'].strip()
        price = deal['price']['text'].strip() if type(deal['price']) is dict else deal['price'].strip()

        if redis_client.exists(text):
            redis_client.expire(text, CACHE_EXPIRE_SECONDS) 
        else:
            redis_client.setex(text, json.dumps({
                'link': link, 
                'notified': [],
                'price': price
            }), CACHE_EXPIRE_SECONDS)


def run_queries(csv_endpoint):
    print ("Running queries")
    deals = []
    response = requests.get(csv_endpoint)
    _csv = csv.reader(StringIO.StringIO(response.text))
    for row in _csv:
        query = row[0].strip()
        _regex = re.compile(query, re.IGNORECASE)
        for key in redis_client.keys():
            if _regex.search(key):
                json_val = json.loads(redis_client.get(key))
                if settings.NOTIFICATION_EMAIL not in json_val['notified']:
                    deals.append({
                        'title': key,
                        'link': json_val['link'],
                        'price': json_val['price']
                    })
                    json_val['notified'].append(settings.NOTIFICATION_EMAIL)
                    redis_client.setex(key, json.dumps(json_val), redis_client.ttl(key))

    return deals




def send_email(email, html):
    message = {
     'from_email': 'rivera.utx@gmail.com',
     'from_name': 'Slicknot',
     'html': html,
     'subject': 'Deals',
     'to': [{'email': email,
             'name': 'Carlos',
             'type': 'to'}]}

    result = mandrill_client.messages.send(message=message)
    print(result)


if __name__ == '__main__':

    pending_deal_notifications = []
    for endpoint in settings.ENDPOINTS:
        if endpoint['status']:
            fetch_deals(endpoint['api'])
            pending_deal_notifications += run_queries(endpoint['csv'])

    if len(pending_deal_notifications) > 0:
        html = ''
        for deal in pending_deal_notifications:
            html += '<p>%s - %s</p><p>%s</p><br />' % (deal['title'], deal['price'], deal['link'])

        send_email(settings.NOTIFICATION_EMAIL, html)
