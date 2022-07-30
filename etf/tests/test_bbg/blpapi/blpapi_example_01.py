# SubscriptionWithEventHandlerExample.py

import blpapi
import blpapi.logging
from optparse import OptionParser
import time

EXCEPTIONS = blpapi.Name("exceptions")
FIELD_ID = blpapi.Name("fieldId")
REASON = blpapi.Name("reason")
CATEGORY = blpapi.Name("category")
DESCRIPTION = blpapi.Name("description")

SessionConnectionDown = blpapi.Name("SessionConnectionDown")
SessionConnectionUp = blpapi.Name("SessionConnectionUp")
SessionTerminated = blpapi.Name("SessionTerminated")
ServiceDown = blpapi.Name("ServiceDown")
SlowConsumerWarning = blpapi.Name("SlowConsumerWarning")
SlowConsumerWarningCleared = blpapi.Name("SlowConsumerWarningCleared")
DataLoss = blpapi.Name("DataLoss")

ServiceName = blpapi.Name("serviceName")
# authorization 
AUTHORIZATION_SUCCESS = blpapi.Name("AuthorizationSuccess")
AUTHORIZATION_FAILURE = blpapi.Name("AuthorizationFailure")
AUTHORIZATION_REVOKED = blpapi.Name("AuthorizationRevoked")
TOKEN_SUCCESS = blpapi.Name("TokenGenerationSuccess")
TOKEN_FAILURE = blpapi.Name("TokenGenerationFailure")
TOKEN = blpapi.Name("token")

g_session = None
g_sessionStarted = False
g_subscriptions = None
g_identity = None
g_authCorrelationId = None

class CorrelationInfo:
    def __init__(self, topic):
        self.topic = topic

    def getTopic(self):
        return self.topic

