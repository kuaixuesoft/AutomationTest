import datetime
import os
import traceback
from TestWare import TestWare
from TestLogger import TestLogger

class TestExecutor(object):
    (SUCCEED, FAIL) = (1, 0)
    def __init__(self, objTestWare):
        self.__objTestWare = objTestWare
        dicGlobVar = {}
        dicGlobVar['GlobTestLogger'] = TestLogger()
        globals().update(dicGlobVar)
        globals().update(self.__objTestWare.getLibFuncDict())
        self.__lstTestSuiteResultList = []


    def __runTestWare(self):
        GlobTestLogger.debug("Run Test Ware")
        lstTestSuiteList = self.__objTestWare.getTestSuiteList()
        for objTestSuite in lstTestSuiteList:
            self.__lstTestSuiteResultList.append(self.__runTestSuite(objTestSuite))

            
    def __runTestSuite(self, objTestSuite):
        lstTestCaseResultList = []
        strTestSuiteName = objTestSuite.getTestSuiteName()
        GlobTestLogger.debug("Run Suite: " + strTestSuiteName)
        lstTestCaseList = objTestSuite.getTestCaseList()
        starttime = datetime.datetime.now()
        for objTestCase in lstTestCaseList:
            lstTestCaseResultList.append(self.__runTestCase(objTestCase))
        endtime = datetime.datetime.now()
        return [strTestSuiteName, lstTestCaseResultList, (endtime-starttime).seconds]

            
    def __runTestCase(self, objTestCase):
        strTestSuiteName = objTestCase.getTestSuiteName()
        strTestCaseName = objTestCase.getTestCaseName()
        strTestCaseLogPath = self.__objTestWare.getLogFolderPath() + os.sep + strTestSuiteName + os.sep + strTestCaseName
        GlobTestLogger.switchCaseLog(strTestSuiteName, strTestCaseName)
        GlobTestLogger.debug("Run Test Case: " + strTestCaseName)
        lstTestStepList = objTestCase.getTestCaseStepList()
        starttime = datetime.datetime.now()
        for step in lstTestStepList:
            result = self.__runTestStep(step)
            if result == TestExecutor.FAIL:
                endtime = datetime.datetime.now()
                self.__runIfFail(objTestCase.getTestCaseFailList())
                return [strTestCaseName, TestExecutor.FAIL, (endtime-starttime).seconds, GlobTestLogger.getCaseLogPath()]
        endtime = datetime.datetime.now()
        return [strTestCaseName, TestExecutor.SUCCEED, (endtime-starttime).seconds, GlobTestLogger.getCaseLogPath()]

            
    def __runTestStep(self, step):    
        strFuncCall = ''
        for lstFun in step:
            strFuncCall = "result = " + lstFun[0] + "("
            lstParameter = lstFun[1]
            if len(lstParameter) > 0:
                strFuncCall += lstParameter[0] 
                for strParameter in lstParameter[1:]:
                    strFuncCall += ', ' + strParameter 
            strFuncCall += ')'
            GlobTestLogger.debug("Call: " + strFuncCall)
            try:
                exec strFuncCall in globals()
            except:
                GlobTestLogger.debug("*** Exceptioin: ***")
                GlobTestLogger.debug(traceback.format_exc())
                return TestExecutor.FAIL
            if result[0] == TestExecutor.FAIL:
                return TestExecutor.FAIL
        return TestExecutor.SUCCEED

    
    def __runIfFail(self, lstIfFailList):
        if len(lstIfFailList) == 0:
            try:
                DefaultCollectLog()
            except:
                GlobTestLogger.debug("*** Exceptioin: ***")
                GlobTestLogger.debug(traceback.format_exc())
        else:
            strFuncCall = ''
            for lstFun in lstIfFailList:
                strFuncCall = lstFun[0] + "("
                lstParameter = lstFun[1]
                if len(lstParameter) > 0:
                    strFuncCall += lstParameter[0] 
                    for strParameter in lstParameter[1:]:
                        strFuncCall += ', ' + strParameter 
                strFuncCall += ')'
                GlobTestLogger.debug("Call: " + strFuncCall)
                try:
                    exec strFuncCall in globals()
                except:
                    GlobTestLogger.debug("*** Exceptioin: ***")
                    GlobTestLogger.debug(traceback.format_exc())

    
    def execute(self):
        self.__runTestWare()

    
    def getTestResult(self):
        return self.__lstTestSuiteResultList


def printTestResult(lstTestResult):
    for suiteResult in lstTestResult:
        print 'Suite Name: %s' % suiteResult[0]
        print 'Suite Elapse Time: %d' % suiteResult[2]
        for caseResult in suiteResult[1]:
            print 'Case Name: %s' % caseResult[0]
            print 'Case Result: %d' % caseResult[1]
            print 'Case Elapse Time: %d' % caseResult[2]
            print 'Case Log Path: %s' % caseResult[3]


def test():
    testware = TestWare('Config.ini')
    executor = TestExecutor(testware) 
    executor.execute()    
    lstTestResult = executor.getTestResult()
    printTestResult(lstTestResult)


if __name__ == '__main__':
    test()