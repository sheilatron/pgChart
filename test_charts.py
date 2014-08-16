import unittest
from pgchart import * 


class charttestcases(unittest.TestCase):

    def test_pie_chart(self):
        """Does the test case return true when expected"""
        testCase = dict()
        testFileName = 'sevenmarythree.html'
        testChartTitle = 'Seven Mary & Three'
        testChartOptions = ["title: 'Seven Mary Three - chart Options'" , "is3D: true"]
        testLables = ['Name' ,'Sickdays']
        expectedResult = True #expected result for good data
        testCase['Seven'] = 7
        testCase['Mary'] = 1
        testCase['Three'] = 3
        self.assertTrue(pgChart(testCase) == None) #no parameters
        self.assertTrue(pgChart(testCase, popupChart=False, chartFileName=testFileName) == None) # tests file-name only parameter
        self.assertTrue(pgChart(testCase, popupChart=False, chartOptions=testChartOptions, chartLabels=testLables ) == None) #test  options
        self.assertTrue(pgChart(testCase,popupChart=False, chartType='ColumnChart', chartLabels=testLables) == None) #test  Lables
        self.assertTrue(pgChart(testCase, popupChart=False, chartTitle=testChartTitle) == None) # test title 
    
    def test_col_chart(self):
        """Does the test case return true when expected"""
        testCase = dict()
        testFileName = 'sevenmarythree.html'
        testChartTitle = 'Lunch Box Counts'
        testChartOptions = ["title: 'Lunch Box Counts - chart Options'" , 'legend: { position: "none" }']
        testLables = ['Name' ,'Total Items']
        expectedResult = True #expected result for good data
        popupChartsNow = True
        testCase['Jake'] = 5
        testCase['Mary'] = 3
        testCase['Tracy'] = 5
        self.assertTrue(pgChart(testCase,popupChart=popupChartsNow, chartType='ColumnChart', chartLabels=testLables) == None) #test  Lables  
        testLable2 = ['Name' ,'Total Items', 'Desserts']
        testCase2 = dict()
        testCase2['Jake'] = [5, 1]
        testCase2['Mary'] = [3, 1]
        testCase2['Tracy'] = [5, 0]
        self.assertTrue(pgChart(testCase2,popupChart=popupChartsNow, chartType='ColumnChart', chartLabels=testLable2) == None) #test  Lables  
    
   
if __name__ == '__main__':
    unittest.main()