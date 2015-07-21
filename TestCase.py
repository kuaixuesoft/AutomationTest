from xml.dom import minidom
from CaseXMLParser import CaseXMLParser

class TestCase(object):
    def __init__(self, strSuiteName, strCasePath = ''):
        self.__strSuiteName = strSuiteName
        self.__strCasePath = strCasePath
        self.__strCaseName = ''
        self.__lstCaseSteps = []
        if len(self.__strCasePath) > 0:
            self.__parseCase()
        
    def __parseCase(self, strCasePath = ''):
        if len(strCasePath) > 0:
            self.__strCasePath = strCasePath
        objDoc = minidom.parse(self.__strCasePath)
        objCaseParser = CaseXMLParser(objDoc)
        self.__strCaseName = objCaseParser.strCaseName
        self.__lstCaseSteps = objCaseParser.lstSteps
        self.__lstIfFail = objCaseParser.lstIfFail
    
    def getTestCasePath(self):
        return self.__strCasePath
    
    def getTestCaseName(self):
        return self.__strCaseName
    
    def getTestSuiteName(self):
        return self.__strSuiteName
    
    def getTestCaseStepList(self):
        return self.__lstCaseSteps
    
    def getTestCaseFailList(self):
        return self.__lstIfFail
        
def test():
    pass

if __name__ == '__main__':
    test()