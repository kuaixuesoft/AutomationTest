import logging
import os

class TestLogger(object):
    __logger = None
    __strLogFolderPath = ''
    __objLogHandler = None
    __strCaseLogPath = ''
    (DEBUG, INFO, WARNING, ERROR) = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR)
    
    def __init__(self, strLogFolderPath='', enmLogLevel=DEBUG):
        if TestLogger.__logger == None:
            TestLogger.__strLogFolderPath = strLogFolderPath
            self.__clearDir(TestLogger.__strLogFolderPath)
            logging.basicConfig(level=enmLogLevel,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        filename=self.__strLogFolderPath+os.sep+'AutoTestLog.txt',
                        filemode='w')
            console = logging.StreamHandler()
            TestLogger.__logger = logging.getLogger('case')
            TestLogger.__logger.addHandler(console)


    def __clearDir(self, top):
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

            
    def switchCaseLog(self, strSuiteName, strCaseName):
        if TestLogger.__objLogHandler != None:
            TestLogger.__logger.removeHandler(TestLogger.__objLogHandler)
        strFullSuiteLogPath = TestLogger.__strLogFolderPath + os.sep + strSuiteName
        strFullCaseLogPath = strFullSuiteLogPath + os.sep + strCaseName
        try:
            if (os.access(strFullSuiteLogPath, os.F_OK) != True):
                os.mkdir(strFullSuiteLogPath)
            if (os.access(strFullCaseLogPath, os.F_OK) != True):
                os.mkdir(strFullCaseLogPath)
        except:
            TestLogger.__strCaseLogPath = ''
            TestLogger.__objLogHandler = None
            return
        TestLogger.__strCaseLogPath = strFullCaseLogPath
        TestLogger.__objLogHandler = logging.FileHandler(TestLogger.__strLogFolderPath+os.sep+strSuiteName+os.sep+strCaseName+os.sep+'AutoTestLog.txt', 'w')
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        TestLogger.__objLogHandler.setFormatter(formatter)
        TestLogger.__logger.addHandler(TestLogger.__objLogHandler)

    def info(self, strLog):
        TestLogger.__logger.info(strLog)
    
    def debug(self, strLog):
        TestLogger.__logger.debug(strLog)
    
    def warning(self, strLog):
        TestLogger.__logger.warning(strLog)
    
    def error(self, strLog):
        TestLogger.__logger.error(strLog)
        
    def getCaseLogPath(self):
        return TestLogger.__strCaseLogPath

def test():
    logger = TestLogger('G:/', TestLogger.DEBUG)
    logger.switchCaseLog('AutoFramework', 'Test')
    logger.debug('This is a test log 1')

if __name__ == '__main__':
    test()