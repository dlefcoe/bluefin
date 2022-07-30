'''

example of single item subscribe
testing


formula to push data in excel:
    =P2PPublish(server,topic,field,value,t)
where:
    server = "londl"
    topic = "side1"
    field = "side2"
    value = "any value"
    t = today()

author: @dlefcoe
contact: dlefcoe@bluefintrading.com


'''

# standard modules
import time
import random

# bluefin internal pubsub modules
from Bluefin.core.observable import Observer
from Bluefin.pubsub.client import Client


class SubscriptionObserver(Observer):
    ''' class for subscribing '''

    def __init__(self, the_dict):
        self.count = 0
        self.the_dict = the_dict

    def notice(self, subscription):
        ''' an action is performed here '''
        # print(subscription.__dict__)
        s = subscription
        print(f'topic: {s.topic}, field: {s.field}, value: {s.value}, last_update: {s.last_update}')
        self.count += 1
        print('data hits:', self.count)
        self.the_dict[(s.topic, s.field)] = s.value
        # self.the_dict[s.topic+ "/"+ s.field] = s.value # coule make a string key but Tuples are better!



def main():
    ''' main entry point of the code '''

    # create Client instance
    global client
    client = Client("londondl.p2p.bluefintrading.com", 44803, "Darren Lefcoe")
    
    my_dict = {}
    # listen
    client.subscription_event.listen(SubscriptionObserver(my_dict))
    
    # subscribe
    client.subscribe(topic='hello', field='world')

    # run client (for 3 seconds)
    whilecounter = 0
    while whilecounter<2:
        client.run()
        time.sleep(1)
        whilecounter += 1

    # print('just the value:', my_dict[('hello', 'world')])
    # print('the whole dict:', my_dict)

    return my_dict



if __name__=='__main__':
    # run if main
    a = main()
    print(a)




