import pytest
import pandas as pd
from appd.AppdApiWrapper import AppdApiWrapper
from appd.AppdRbacFunctions import AppdRbacFunctions
from datetime import datetime
from datetime import timedelta

def test_createUserReport():
    rbac = AppdRbacFunctions()
    rbac.writeRbacExcel(days=90)
