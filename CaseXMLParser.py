from xml.dom import minidom, Node
import re

class CaseXMLParser(object):
    def __init__(self, doc):
        self.__tab = '    '
        self.strCaseName = ''
        self.lstSteps = []
        self.lstIfFail = []
        for child in doc.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and \
               child.tagName == 'case':
                self.__handleCase(child)
                
    def __getText(self, nodelist):
        retlist = []
        for node in nodelist:
            if node.nodeType == Node.TEXT_NODE:
                retlist.append(node.wholeText)
        return re.sub('\s+', ' ', ''.join(retlist)).strip()
                
    def __handleCase(self, node):
        for child in node.childNodes:
            if child.nodeType != Node.ELEMENT_NODE:
                continue
            if child.tagName == 'name':
                self.strCaseName = self.__getText(child.childNodes)
            if child.tagName == 'step':
                self.lstSteps.append(self.__handleStep(child))
            if child.tagName == 'ifFail':
                self.lstIfFail = self.__handleIfFail(child)
    
    def __handleStep(self, node):
        lstFunc = []
        for child in node.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and \
               child.tagName == 'function':
                lstFunc.append(self.__handleFunction(child))
        return lstFunc
                
    def __handleFunction(self, node):
        strFuncName = ''
        lstFuncPara = []
        for child in node.childNodes:
            if child.nodeType != Node.ELEMENT_NODE:
                continue
            if child.tagName == 'name':
                strFuncName = self.__getText(child.childNodes)
            if child.tagName == 'para':
                lstFuncPara.append(self.__getText(child.childNodes))
        return [strFuncName, lstFuncPara]
    
    def __handleIfFail(self, node):
        lstFunc = []
        for child in node.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and \
               child.tagName == 'function':
                lstFunc.append(self.__handleFunction(child))
        return lstFunc
        
    def printCase(self):
        print 'Case:'
        print self.__tab + 'Name: %s' % self.strCaseName
        for index in range(0, len(self.lstSteps)):
            print self.__tab + 'Step %d:' % index
            self.__printFuncList(self.lstSteps[index], 2)
        print self.__tab + 'IfFail:'
        self.__printFuncList(self.lstIfFail, 2)
        
    def __printFuncList(self, funclist, indent):
        for index in range(0, len(funclist)):
            print self.__tab*indent + 'Function %d:' % index
            self.__printFunc(funclist[index], indent+1)
                   
    def __printFunc(self, func, indent):
        print self.__tab*(indent) + 'Name: %s' % func[0]
        self.__printParaList(func[1], indent)
            
    def __printParaList(self, paralist, indent):
        for index in range(0, len(paralist)):
            print self.__tab*indent + 'Parameter %d: %s' % (index, paralist[index])

def test():                
    doc = minidom.parse('../TestWare/TestSuiteList/TestFramework/TestFramework.xml')
    parser = CaseXMLParser(doc)
    print parser.printCase()
    
if __name__ == '__main__':
    test()