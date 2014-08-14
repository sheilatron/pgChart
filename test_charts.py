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
        # testChartOptions = """
        # var options = {
          # title: 'Seven Mary Three - chart Options',
          # is3D: true,
        # };
        # """
        expectedResult = True #expected result for good data
        testCase['Seven'] = 7
        testCase['Mary'] = 1
        testCase['Three'] = 3
        self.assertTrue(pgChart(testCase) == None) #no parameters
        #self.assertTrue(pgChart(testCase, popupChart=False, chartFileName=testFileName) == None) # tests file-name only parameter
        #self.assertTrue(pgChart(testCase, chartOptions=testChartOptions, chartLabels=testLables ) == None) #test  options
        #self.assertTrue(pgChart(testCase, chartType='ColumnChart', chartLabels=testLables) == None) #test  Lables
        #self.assertTrue(pgChart(testCase, chartTitle=testChartTitle) == None) # test title 
        
    
   
if __name__ == '__main__':
    unittest.main()