import pandas as pd
import abc
import os
from timeit import default_timer as timer
import datetime
import pickle

class QuickObjectLoader(object):

    __metaclass__ = abc.ABCMeta   

    def __init__(self):
        self.__refreshTime = False
        self.__timeSpan = datetime.timedelta(hours=0)      

    def _refresh(self, fileName, refreshMethod, methodArgs):
        data = refreshMethod(**methodArgs)
        self._storeSource(data, fileName)
        return data

    def _timeToRefresh(self, fileName):
        if self.__refreshTime == False:
            return False
        else:
            timeStamp = os.path.getmtime(fileName)
            curTime = datetime.datetime.now()
            modTime = datetime.datetime.fromtimestamp(timeStamp)
            if (curTime-modTime) < self.__timeSpan:
                return False
            else:
                return True

    def _existingCacheFile(self,fileName):
        if os.path.exists(fileName):
            return True
        else:
            return False

    @abc.abstractmethod 
    def _readSource(self,fileName):
        pass

    @abc.abstractmethod  
    def _storeSource(self, data, fileName):
        pass      

    def load(self, fileName, refreshMethod, methodArgs):
        if not os.path.exists(os.path.dirname(fileName)):
            os.makedirs(os.path.dirname(fileName))
        if self._existingCacheFile(fileName)\
        and not self._timeToRefresh(fileName):
            return self._readSource(fileName)                        
        else:
            return self._refresh(fileName, refreshMethod, methodArgs)

    def deleteCache(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)
        return

    
    def unsetRefreshTime(self):
        self.__refreshTime = False

    def setRefreshTime(self, hours):
        self.__refreshTime = True
        self.__timeSpan = datetime.timedelta(hours=hours)      

class QuickObjectLoaderPickle(QuickObjectLoader):

    def __init__(self):
        super(QuickObjectLoaderPickle, self).__init__()
    
    def _readSource(self,fileName):
        with open(fileName, 'rb') as f:
            data = pickle.load(f)
        return data
             
    def _storeSource(self, data, fileName):
        with open(fileName, 'wb') as f:
            pickle.dump(data, f)
        return

def returnList():
    listVal = [1,2,3,4,5,61,2,3,4,5,61,2,3,4,5,61,2,3,4,5,61,2,3,4,5,61,2,3,4,5,61,2,3,4,5,61,2,3,4,5,6]
    return listVal

if __name__ == '__main__':
    #df = None
    #ol = QuickDataFrameLoaderPickle()
    #ol.setRefreshTime(3)
    
    #el = QuickDataFrameLoaderExcel()
    #el.setRefreshTime(3)

    ol = QuickObjectLoaderPickle()
    
    picklePath = ".//cache//pickle//"
    excelPath = ".//cache//excel//"

    start = timer()
    print(ol.load(picklePath+"testList.pkl", returnList, {} ))
    #df = el.load(excelPath+"TestFrame.xlsx", df.copy, {} )
#    
    end = timer()
    print(end-start)
#    #print(ol.getFileName())
