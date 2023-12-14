###############################################################################################
# Over view on test directory files:
# 1. AbstractParserTest/AbstractParserTest -  has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 2. JsonParserTest/JsonParserTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 3. XMLParserTest/XMLParserTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 4. CSVParserTest./CSVParserTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 5. DataManagerFactoryTest/DataManagerFactoryTest - has setUpCls, setUp, test method(s),  tearDown, tearDownCls
# 6. test_entity/TestEntity
# 7. test_entity/TestEntityCollection
# 8. my_suite() - Suite that co-ordinates all the test
#############################################################################################

import sys
sys.path.append(r'.\main')
sys.path.append(r'.\main\data_transformer')
sys.path.append(r'.\main\data_processor')

import unittest
from Test.AbstractParserTest import AbstractParserTest
from Test.JsonParserTest import JsonParserTest
from Test.XmlParserTest import XMLParserTest
from Test.CSVParserTest import CSVParserTest
from Test.DataManagerfactoryTest import DataManagerFactoryTest
from Test.test_entity import TestEntity
from Test.test_entity import TestEntityCollection
from Test.test_configuration import TestConfig

def my_suite():
    """
    Test Suite
    """
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    suite.addTest(unittest.makeSuite(AbstractParserTest))
    suite.addTest(unittest.makeSuite(JsonParserTest))
    suite.addTest(unittest.makeSuite(XMLParserTest))
    suite.addTest(unittest.makeSuite(CSVParserTest))
    suite.addTest(unittest.makeSuite(DataManagerFactoryTest))
    suite.addTest(unittest.makeSuite(TestEntity))
    suite.addTest(unittest.makeSuite(TestEntityCollection))
    suite.addTest(unittest.makeSuite(TestConfig))
    print(runner.run(suite))

if __name__ == '__main__':
    my_suite()




