'''
module to get live bond prices from server.

pip install Y:\DL_trade\code\python\tests\pub_sub\version_2.0\Bluefin-0.0.2-py3-none-any.whl


'''



import time
import random

import pandas as pd

# bluefin internal pubsub modules
from Bluefin.core.observable import Observer
from Bluefin.pubsub.client import Client


class SubscriptionObserver(Observer):

    def __init__(self):
        self.count = 0

    def notice(self, subscription):
        # print(subscription.__dict__)
        s = subscription
        print(f'topic: {s.topic}, field: {s.field}, value: {s.value}, last_update: {s.last_update}')
        self.count += 1
        print('data hits:', self.count)

        # perform every 500 changes
        if self.count % 100 == 0:
            perform_a_calc()
    





def main(isin_list):
    ''' entry point for the code'''

    # create Client instance & subscribe
    global client
    client = Client("londondl.p2p.bluefintrading.com", 44803, "Darren Lefcoe")
    client.subscription_event.listen(SubscriptionObserver())
    client.run()
    
    # a list of (topic, field) tuples too listen to
    # file_with_list = 'Y:\\DL_trade\\system_files\\unique_bonds.csv'
    # isin_list = pd.read_csv(file_with_list)['isin']


    print('the list of bond isin identifiers:')
    print(isin_list)

    # subscribe to all items in the list
    for i, isin in enumerate(isin_list):
        print('subscribing:', i, isin)
        client.subscribe(isin, 'final mid')
   

    done = False

    while not done:
        client.run()
        time.sleep(3)
        # client.publish("side1", "side2", random.randint(-1000,1000))

    return




def perform_a_calc():
    x = random.randint(-1000,1000)
    print(f'publishing: (some_ETF, fair_value) = {x}')
    client.publish('some_ETF', 'fair_value', x)


    return





if __name__ == '__main__':
    main()        


