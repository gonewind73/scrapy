'''
Created on 2016年5月11日

@author: heguofeng

DomainHunter
1\find domain
2\test is https
3\if https get certificate,check issuer and validate
4\if not https get whois,get contact email & telephone
5\write in database

'''
import unittest

class DomainHunter(object):
    def __init__(self):
        pass
    

class Domain(object):    
    def __init__(self):
        self.domainName=''
        self.hasCertificate=False
        self.certficate=""
        self.contact=""
        
class Contact(object):    
    def __init__(self):
        self.name=""
        self.telephone=""
        self.email=""
        pass

    
    
    
    

    

class https(object):
    
    def __init__(self):
        pass
    
    def isHttps(self):
        return True

class Test(unittest.TestCase):


    def setUp(self):
        self.hs=https()
        pass


    def tearDown(self):
        pass


    def testHttps(self):
        print("test1")
        self.assertTrue(self.hs.isHttps(),"test failure")
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()