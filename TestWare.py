import os
import sys
import re
from ConfigParser import ConfigParser
from TestSuite import TestSuite
from TestLogger import TestLogger

class TestWare(object):
    def __init__(self, strConfFilePath):
        self.__strConfFilePath = strConfFilePath
        self.__lstTestSuiteList = []
        self.__strLibPath = ''
        self.__strTestSuiteListPath = ''
        self.__strTestResultPath = ''
        self.__dicLibFuncDict = {}
        self.__strLogFolderPath = ''
        self.__getConfig()
        TestLogger(self.__strLogFolderPath)
        self.__loadAllLibs('')
        self.__loadAllCases()
        
    def __getConfig(self):
        cfg = ConfigParser()
        cfg.read(self.__strConfFilePath)
        dicConfig = {}
        for strOption in cfg.options('TestWare'):
            dicConfig[strOption] = cfg.get('TestWare', strOption).strip()  
        self.__strLibPath = dicConfig['libpath']
        self.__strTestSuiteListPath = dicConfig['testsuitelistpath']
        self.__strTestResultPath = dicConfig['testresultpath']
        self.__strLogFolderPath = dicConfig['logfolderpath']
    
    def __loadAllLibs(self, strRelativePath):
        sys.path.insert(0, self.__strLibPath + strRelativePath)
        lstFileFullName = os.listdir(self.__strLibPath + os.sep + strRelativePath)
        lstFileFullName.sort()
        for strFileFullName in lstFileFullName:
            if len(strRelativePath) != 0:
                strFileFullPath = self.__strLibPath + os.sep + strRelativePath \
                          + os.sep + strFileFullName
            else:
                strFileFullPath = self.__strLibPath + os.sep + strFileFullName
            if os.path.isdir(strFileFullPath):
                strFurtherPath = strRelativePath + os.sep + strFileFullName
                self.__loadAllLibs(strFurtherPath)
            else:
                strFileName, strFileExt = os.path.splitext(strFileFullName)
                if strFileExt == '.py':
                    self.__loadFromFile(strFileFullPath)
                    
    def __loadFromFile(self, strFileFullPath):
        strModName = os.path.splitext(os.path.basename(strFileFullPath))[0]
        objMod = __import__(strModName)
        lstFuncNameList = []
        for strAttrName in dir(objMod):
            if strAttrName[0:2] != '__':
                lstFuncNameList.append(strAttrName)
        for strFuncName in lstFuncNameList:
            self.__dicLibFuncDict[strFuncName] = getattr(objMod, strFuncName)
    
    def __loadAllCases(self):
        lstFileFullName = os.listdir(self.__strTestSuiteListPath)
        lstFileFullName.sort()
        for strFileFullName in lstFileFullName:
            strFileFullPath = self.__strTestSuiteListPath + os.sep + strFileFullName
            if os.path.isdir(strFileFullPath):
                self.__lstTestSuiteList.append(TestSuite(strFileFullName, strFileFullPath))
                
    def getTestSuiteList(self):
        return self.__lstTestSuiteList
    
    def getLibPath(self):
        return self.__strLibPath
    
    def getTestSuiteListPath(self):
        return self.__strTestSuiteListPath
    
    def getTestResultPath(self):
        return self.__strTestResultPath
    
    def getLibFuncDict(self):
        return self.__dicLibFuncDict
    
    def getLogFolderPath(self):
        return self.__strLogFolderPath
    
def test():
    testware = TestWare('Config.ini')
    globals().update(testware.getLibFuncDict())
    print globals()

if __name__ == '__main__':
    test()