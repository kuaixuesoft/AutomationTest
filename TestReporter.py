from xml.dom import minidom
import os
import datetime
from TestSuiteReporter import TestSuiteReporter

class TestReporter(object):
    def __init__(self):
        self.__reportName = 'summary'
        self.__suiteNum = 0
        self.__strResultPath = ''
        self.__lstSummary = []
        self.__lstSummaryElement = ['testSuiteList', 'totalElapsedTime']
        self.__lstSuiteElement = ['name', 'url', 'numOfCases', 'passes', 'fails']

        
    def __clearDir(self, top):
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


    def makeReport(self, lstResult, strResultPath):
        self.__strResultPath = strResultPath
        self.__suiteNum = 0
        self.__clearDir(strResultPath)
        for lstSuite in lstResult:
            self.__suiteNum += 1
            testSuiteReport = TestSuiteReporter(lstSuite, strResultPath+os.sep+lstSuite[0])
            self.__lstSummary.append(testSuiteReport.getSuiteInfo())
        self.__makeSummaryReport()
        self.__fillSummaryReport()
        self.__saveSummaryReport()

    
    def __makeSummaryReport(self):
        self.__doc = minidom.Document() 
        strXSL='"../xsl/' + 'TotalSummary.xsl"'
        self.__doc.appendChild(self.__doc.createProcessingInstruction \
                ('xml-stylesheet',  'type="text/xsl" href=' + strXSL))
        self.__oSummary = self.__doc.createElement(self.__reportName)
        self.__doc.appendChild(self.__oSummary)
        for summary in self.__lstSummaryElement:
            object = self.__doc.createElement(summary)
            self.__oSummary.appendChild(object)

    
    def __fillSummaryReport(self):
        index = 0
        iTotalElapsedTime = 0
        for suiteInfo in self.__lstSummary:        
            self.__addTestSuiteElement(suiteInfo, index)      
            index += 1
            iTotalElapsedTime += suiteInfo[5]       
        self.__addElement("totalElapsedTime", self.__doc.createTextNode(str(datetime.timedelta(seconds=iTotalElapsedTime))))

              
    def __saveSummaryReport(self):
        domcopy = self.__doc.cloneNode(True)
        if (os.access(self.__strResultPath, os.F_OK) != True):
            os.mkdir(self.__strResultPath)
        reportFile = open(self.__strResultPath + os.sep + self.__reportName + '.xml', 'w+')
        domcopy.writexml(reportFile, addindent="    ", newl="\n")
        reportFile.close()

        
    def __addTestSuiteElement(self, lstSuiteInfo, index):   
        oTestSuite=self.__doc.createElement('testSuite')
        for strElement in self.__lstSuiteElement:
            element = self.__doc.createElement(strElement) 
            oTestSuite.appendChild(element) 
        self.__addElement('testSuiteList', oTestSuite) 
        self.__addElement('name', self.__doc.createTextNode(lstSuiteInfo[0]),index)
        self.__addElement('url', self.__doc.createTextNode(lstSuiteInfo[1]),index)
        self.__addElement('numOfCases', self.__doc.createTextNode(str(lstSuiteInfo[2])),index)
        self.__addElement('passes', self.__doc.createTextNode(str(lstSuiteInfo[3])),index)
        self.__addElement('fails', self.__doc.createTextNode(str(lstSuiteInfo[4])),index)

        
    def __addElement(self, strAddingElement, oAddedElement, index = 0):
        oAddingElement = self.__doc.getElementsByTagName(strAddingElement)[index]
        oAddingElement.appendChild(oAddedElement)