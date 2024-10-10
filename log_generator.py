from datetime import datetime
from datetime import timedelta
import pytz
import random
import requests
import time


def test_http_collector(body):
    api_key = "MTA4OnNWWlp2aFEyV2xtdll0UXIyT3plYjZPRFl1T2xxRmtCbm9GZW9jR0JCMFpTZDd6REZYTDRaeHVZd01KeVJJeU5tcTdOWlJaRktJeWk4VGFBQVdrYTFXOElnRFBrNzBhOEhaYnlXN3NINHdtdkdnSkZvRjJDZnpDaVdYVDM4Z1RV"

    headers = {
        "Authorization": api_key,
        "Content-Type": "text/json"
    }
    # Note: the logs must be separated by a new line
    res = requests.post(url="https://api-csxsiam.xdr.us.paloaltonetworks.com/logs/v1/event",
                        headers=headers,
                        json=body)
    return res

# Data types
instance = [
    'demo-1',
    'dev-1',
    'prod-1'
]

event = [
    'login',
    'logout'
]

result = [
    'success',
    'fail'
]

user = [
    'steve',
    'jane',
    'javier',
    'admin'
]

ip = [
    '1.1.1.1',
    '102.234.2.8',
    '8.8.8.8',
    '32.99.8.104'
]

for x in range(1,100):
    log = {
        'timestamp': (datetime.now(pytz.utc) + timedelta(0,-3)).strftime('%d/%m/%YT%H:%M:%S%z'),
        'instance': random.choice(instance),
        'event': random.choice(event),
        'result': random.choice(result),
        'user': random.choice(user),
        'ip': random.choice(ip)
    }

    # print(log)
    res = test_http_collector(log)
    if res.status_code != 200:
        print(f"Error: {res.text}")
        break
