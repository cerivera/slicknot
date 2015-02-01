import json
import keys
import requests
import csv
import StringIO
import re
import time
import redis

CACHE_EXPIRE_SECONDS = 60*60*24
LOOP_SECONDS = 60*60


def fetch_deals(cache):
    print("Fetching deals")
    response = requests.get(keys.KIMONO_URL)
    _json = json.loads(response.text)

    for deal in _json['results']['collection1']:
        text = deal['fp_titles']['text'].strip()
        link = deal['fp_titles']['href'].strip()

        if cache.exists(text):
            cache.expire(text, CACHE_EXPIRE_SECONDS) 
        else:
            cache.setex(text, json.dumps({
                'link': link, 
                'notified': []
            }), CACHE_EXPIRE_SECONDS)


def run_queries(cache):
    print("running queries")
    response = requests.get(keys.QUERIES_URL)
    _csv = csv.reader(StringIO.StringIO(response.text))
    _csv.next()
    count = 0
    for row in _csv:
        print(row)
        email = row[0].strip()
        query = row[1].strip()
        _regex = re.compile(query)
        for key in cache.keys():
            if _regex.match(key):
                json_val = json.loads(cache.get(key))
                if email not in json_val['notified']:
                    # TODO Send notification email
                    json_val['notified'].append(email)
                    cache.setex(key, json.dumps(json_val), cache.ttl(key))
        count += 1

    print("Queries: %s" % count)

if __name__ == '__main__':
    cache = redis.Redis(host='localhost', port=6379, db=0)

    while True:
        deals = fetch_deals(cache)
        queries = run_queries(cache)
        time.sleep(LOOP_SECONDS)

