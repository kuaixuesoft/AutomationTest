import os
from TestCase import TestCase

class TestSuite(object):
    def __init__(self, strSuiteName, strSuitePath):
        self.__strSuiteName = strSuiteName
        self.__strSuitePath = strSuitePath
        self.__lstCaseList = []
        self.__getSuiteTestCases('')

           
    def __getSuiteTestCases(self, strRelativePath):
        lstFileFullName = os.listdir(self.__strSuitePath + os.sep + strRelativePath)
        lstFileFullName.sort()
        for strFileFullName in lstFileFullName:
            if len(strRelativePath) != 0:
                strFileFullPath = self.__strSuitePath + os.sep + strRelativePath \
                          + os.sep + strFileFullName
            else:
                strFileFullPath = self.__strSuitePath + os.sep + strFileFullName
            
            if os.path.isdir(strFileFullPath):
                strFurtherPath = strRelativePath + os.sep + strFileFullName
                self.__getSuiteTestCases(strFurtherPath)
            else:
                strFileName, strFileExt = os.path.splitext(strFileFullName)
                if strFileExt == '.xml':
                    self.__lstCaseList.append(TestCase(self.__strSuiteName, strFileFullPath))

                
    def getTestSuiteName(self):
        return self.__strSuiteName

    
    def getTestSuitePath(self):
        return self.__strSuitePath
      
                    
    def getTestCaseList(self):
        return self.__lstCaseList

 
def test():
    pass

if __name__ == '__main__':
    test()
