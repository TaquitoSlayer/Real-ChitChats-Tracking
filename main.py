from helpers import chitchats
from helpers import ebay
import json
import logging

logging.basicConfig(level=logging.INFO, format = '%(asctime)s: %(message)s')
logging.basicConfig(filename='debug.log',level=logging.DEBUG, format = '%(asctime)s: %(message)s')

with open(f'./config/couriers.json') as f:
  couriers = json.load(f)

with open(f'./config/info.json') as f:
  data = json.load(f)
cc = data['chitchats']['access_token']
client_id = data['chitchats']['client_id']
# get inducted orders that have asendia as the courier
resp = chitchats.get_inducted(client_id, cc)

asendia_tracking_inducted = []
for x in resp:
    if x['carrier'] == 'asendia':
        asendia_tracking_inducted.append(x['carrier_tracking_code'])

# list of orders and their info to finish up and edit ebay orders
asendia_orders = []
for x in asendia_tracking_inducted:
    real_tracking_number, tracking_link, destination = chitchats.get_asendia(x)

    tracking_dict = {
        'asendiaTracking': x,
        'destination': destination,
        'trackingNumber': real_tracking_number,
        'trackingURL': tracking_link
    }
    asendia_orders.append(tracking_dict)


ebay_orders = ebay.get_orders()

for x in ebay_orders:
    for y in asendia_orders:
        if str(x['trackingNumber']) == str(y['asendiaTracking']):
            logging.info('found real tracking number for asendia')
            print(x['trackingNumber'], '-->', y['trackingNumber'])
            courier_name = couriers[destination]
            real_tracking = y['trackingNumber']
            order_to_change = x['orderID']

            if 'usps' in y['trackingURL']:
                courier_name = 'USPS'
            logging.info('changing now...')
            resp = ebay.update_tracking(order_to_change, real_tracking, courier_name)
            print(resp.reply)





