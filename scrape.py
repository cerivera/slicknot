import json
import keys
import requests
import csv
import StringIO
import re
import time
import redis
import mandrill

CACHE_EXPIRE_SECONDS = 60*60*24
LOOP_SECONDS = 60*60

redis_client = redis.Redis(host=keys.REDIS_HOST, port=keys.REDIS_PORT, db=0)
mandrill_client = mandrill.Mandrill(keys.MANDRILL_API_KEY) 


# TODO Don't fetch if you've already processed the latest results
def fetch_deals():
    print("Fetching deals")
    response = requests.get(keys.KIMONO_URL)
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
    response = requests.get(keys.QUERIES_URL)
    _csv = csv.reader(StringIO.StringIO(response.text))
    for row in _csv:
        query = row[0].strip()
        _regex = re.compile(query, re.IGNORECASE)
        for key in redis_client.keys():
            if _regex.search(key):
                json_val = json.loads(redis_client.get(key))
                if keys.NOTIFICATION_EMAIL not in json_val['notified']:
                    send_deal_notification(keys.NOTIFICATION_EMAIL, key, json_val['link'])
                    json_val['notified'].append(keys.NOTIFICATION_EMAIL)
                    redis_client.setex(key, json.dumps(json_val), redis_client.ttl(key))


def send_deal_notification(email, title, link):
    print("Notifying about '%s'" % title)
    message = {
     'from_email': 'rivera.utx@gmail.com',
     'from_name': 'Slicknot',
     'html': '<p>%s</p><p><a href="%s">%s</a></p>' % (title, link, link),
     'subject': title,
     'to': [{'email': email,
             'name': 'Carlos',
             'type': 'to'}]}

    result = mandrill_client.messages.send(message=message)
    print(result)


if __name__ == '__main__':
    while True:
        deals = fetch_deals()
        queries = run_queries()
        time.sleep(LOOP_SECONDS)

