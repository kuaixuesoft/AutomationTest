from xml.dom import minidom
import os
import shutil
import datetime
from TestWare import TestWare

class TestSuiteReporter(object):
    (SUCCEED, FAIL) = (1, 0)
    
    def __init__(self, lstSuiteResult, strSuiteResultPath):
        self.__lstSuiteResult = lstSuiteResult
        self.__strSuiteResultPath = strSuiteResultPath
        self.__strSuiteName = self.__lstSuiteResult[0]
        self.__iTotalCaseNum = 0
        self.__iCasePasses = 0
        self.__iCaseFails = 0
        self.__iTotalElapsedTime = self.__lstSuiteResult[2]
        self.__makeReport()
        self.__saveReport()

   
    def __makeReport(self):
        self.__doc = minidom.Document()
        strXSL = '"../../xsl/' + 'TestSuiteSummary.xsl"'
        self.__doc.appendChild(self.__doc.createProcessingInstruction \
                ('xml-stylesheet', 'type="text/xsl" href=' + strXSL))
        self.__addTestSuite(self.__doc)       
 
    
    def __addTestSuite(self, objParentNode):
        objTestSuite = self.__doc.createElement('testSuite')
        objParentNode.appendChild(objTestSuite)
        
        objSuiteName = self.__doc.createElement('suiteName')
        objSuiteName.appendChild(self.__doc.createTextNode(self.__strSuiteName))
        objTestSuite.appendChild(objSuiteName)
        
        objNumOfCases = self.__doc.createElement('numOfCases')
        objTestSuite.appendChild(objNumOfCases)
        
        objPasses = self.__doc.createElement('passes')
        objTestSuite.appendChild(objPasses)
        
        objFails = self.__doc.createElement('fails') 
        objTestSuite.appendChild(objFails)
        
        objTotalElapsedTime = self.__doc.createElement('totalElapsedTime')
        objTotalElapsedTime.appendChild(self.__doc.createTextNode(str(datetime.timedelta(seconds=self.__iTotalElapsedTime))))
        objTestSuite.appendChild(objTotalElapsedTime)
        
        for lstCaseResult in self.__lstSuiteResult[1]:
            self.__addTestResult(objTestSuite, lstCaseResult)
            
        objNumOfCases.appendChild(self.__doc.createTextNode(str(self.__iTotalCaseNum))) 
        objPasses.appendChild(self.__doc.createTextNode(str(self.__iCasePasses)))
        objFails.appendChild(self.__doc.createTextNode(str(self.__iCaseFails)))

            
    def __addTestResult(self, objParentNode, lstCaseResult):
        self.__iTotalCaseNum += 1
        
        objTestResult = self.__doc.createElement('testResult')
        objParentNode.appendChild(objTestResult)
        
        objCaseName = self.__doc.createElement('name')
        objCaseName.appendChild(self.__doc.createTextNode(lstCaseResult[0]))
        objTestResult.appendChild(objCaseName)
        
        objCaseResult = self.__doc.createElement('result')
        if lstCaseResult[1] == TestSuiteReporter.SUCCEED:
            self.__iCasePasses += 1
            objCaseResult.appendChild(self.__doc.createTextNode('passed'))
        else:
            self.__iCaseFails += 1
            objCaseResult.appendChild(self.__doc.createTextNode('failed'))
        objTestResult.appendChild(objCaseResult)
        
        objCaseElapsedTime = self.__doc.createElement('elapsedTime')
        objCaseElapsedTime.appendChild(self.__doc.createTextNode(str(datetime.timedelta(seconds=lstCaseResult[2]))))
        objTestResult.appendChild(objCaseElapsedTime)
        
        self.__addLog(objTestResult, lstCaseResult[0], lstCaseResult[3])
        
        hResultTxtFile = open(self.__strSuiteResultPath+os.sep+'..'+os.sep+'Result.txt', 'a')
        strResult = lstCaseResult[0]
        if lstCaseResult[1] == TestSuiteReporter.SUCCEED:
            strResult += ': pass'
        else:
            strResult += ': fail'
        hResultTxtFile.write(strResult+'\r\n')
        hResultTxtFile.close()
        
        
    def __addLog(self, objParentNode, strTestCaseName, strLogFolderPath):
        if len(strLogFolderPath) == 0:
            return
        
        objLog = self.__doc.createElement('log')
        
        lstLogFileFullName = os.listdir(strLogFolderPath)
        lstLogFileFullName.sort()
        for strLogFileFullName in lstLogFileFullName:
            strLogFileFullPath = strLogFolderPath + os.sep + strLogFileFullName 
            if os.path.isdir(strLogFileFullPath):
                continue
            else:
                self.__copyLogFile(strTestCaseName, strLogFileFullPath)
                self.__addFile(objLog, './'+strTestCaseName+'/'+strLogFileFullName)
        
        objParentNode.appendChild(objLog)
        
        
    def __copyLogFile(self, strTestCaseName, strSrcLogFileFullPath):
        if (os.access(self.__strSuiteResultPath, os.F_OK) != True):
            os.mkdir(self.__strSuiteResultPath)
        if (os.access(self.__strSuiteResultPath+os.sep+strTestCaseName, os.F_OK) != True):
            os.mkdir(self.__strSuiteResultPath+os.sep+strTestCaseName)
            
        strLogFileFullName = os.path.basename(strSrcLogFileFullPath)
        
        shutil.copyfile(strSrcLogFileFullPath, self.__strSuiteResultPath+os.sep+strTestCaseName+os.sep+strLogFileFullName)
         
        
    def __addFile(self, objParentNode, strLogFileRelativePath):
        objLogFile = self.__doc.createElement('file')
        
        objLogFileName = self.__doc.createElement('name')
        strLogFileName = os.path.basename(strLogFileRelativePath)
        objLogFileName.appendChild(self.__doc.createTextNode(strLogFileName))
        objLogFile.appendChild(objLogFileName)
        
        objLogFileUrl = self.__doc.createElement('url')
        objLogFileUrl.appendChild(self.__doc.createTextNode(strLogFileRelativePath))
        objLogFile.appendChild(objLogFileUrl)
        
        objParentNode.appendChild(objLogFile)


    def __saveReport(self):
        domcopy = self.__doc.cloneNode(True)
        if (os.access(self.__strSuiteResultPath, os.F_OK) != True):
            os.mkdir(self.__strSuiteResultPath)
        strXMLFilePath = self.__strSuiteResultPath + os.sep + self.__strSuiteName + '.xml'
        reportFile = open(strXMLFilePath, 'w+')
        domcopy.writexml(reportFile, addindent="", newl="")
        reportFile.close()

            
    def getCaseNum(self):
        return self.__iTotalCaseNum

    
    def getCasePassed(self):
        return self.__iCasePasses

    
    def getCaseFailed(self):
        return self.__iCaseFails

    
    def getSuiteInfo(self):
        return [self.__strSuiteName, './'+self.__strSuiteName+'/'+self.__strSuiteName+'.xml', self.__iTotalCaseNum, self.__iCasePasses, self.__iCaseFails, self.__iTotalElapsedTime]     