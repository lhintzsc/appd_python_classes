import pytest
import pandas as pd
from appd.AppdApiWrapper import AppdApiWrapper
from appd.AppdRbacFunctions import AppdRbacFunctions
from datetime import datetime
from datetime import timedelta

api = AppdApiWrapper()
rbac = AppdRbacFunctions()

def test_iniUsers():

    testResult="NOK"
    testMessage="NOK"

    df = pd.DataFrame()
    df = rbac.iniUsers()

    rows = df.shape[0]
    columns = df.shape[1]

    if rows >= 1 \
    and columns == 1:
        testResult = "OK"

    assert testResult == "OK"

def test_iniDetails():
    
    testResult="NOK"
    testMessage="NOK"

    dfUsers = pd.DataFrame()
    dfDetails = pd.DataFrame()

    dfUsers = rbac.iniUsers()
    dfDetails = rbac.iniDetails()

    rows = dfDetails.shape[0]
    columns = dfDetails.shape[1]

    print("rows: "+str(rows))
    print("columns: "+str(columns))
    
    assert testResult == "OK"

def test_getTimeinterval():

    testResult="NOK"
    testMessage="OK"

    startTime= datetime(2021, 7, 4, 23, 30)
    endTime= datetime(2021, 7, 7, 23, 30)

    start0 = datetime(2021, 7, 4, 00, 00).replace(hour=00, minute=00, second=00)
    end0 = datetime(2021, 7, 4, 23, 59).replace(hour=23, minute=59, second=59)

    start1 = datetime(2021, 7, 5, 00, 00).replace(hour=00, minute=00, second=00)
    end1 = datetime(2021, 7, 5, 23, 59).replace(hour=23, minute=59, second=59)

    start2 = datetime(2021, 7, 6, 00, 00).replace(hour=00, minute=00, second=00)
    end2 = datetime(2021, 7, 6, 23, 59).replace(hour=23, minute=59, second=59)

    start3 = datetime(2021, 7, 7, 00, 00).replace(hour=00, minute=00, second=00)
    end3 = datetime(2021, 7, 7, 23, 59).replace(hour=23, minute=59, second=59)

    intervals = rbac.getTimeIntervals(startTime, endTime)

    if intervals[0]["startTime"] == start0 \
    and intervals[0]["endTime"] == end0 \
    and intervals[1]["startTime"] == start1 \
    and intervals[1]["endTime"] == end1 \
    and intervals[2]["startTime"] == start2 \
    and intervals[2]["endTime"] == end2 \
    and intervals[3]["startTime"] == start3 \
    and intervals[3]["endTime"] == end3:
        testResult = "OK"     
    
    assert testResult == "OK"

def test_getLastLogin():
    testResult="NOK"

    dfResult = pd.DataFrame()
    startTime= datetime.now() - timedelta(days=10)
    endTime= datetime.now() - timedelta(days=1)

    dfResult = rbac.getLastLogin(startTime, endTime)
    columns = dfResult.columns
    size=columns.size

    if size == 3 \
    and True not in dfResult.index.duplicated():
        testResult="OK"

    assert testResult == "OK"