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
def fetch_deals():
    print("Fetching deals")
    response = requests.get(settings.KIMONO_ENDPOINT)
    _json = json.loads(response.text)

    for deal in _json['results']['collection1']:
        text = deal['fp_titles']['text'].strip()
        link = deal['fp_titles']['href'].strip()

        if redis_client.exists(text):
            redis_client.expire(text, CACHE_EXPIRE_SECONDS) 
        else:
            redis_client.setex(text, json.dumps({
                'link': link, 
                'notified': []
            }), CACHE_EXPIRE_SECONDS)


def run_queries():
    print ("Running queries")
    pending_deal_notifications = []
    response = requests.get(settings.CSV_ENDPOINT)
    _csv = csv.reader(StringIO.StringIO(response.text))
    for row in _csv:
        query = row[0].strip()
        _regex = re.compile(query, re.IGNORECASE)
        for key in redis_client.settings():
            if _regex.search(key):
                json_val = json.loads(redis_client.get(key))
                if settings.NOTIFICATION_EMAIL not in json_val['notified']:
                    pending_deal_notifications.append({
                        'title': key,
                        'link': json_val['link']
                    })
                    json_val['notified'].append(settings.NOTIFICATION_EMAIL)
                    redis_client.setex(key, json.dumps(json_val), redis_client.ttl(key))


    if len(pending_deal_notifications) > 0:
        html = ''
        for deal in pending_deal_notifications:
            html += '<p>%s</p><p>%s</p><br /><br />' % (deal['title'], deal['link'])

        send_email(settings.NOTIFICATION_EMAIL, html)


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
    fetch_deals()
    run_queries()

