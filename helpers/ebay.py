from ebaysdk.trading import Connection

api = Connection(config_file="./config/ebay.yaml", domain="api.ebay.com")

# find the matching asendia tracking number and grab the orderid with it
# we plan to use order id to update tracking number with CompleteSale
def get_orders():
    orders = []
    resp = api.execute("GetSellerTransactions")
    for x in resp.reply.TransactionArray.Transaction:
        order_id = x.OrderLineItemID
        user = x.Buyer.UserID
        try:
            shipping_details = x.ShippingDetails.ShipmentTrackingDetails

            # if we have multiple tracking numbers, iterate
            is_list = type(shipping_details).__name__ == 'list'
            if is_list:
                for detail in shipping_details:
                    shipping = {
                        'courier': detail.ShippingCarrierUsed,
                        'trackingNumber': detail.ShipmentTrackingNumber,
                        'orderID': order_id,
                        'username': user
                    }

                    orders.append(shipping)
            else:
                shipping = {
                        'courier': shipping_details.ShippingCarrierUsed,
                        'trackingNumber': shipping_details.ShipmentTrackingNumber,
                        'orderID': order_id,
                        'username': user
                    }

                orders.append(shipping)
        except:
            # will happen if no tracking info was added
            print(f'No tracking info found for {order_id} - {user}')
            pass
    
    return orders

def update_tracking(order_id, tracking_number, post_ops):
    request = {
        "OrderLineItemID": order_id,
        "Shipment": {
            "ShipmentTrackingDetails": {
                "ShipmentTrackingNumber": tracking_number,
                "ShippingCarrierUsed": post_ops
            }
        }
    }
    resp = api.execute("CompleteSale", request)
    return resp
        