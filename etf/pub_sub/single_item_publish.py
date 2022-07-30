'''

example of single item publish
testing


formula to get data in excel:
    =RTD("bluefin.p2p.rtd",,server,topic,field)
where:
    server = "londl"
    topic = "side1"
    field = "side2"

author: @dlefcoe
contact: dlefcoe@bluefintrading.com


'''

# standard modules
import random

# bluefin internal pubsub modules
from Bluefin.pubsub.client import Client




def main():
    ''' main entry point of the code '''

    # create Client instance
    global client
    client = Client("londondl.p2p.bluefintrading.com", 44803, "Darren Lefcoe")
    
    # publish something
    client.publish("side1", "side2", random.randint(-1000,1000))
    client.run()
    client.run()


    return 'done'




if __name__=='__main__':
    # run if main
    a = main()
    print(a)




