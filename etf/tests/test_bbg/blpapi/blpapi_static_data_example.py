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

SECURITY_ERROR = blpapi.Name("securityError")
MESSAGE = blpapi.Name("message")
FIELD_EXCEPTION = blpapi.Name("fieldExceptions")
SEQ_NUMBER = blpapi.Name("sequenceNumber")
SECURITY_DATA = blpapi.Name("securityData")
FIELD_DATA = blpapi.Name("fieldData")
SECURITY = blpapi.Name("security")
FIELD_ID = blpapi.Name("fieldId")
ERROR_INFO = blpapi.Name("errorInfo")
EID_DATA = blpapi.Name("eidData")

g_session = None
g_sessionStarted = False
g_requestList = []
g_identity = None
g_authCorrelationId = None

class CorrelationInfo:
    def __init__(self, topic):
        self.topic = topic

    def getTopic(self):
        return self.topic

class SessionEventHandler(object):
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
                    # API service connection disconnect (Session still active)
                    print("%s: %s service down detected: %s" % (timeStamp, msg.getElement(ServiceName).getValueAsString(), msg))
                else:
                    print("%s: Service down detected: %s" % (timeStamp, msg))
            else:
                # misc messages
                print("%s: Misc session message: %s" % (timeStamp, msg))
        
    def processAdmin(self, event):
        timeStamp = self.getTimeStamp()
        for msg in event:
            if msg.messageType() == SlowConsumerWarning:
                print ("!!!! Slow consumer warning !!!! ")
            elif msg.messageType() == SlowConsumerWarningCleared:
                print ("!!!! Slow consumer warning cleared !!!! ")
            else:
                print ("%s: %s\n%s" % (timeStamp, msg.messageType(), msg))



    # process bulk field
    def processBulkField(self, bulkField):
        print ("\tBulk field: %s\n" % bulkField.name() )
        rows = bulkField.numValues()
        for rowCtr in range(rows):
            # access row data
            rowData = bulkField.getValueAsElement(rowCtr)
            # number of columns
            columns = rowData.numElements()
            for colCtr in range(columns):
                # process data
                columnData = rowData.getElement(colCtr)
                print ( "\t\t%s = %s" % (columnData.name(), columnData.getValueAsString()))

    # process PARTIAL_RESPONSE or RESPONSE event
    def processReferenceResponseEvent(self, event):
        for msg in event:
            print("Received response to request " + msg.getRequestId())
            if msg.correlationIds()[0].value():
                cID = msg.correlationIds()[0].value()
            else:
                cID = msg.correlationIds()[0].object()
            print (str(cID) + ":")
            securities = msg.getElement(SECURITY_DATA)
            securityCount = securities.numValues()
            # for Python verson prior to 3.x, please use xrange()
            for index in range(securityCount):
                security = securities.getValueAsElement(index)
                secIndex = security.getElement(SEQ_NUMBER).getValueAsInteger()
                securityName = security.getElement(SECURITY).getValueAsString()
                if security.hasElement(SECURITY_ERROR, True):
                    print ("Security error for " + securityName)
                    print (security.getElement(SECURITY_ERROR))
                else:
                    print (securityName + ":")
                    if security.hasElement(FIELD_EXCEPTION, True):
                        fieldExceptions = security.getElement(FIELD_EXCEPTION)
                        fieldExceptionCount = fieldExceptions.numValues()
                        # for Python verson prior to 3.x, please use xrange()
                        for fIndex in range(fieldExceptionCount):
                            fieldException = fieldExceptions.getValueAsElement(fIndex)
                            errorInfo = fieldException.getElement(ERROR_INFO)
                            errorMessage = ""
                            if errorInfo.hasElement(MESSAGE, True):
                                errorMessage = errorInfo.getElement(MESSAGE).getValueAsString()
                            print ("Field Exception: (" + fieldException.getElement(FIELD_ID).getValueAsString() + \
                                   ") " + errorMessage)
                    fieldData = security.getElement(FIELD_DATA)
                    # long way to get to field data to demostrate field access in fieldData element
                    fieldCount = fieldData.numValues()
                    if fieldCount > 0:
                        for fieldElement in fieldData.elements():
                            # check if field is a bulk field
                            if not fieldElement.isValid():
                                print(fieldElement.name(), "is NULL.")
                            elif (fieldElement.isArray()):
                                # process bulk field
                                self.processBulkField(fieldElement)
                            else:
                                # field value can be retreive in it's native type
                                # fieldElement.datatype()
                                print ("\t%s = %s" % (fieldElement.name(), fieldElement.getValueAsString()))
                print()

    def processMiscEvents(self, event):
        timeStamp = self.getTimeStamp()
        for msg in event:
            if event.eventType() == blpapi.Event.REQUEST_STATUS:
                if msg.correlationIds()[0].value():
                    cID = msg.correlationIds()[0].value()
                else:
                    cID = msg.correlationIds()[0].object()
                print (str(cID) + ":")
            # print message
            print ("%s: %s\n%s" % (timeStamp, msg.messageType(), msg))

    def processEvent(self, event, session):
        try:
            if event.eventType() == blpapi.Event.REQUEST_STATUS:
                # request timeout
                return self.processMiscEvents(event)
            elif event.eventType() == blpapi.Event.SESSION_STATUS:
                return self.processSessionStatus(event)
            elif event.eventType() == blpapi.Event.SERVICE_STATUS:
                return self.processServiceStatus(event)
            elif event.eventType() == blpapi.Event.ADMIN:
                return self.processAdmin(event)
            elif event.eventType() == blpapi.Event.PARTIAL_RESPONSE or \
                 event.eventType() == blpapi.Event.RESPONSE:
                return self.processReferenceResponseEvent(event)
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

