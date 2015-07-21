from TestWare import TestWare
from TestExecutor import TestExecutor
from TestReporter import TestReporter
from TestLogger import TestLogger

testware = TestWare('Config.ini')
executor = TestExecutor(testware)
executor.execute()        
reportor = TestReporter()
reportor.makeReport(executor.getTestResult(), testware.getTestResultPath())