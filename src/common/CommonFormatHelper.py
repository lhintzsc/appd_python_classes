import pprint 
import time
from datetime import datetime

class CommonTimeConverter:

    def String2Datetime(self, string, format="%Y-%m-%d %H:%M:%S"):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    
    def Datetime2Timestamp(self, datetime):
        return time.mktime(datetime.timetuple())

class CommonObjectPrinter:

    def show(self, p = None): 

        if p == None:
            return self.__dict__
        elif hasattr(self, str(p)): 
            return (getattr(self, p)) 


class CommonFormatHelper:

    def __init__(self):

        self.__dictPrinter = pprint.PrettyPrinter(indent=4)

    def print(self, ugly):

        print(type(ugly))

        if type(ugly) == dict:
            self.__dictPrinter.pprint(ugly)
        if type(ugly) == list:
            self.__dictPrinter.pprint(ugly)