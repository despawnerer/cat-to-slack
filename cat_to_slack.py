import schedule
import requests
import time
import collections
import json
import logging
import sys
import os
import random


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout,
)


# errors

class CatShortageError(RuntimeError):
    pass


# fetching cats

CAT_URL = "https://www.reddit.com/r/CatGifs/top.json"
CAT_PARAMS = {'sort': 'top', 't': 'day'}
CAT_HEADERS = {
    'User-Agent': 'Cat to Slack 1.0',
}

last_cats = collections.deque([], 30)


def get_new_cat():
    response = requests.get(CAT_URL, params=CAT_PARAMS, headers=CAT_HEADERS)
    posts = response.json()['data']['children']
    for post in posts:
        cat = post['data']['url']
        if cat not in last_cats:
            last_cats.append(cat)
            return cat
    else:
        raise CatShortageError


# posting cats

INCOMING_WEBHOOK_URL = os.environ.get('INCOMING_WEBHOOK_URL')
CAT_EMOJIS = [
    ':smiley_cat:', ':smile_cat:', ':joy_cat:', ':heart_eyes_cat:',
    ':smirk_cat:', ':kissing_cat:', ':scream_cat:', ':crying_cat_face:',
    ':pouting_cat:', ':cat:', ':cat2:',
]
PAYLOAD_PARAMS = {
    "channel": os.environ.get('CAT_CHANNEL'),
    "username": "Cat",
    "unfurl_media": True,
    "unfurl_links": True,
}


def post_cat(cat):
    payload = PAYLOAD_PARAMS.copy()
    payload['text'] = '<%s>' % cat
    payload['icon_emoji'] = random.choice(CAT_EMOJIS)
    return requests.post(INCOMING_WEBHOOK_URL, data={
        'payload': json.dumps(payload)
    })


# the job

def post_new_cat():
    try:
        cat = get_new_cat()
    except CatShortageError:
        logging.warning("No new cats available!")
        return
    except Exception as exc:
        logging.exception("Failed to get cat :( %s" % exc, exc_info=True)
        return
    else:
        logging.info("Have cat: %s" % cat)

    try:
        response = post_cat(cat)
        response.raise_for_status()
    except:
        logging.error("Failed to post cat :( %s" % response)
        return
    else:
        logging.info("Posted cat: %s" % response)


# the schedule

CAT_TIMES = os.environ.get('CAT_TIMES', '10:00').split(',')

for cat_time in CAT_TIMES:
    logging.info("Adding daily schedule at %s" % cat_time)
    schedule.every().day.at(cat_time).do(post_new_cat)

while 1:
    schedule.run_pending()
    time.sleep(1)