def sendRequest(p_identity):
    # get service
    service = g_session.getService("//blp/refdata")

    # create request
    request = service.createRequest("ReferenceDataRequest")
    # append securities to request
    request.append("securities", "/isin/XS1412266907")

    # field list for all requests
    request.append("fields", "PX_LAST")
    # field list for all requests
    request.append("fields", "RISK_MID")
    # field list for all requests
    request.append("fields", "TICKER")
    # field list for all requests
    request.append("fields", "CPN")
    # field list for all requests
    request.append("fields", "MATURITY")


    # add request to list
    g_requestList.append(request)
    # send requests
    requestIndex = 0
    for request in g_requestList:
        # request.getRequestId() require BLPAPI version 3.16 or later
        print("Request ID: " + request.getRequestId() + "\n")
        print(request)
        g_session.sendRequest(request, p_identity, blpapi.CorrelationId("Request " + str(requestIndex)))
        requestIndex += 1
        print("\n\n")

# callback for BLPAPI logging
def onMessage(threadId, traceLevel, dateTime, loggerName, message):
    print("%s %s [%s] Thread ID = %s %s" %
          (dateTime, loggerName, traceLevel, threadId, message))



def main():
    global g_session, g_sessionStarted, g_requestList, g_identity, g_authCorrelationId

    # set BLPAPI log level
    blpapi.logging.Logger.registerCallback(onMessage, blpapi.logging.Logger.SEVERITY_OFF)

    # Fill SessionOptions
    options = blpapi.SessionOptions()

    options.setServerHost("69.184.252.19")
    options.setAuthenticationOptions("AuthenticationType=OS_LOGON")


    print("Session options: %s" % options)
    eventHandler = SessionEventHandler()
    # Create a Session
    g_session = blpapi.Session(options, eventHandler.processEvent)

    # Start a Session
    if not g_session.start():
        print ("Failed to start session.")
        return

    print ("Connected successfully")
    g_sessionStarted = True

    service = "//blp/refdata"
    if not g_session.openService(service):
        print ("Failed to open %s service" % service)
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

    # create and send request
    sendRequest(g_identity)



    try:
        # Wait for enter key to exit application
        print ("Press ENTER to quit")
        input() 
    finally:
        if g_sessionStarted:
            # Stop the session
            g_session.stop()
            time.sleep(1)

if __name__ == "__main__":
    print ("Reference Data Request Example")
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





