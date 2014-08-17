import unittest
import os.path

from pgchart import * 


class IdealApi(unit.TestCase):
    """
    Think about what would be the most useful, testable
    API, resulting in the most readable code.
    """
    def setUp(self):
        from pgchart import GoogleChart 
        self.chart_data = dict(Seven=7, Mary= 1, Three=3)
        self.testFileName = 'sevenmarythree.html'
        self.testChartTitle = 'Seven Mary & Three'
        # Google's chart API requires a list of strings that have
        # a special structure, like so:
        self.testChartOptions = ["title: 'Seven Mary Three - chart Options'",
                            "is3D: true"]
        self.testLables = ['Name' ,'Sickdays']
        self.chart = GoogleChart(data, title=self.testChartTitle, labels=self.testLables)

    def test_data_is_valid_for_type(self):
        
        
    def test_valid_html(self):
        assert self.chart.is_valid_html()

    def test_create_file(self):
        create_file = self.chart.create_file(self.testFileName)
        assert os.path.isfile(create_file)

    def test_popup(self):
        pass

    def test_expected_content_for_piechart(self):
        from pgchart import PIE_CHART
        content = self.chart.render_html(PIE_CHART)
        assert self.testChartTitle in content


class charttestcases(unittest.TestCase):

    def setUp(self):
        self.chart_data = dict(Seven=7, Mary= 1, Three=3)
        self.testFileName = 'sevenmarythree.html'
        self.testChartTitle = 'Seven Mary & Three'
        # Google's chart API requires a list of strings that have
        # a special structure, like so:
        self.testChartOptions = ["title: 'Seven Mary Three - chart Options'",
                            "is3D: true"]
        self.testLables = ['Name' ,'Sickdays']
        
        self.testLable2 = ['Name' ,'Total Items', 'Desserts']
        self.chart_data2 = dict()
        self.chart_data2['Jake'] = [5, 1]
        self.chart_data2['Mary'] = [3, 1]
        self.chart_data2['Tracy'] = [5, 0]

    def test_pie_chart_no_params(self):
        """Does the test case return true when expected"""
        # This test case exercises no params
        self.assertTrue(pgChart(self.chart_data) == None)

    def test_pie_chart_filename_only_param(self):
        # tests file-name only parameter
        self.assertTrue(pgChart(self.chart_data, popupChart=False,
                        chartFileName=self.testFileName) == None) 
        self.assertTrue(pgChart(self.chart_data, popupChart=False,
                                chartOptions=self.testChartOptions,
                                chartLabels=self.testLables ) == None) #test  options
        #test  Lables
        self.assertTrue(pgChart(self.chart_data, popupChart=False,
                       chartType='ColumnChart', chartLabels=self.testLables) == None) 
        self.assertTrue(pgChart(self.chart_data, popupChart=False,
                                chartTitle=self.testChartTitle) == None) # test title 
    
    def test_col_chart(self):
        """Does the test case return true when expected"""
        expectedResult = True #expected result for good data
        popupChartsNow = True
        self.assertTrue(pgChart(self.chart_data,popupChart=popupChartsNow, chartType='ColumnChart', chartLabels=self.testLables) == None) #test  Lables  
        self.assertTrue(pgChart(self.chart_data2,popupChart=popupChartsNow, chartType='ColumnChart', chartLabels=self.testLable2) == None) #test  Lables  
    
   
if __name__ == '__main__':
    unittest.main()
