import asyncio
import aiohttp
import json

API_URL = 'https://www.kimonolabs.com/api/6htta1k8?apikey=yMslDnCVP4I9LZDZg25U1O29zwCvtGrR'

@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read_and_close())


@asyncio.coroutine
def print_slickdeals():
    result = yield from get(API_URL)
    json_result = json.loads(result.decode())

    print(json_result['thisversionrun'])
    for deal in json_result['results']['collection1']:
        print("%s:%s"%(deal['fp_titles']['text'], deal['fp_titles']['href']))



loop = asyncio.get_event_loop()
loop.run_until_complete(print_slickdeals())


