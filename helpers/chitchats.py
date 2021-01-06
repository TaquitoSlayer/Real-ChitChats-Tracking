import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import bs4 as bs

# chitchats doesnt really have documentation on returns so lets expect 200s
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
r = requests.Session()
r.mount("https://", adapter)
r.mount("http://", adapter)

def get_inducted(client_id, cc):
    headers = {
        'Authorization': f'{cc}',
        'Content-Type': 'application/json'
    }

    # only use inducted because that means country courier said yuh i got it
    resp = r.get(f'https://chitchats.com/api/v1/clients/{client_id}/shipments?status=inducted', headers = headers)

    return resp.json()

def get_asendia(tracking_number):
    # asendia api has a key and a trackingKey, does it matter?
    headers = {
    'Host': 'a1api.asendiausa.com',
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'accept': 'application/json',
    'x-asendiaone-apikey': '32337AB0-45DD-44A2-8601-547439EF9B55',
    'sec-ch-ua-mobile': '?0',
    'authorization': 'Basic Q3VzdEJyYW5kLlRyYWNraW5nQGFzZW5kaWEuY29tOjJ3cmZzelk4cXBBQW5UVkI=',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://a1.asendiausa.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://a1.asendiausa.com/',
    'accept-language': 'en-US,en;q=0.9',
    }

    resp = r.get(f'https://a1api.asendiausa.com/api/A1/TrackingBranded/Tracking?trackingKey=AE654169-0B14-45F9-8498-A8E464E13D26&trackingNumber={tracking_number}', headers=headers)
    if 'trackingBrandedSummary' in resp.text:
        real_tracking_number = resp.json()['trackingBrandedSummary']['trackingNumberVendor']
        tracking_link = resp.json()['trackingBrandedSummary']['finalMileTrackingLink']
        destination = resp.json()['trackingBrandedSummary']['destinationCountry']
    else:
        real_tracking_number = resp.json()['trackingNumberVendor']
        tracking_link = resp.json()['finalMileTrackingLink']
        destination = resp.json()['destinationCountry']
    
    return real_tracking_number, tracking_link, destination