class SubscriptionEventHandler(object):
    def getTimeStamp(self):
        return time.strftime("%Y/%m/%d %X")

    #
    # Process Session Status 
    #
    # session connected message
    #SessionConnectionUp = {
    #    server = "127.0.0.1:8194"
    #}
    
    # session started message
    #SessionStarted = {}
    
    # session disconnected message
    #SessionConnectionDown = {
    #    server = "127.0.0.1:8194"
    #}

    # session terminated message
    #SessionTerminated = {
    #    reason = {
    #    }
    #}
    def processSessionStatus(self, event):
        timeStamp = self.getTimeStamp()
        print("Processing SESSION_STATUS")
        for msg in event:
            if msg.messageType() == SessionConnectionDown:
                # API connection disconnect (Session still active)
                print("%s: Session connection down detected: %s" % (timeStamp, msg))
            elif msg.messageType() == SessionConnectionUp:
                # API connection up (Session still active)
                print("%s: Session connection up detected: %s" % (timeStamp, msg))
            elif msg.messageType() == SessionTerminated:
                # Session no longer active
                print("%s: Session terminated!: %s" % (timeStamp, msg))
                g_sessionStarted = False
            else:
                # misc messages
                print("%s: Misc session message: %s" % (timeStamp, msg))
               
    def processServiceStatus(self, event):
        timeStamp = self.getTimeStamp()
        print("Processing SESSION_STATUS")
        for msg in event:
            if msg.messageType() == ServiceDown:
                if msg.hasElement(ServiceName, True):
                    if msg.getElement(ServiceName).getValueAsString() == "//blp/mktdata":
                        # API connection disconnect (Session still active)
                        print("%s: //blp/mktdata service down detected: %s" % (timeStamp, msg))
            else:
                # misc messages
                print("%s: Misc session message: %s" % (timeStamp, msg))
        
    def processSubscriptionStatus(self, event):
        timeStamp = self.getTimeStamp()
        print ("Processing SUBSCRIPTION_STATUS")
        for msg in event:
            cInfo = msg.correlationIds()[0].value()
            print ("%s: %s - %s" % (timeStamp, cInfo.getTopic(), msg.messageType()))
            print (msg)

            if msg.hasElement(REASON):
                # This can occur on SubscriptionFailure.
                reason = msg.getElement(REASON)
                if msg.hasElement(CATEGORY) and msg.hasElement(DESCRIPTION):
                    print ("        %s: %s" % (
                        reason.getElement(CATEGORY).getValueAsString(),
                        reason.getElement(DESCRIPTION).getValueAsString()))

            if msg.hasElement(EXCEPTIONS):
                # This can occur on SubscriptionStarted if at least
                # one field is good while the rest are bad.
                exceptions = msg.getElement(EXCEPTIONS)
                for exInfo in exceptions.values():
                    fieldId = exInfo.getElement(FIELD_ID)
                    reason = exInfo.getElement(REASON)
                    print ("        %s: %s" % (
                        fieldId.getValueAsString(),
                        reason.getElement(CATEGORY).getValueAsString()))

    def processSubscriptionDataEvent(self, event):
        timeStamp = self.getTimeStamp()
        print ()
        print ("Processing SUBSCRIPTION_DATA")
        for msg in event:
            cInfo = msg.correlationIds()[0].value()
            print ("%s: %s - %s" % (timeStamp, cInfo.getTopic(), msg.messageType()))
            for field in msg.asElement().elements():
                if field.numValues() < 1:
                    print ("        %s is NULL" % field.name())
                    continue

                # Assume all values are scalar.
                print( "        %s = %s" % (field.name(),
                                           field.getValueAsString()))

    def processAdmin(self, event):
        timeStamp = self.getTimeStamp()
        for msg in event:
            if msg.messageType() == SlowConsumerWarning:
                print ("!!!! Slow consumer warning !!!! ")
            elif msg.messageType() == SlowConsumerWarningCleared:
                print ("!!!! Slow consumer warning cleared !!!! ")
            else:
                print ("%s: %s\n%s" % (timeStamp, msg.messageType(), msg))



    def processMiscEvents(self, event):
        timeStamp = self.getTimeStamp()
        for msg in event:
            print ("%s: %s\n%s" % (timeStamp, msg.messageType(), msg))

    def processEvent(self, event, session):
        try:
            if event.eventType() == blpapi.Event.SUBSCRIPTION_DATA:
                return self.processSubscriptionDataEvent(event)
            elif event.eventType() == blpapi.Event.SUBSCRIPTION_STATUS:
                return self.processSubscriptionStatus(event)
            elif event.eventType() == blpapi.Event.SESSION_STATUS:
                return self.processSessionStatus(event)
            elif event.eventType() == blpapi.Event.SERVICE_STATUS:
                return self.processServiceStatus(event)
            elif event.eventType() == blpapi.Event.ADMIN:
                return self.processAdmin(event)

            else:
                return self.processMiscEvents(event)
        except blpapi.Exception as e:
            print ("Library Exception !!! %s" % e.description())
        return False

def authorize(p_cid):
    is_authorized = None
    WAIT_TIME_SECONDS = 10
    authService = g_session.getService("//blp/apiauth")

    # generate token
    identity = g_session.createIdentity()
    tokenEventQueue = blpapi.EventQueue()
    g_session.generateToken(eventQueue=tokenEventQueue)

    # Process token response
    ev = tokenEventQueue.nextEvent(WAIT_TIME_SECONDS * 1000)
    token = None
    if ev.eventType() == blpapi.Event.TOKEN_STATUS:
        for msg in ev:
            print (msg)
            if msg.messageType() == TOKEN_SUCCESS:
                token = msg.getElementAsString(TOKEN)
            elif msg.messageType() == TOKEN_FAILURE:
                break
    elif ev.eventType() == blpapi.Event.REQUEST_STATUS:
        # request failure
        for msg in ev:
            print (msg)
    elif ev.eventType() == blpapi.Event.TIMEOUT:
        print ("Generate token response did not return within the timeout given timeout period")

    if not token:
        print ("Failed to get token")
    else:
        # Create and fill the authorithation request
        authRequest = authService.createAuthorizationRequest()
        authRequest.set(TOKEN, token)
        
        eventQueue = blpapi.EventQueue()
        
        # Send authorithation request to "fill" the Identity
        identity = g_session.createIdentity()
        g_session.sendAuthorizationRequest(authRequest, identity, p_cid, eventQueue)
        
        # Process related responses
        event = eventQueue.nextEvent(WAIT_TIME_SECONDS * 1000)
        if event.eventType() == blpapi.Event.RESPONSE or \
            event.eventType() == blpapi.Event.PARTIAL_RESPONSE:
            if event.eventType() == blpapi.Event.PARTIAL_RESPONSE:
                print ("Warning: Received authorization partial response. The authorization requestion should be sent asynchronously")
            for msg in event:
                print (msg)
                if msg.messageType() == AUTHORIZATION_SUCCESS:
                    is_authorized = identity
                else:
                    print ("Authorization failed")
        elif ev.eventType() == blpapi.Event.REQUEST_STATUS:
            # request failure
            for msg in ev:
                print (msg)
        elif ev.eventType() == blpapi.Event.TIMEOUT:
            print ("Generate token response did not return within the timeout given timeout period")
            g_session.cancel(p_cid)
    return is_authorized

