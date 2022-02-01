import pytest
from appd.AppdApiWrapper import AppdApiWrapper
from datetime import datetime
from datetime import timedelta


api = AppdApiWrapper()

def test_getToken():
    
    testResult = ""
    testMessage = ""

    token = api.getToken()

    if  len(token["access_token"]) == 665 and token["expires_in"] == 300:
        testResult = "OK"
        testMessage = "Token generation works"
    else:
        testResult = "NOK"

    assert testResult == "OK"

def test_getAllUsers():

    testResult = "NOK"
    testMessage = "NOK"

    result = api.getAllUsers()
    if type(result) == dict:

        users = result["users"]
        user = users[0]

        if type(user["id"]) == int \
        and type(user ["name"]) == str:
            testResult = "OK"
    else:
        testResult = "NOK"

    assert testResult == "OK"

def test_getUserDetails():

    testResult = "NOK"
    testMessage = "NOK"

    result = api.getAllUsers()
    if type(result) == dict:

        users = result["users"]
        user = users[0]

        if type(user["id"]) == int \
        and type(user ["name"]) == str:

            details = api.getUserDetails(user["id"])
            
            if type(details["id"]) == int:
                testResult = "OK"

    assert testResult == "OK"

def test_getControllerAuditHistory():
    
    testResult = "NOK"
    testMessage = "NOK"

    endTime = datetime.now()
    startTime = endTime - timedelta(days=1)

    result = api.getControllerAuditHistory(startTime=startTime, endTime=endTime)
    
    if  type(result) == list \
    and result[0]['timeStamp'] > 0:
        testResult = "OK"

    assert testResult == "OK"