def subscribe(p_identity):
    subscriptionOptions = []
    fieldList = []
    fieldList.append("ASK")
    fieldList.append("BID")
    fieldList.append("EID")
    fieldList.append("MKTDATA_EVENT_TYPE")
    fieldList.append("MKTDATA_EVENT_SUBTYPE")
    fieldList.append("IS_DELAYED_STREAM")
    subscriptionOptions1 = []
    cInfo = CorrelationInfo("/isin/XS1412266907")
    cId = blpapi.CorrelationId(cInfo)
    g_subscriptions.add(cInfo.getTopic(), fieldList, subscriptionOptions1, cId)
    g_session.subscribe(g_subscriptions, p_identity)



# callback for BLPAPI logging
def onMessage(threadId, traceLevel, dateTime, loggerName, message):
    print("%s %s [%s] Thread ID = %s %s" %
          (dateTime, loggerName, traceLevel, threadId, message))



def main():
    global g_session, g_sessionStarted, g_subscriptions , g_identity, g_authCorrelationId

    # set BLPAPI log level
    blpapi.logging.Logger.registerCallback(onMessage, blpapi.logging.Logger.SEVERITY_OFF)

    # Fill SessionOptions
    options = blpapi.SessionOptions()
    g_subscriptions = blpapi.SubscriptionList()

    options.setServerHost("69.184.252.19")
    options.setAuthenticationOptions("AuthenticationType=OS_LOGON")


    print("Session options: %s" % options)
    eventHandler = SubscriptionEventHandler()
    # Create a Session
    g_session = blpapi.Session(options, eventHandler.processEvent)

    # Start a Session
    if not g_session.start():
        print ("Failed to start session.")
        return

    print ("Connected successfully")
    g_sessionStarted = True

    service = "//blp/mktdata"
    if not g_session.openService(service):
        print ("Failed to open %s service" % service)
        return

    # Open authorization service
    if not g_session.openService("//blp/apiauth"):
        print("Failed to open //blp/apiauth")
        return

    # Open authorization service
    if not g_session.openService("//blp/apiauth"):
        print("Failed to open //blp/apiauth")
        return

    # Authorize user that is interested in receiving data
    g_authCorrelationId = blpapi.CorrelationId("authCorrelation");
    g_identity = authorize(g_authCorrelationId)

    if g_identity is None:
        print ("Exiting...")
        return

    print ("Subscribing...")
    subscribe(g_identity)

    try:
        # Wait for enter key to exit application
        print ("Press ENTER to quit")
        # python 2.x
        #raw_input()
        # python 3.x
        input() 
    finally:
        if g_sessionStarted:
            g_session.unsubscribe(g_subscriptions)
            # Stop the session
            g_session.stop()
            time.sleep(1)

if __name__ == "__main__":
    print ("SubscriptionWithEventHandlerExample")
    try:
        main()
    except KeyboardInterrupt:
        print ("Ctrl+C pressed. Stopping...")

__copyright__ = """
Copyright 2018. Bloomberg Finance L.P.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  The above
copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

