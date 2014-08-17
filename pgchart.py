"""
NapalmHorn Code

pgChart is an ultralightweight easy to use solution to creating charts in
python it use Google's Chart API Thus it creates good looking reasonable charts
in a fast and easy way.  basiclly I wanted a fast easy lightweight(no big
packages, dependences of complex api's) way to Take a log file count some stuff
and make a chart.
"""

import os.path
import webbrowser
import string
import copy

PIE_CHART = 'PieChart'
COLUMN_CHART = 'ColumnChart'


class GoogleChart(object):
    """
    TODO
    """

    default_type = PIE_CHART
    default_title = "My Chart"

    def __init__(self, data, title=None, labels=None):
        if title:
            self.title = title
        else:
            self.title = self.default_title

    def valid_html(self, chart_type=None):
        """
        Return True if html passes validation.
        """
        # TODO
        if not chart_type:
            chart_type = self.default_type

    def create_file(self, chart_type=None):
        # TODO

    def render_html(self, chart_type=None):
        """
        Return the rendered html for the data and the specified chart type.
        """
        # TODO
        
    


def pg1VarTable(chartableDict):
    """ Inputs the chartableDict from pgChart and creates a html table for use 
    in the HTML file for use with single data point per label
    """
    htmlDataChart = ''
    for datum in chartableDict.keys():
        # add a label and data row to the htmlDataChart
        if htmlDataChart:
            htmlDataChart +=',' # if its not blank put a comma at the end, saves unneeded trailing comma         
        if datum.find("'") + 1 : # fix raw ' in labels find returns -1 if not found so +1 evals to zero => False
            fixed_datum = datum
            fixed_datum = fixed_datum.replace("'","feet")
            htmlDataChart += "\n          ['" + fixed_datum  + "',   " + str(chartableDict[datum]) + '  ]' 
        else: 
            htmlDataChart += "\n          ['" + str(datum) + "',   " + str(chartableDict[datum]) + '  ]' 
    htmlDataChart += '\n        ]);\n'    #close char
    return htmlDataChart

def pgXVarTable(chartableDict):
    """ Inputs the chartableDict from pgChart and creates a html table for use 
    in the HTML file for use with multiple data points per label
    """
    htmlDataChart = ''
    for data in chartableDict.keys():
        # add a label and data row to the htmlDataChart
        if htmlDataChart:
            htmlDataChart +=',' # if the chart is not blank put a comma at the end, saves unneeded trailing comma         
        if str(data).find("'") + 1 : # fix raw ' in labels find returns -1 if not found so +1 evals to zero => False
            fixed_datum = data
            fixed_datum = fixed_datum.replace("'","feet") #raw ' causes issues 
            htmlDataChart += "'" + fixed_datum  + "'"  # add data one at a time to the line
        else: 
            htmlDataChart += "\n          ['" + str(data) + "'" #for each data entry create a new line.
        for datum in chartableDict[data]:
            htmlDataChart += ",   " + str(datum) + " " # add data one at a time to the line        
        htmlDataChart +=  '  ]' # close the line
    htmlDataChart += '\n        ]);\n'    #close chart    
    return htmlDataChart
    

def pgChart(chartableDict, popupChart=None, chartType='PieChart', returnhtml=None,
           chartOptions=None , chartFileName=None, chartTitle=None, chartLabels=[]):
    """Takes a dictionary with the subset of data that we want and makes a chart.
    
    Args: 
        chartableDict(dict): a mapping containg the following keys:
                "chartTitle" => the title of the new chart, also the basis for the title of chart object
                    if absent or blank title will be 'chart title'
                "chartOptions" => the options to be sent to google charts as a list of strings like: ["is3D: true"], 
                    if absent or blank defaults will be used
        'popupChart' => if present indicates chart should open automatically
        'returnhtml' => returns a string of html instead of /(or addition to) saving to file.
        'chartFileName' => the filename to save the chart as if absent and not returnhtml save to lowest chart name
        'chartType' => type of chart to create, currently supports 'PieChart' , 'ColumnChart'
        'chartLabels' => a list strings that label the columns of data.

    Output: a file named whatever the chartableDict['control chart title'] + '.html',
        or, if absent or blank, chart\d+.html w/ \d+ as lowest possible choice starting at zero        

    TO DO:
    Split off each chart type to its own function called by this function so my code is more modular.
    add an option returnhtml to return a string of HTML  such that putting many charts in 1 html file is easier
    allow for as many different chart types as the google chart api has with good defaults.
    """ 
    htmlPriorToChart = """<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          """
          
    htmlFollowingChart_Pie = """
        var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="piechart_3d" style="width: 900px; height: 500px;"></div>
  </body>
</html>
    """
    controlChartTitle = ''# title of chart
    controlChartFilename = ''
    controlChartLables = copy.deepcopy(chartLabels) # keeps the list from breaking on multiple function calls with the same array of labels
    controlChartOptions = '' # the options properly formatted to be loaded into the HTML file
    htmlDataChart = '' # the working string of html of chart data 
    #handle options
    
    varType = type(chartableDict[chartableDict.keys()[0]])
    if  varType == type(list()) :
        chartDim = len(chartableDict[chartableDict.keys()[0]])
    elif varType == type(1) or varType == type('1'):
        chartDim = 1
    else:
        print 'Unexpected data type', type(chartableDict[chartableDict.keys()[0]])
    # figure out a way to calculate this at runtime
    if chartFileName:
        controlChartFilename = chartFileName
    else:
         chartNumber = 1
         while chartNumber : #use the next chart[\d]+.html that is open
            if not os.path.isfile('chart' + str(chartNumber - 1) + '.html' ):
                controlChartFilename = 'chart' + str(chartNumber - 1) + '.html'
                chartNumber = 0
            else:
                chartNumber += 1
    if chartTitle: #is there is a chart title use it
        controlChartTitle = chartTitle
        #this covers the most common cases that will break javascript/HTML but I should simplify with RE
        chartTitleTag = string.replace(controlChartTitle,' ','_')#remove spaces
        chartTitleTag = string.replace(chartTitleTag,'\t','_')#remove tabs
        chartTitleTag = string.replace(chartTitleTag,'.','_')#remove dot
        chartTitleTag = string.replace(chartTitleTag,',','_')#remove comma
        chartTitleTag = string.replace(chartTitleTag,'"','_')#remove quote
        chartTitleTag = string.replace(chartTitleTag,"'",'_')#remove 2x quote
        chartTitleTag = string.replace(chartTitleTag,"-",'_')#remove dash
        chartTitleTag = string.replace(chartTitleTag,"?",'_')#remove '?'
        chartTitleTag = string.replace(chartTitleTag,"!",'_')#remove '!'
        chartTitleTag = string.replace(chartTitleTag,"`",'_')#remove `
        chartTitleTag = string.replace(chartTitleTag,"~",'_')#remove ~
        htmlFollowingChart_Pie = string.replace(htmlFollowingChart_Pie,'piechart_3d',chartTitleTag)
        if not chartOptions:
            # insert the title if it is passed separately 
            controlChartOptions = "        var options = {\n          title: '" + chartTitle + "'\n        };\n"+ controlChartOptions 
    elif chartFileName: # otherwise use the file-name
        controlChartTitle = chartFileName
    else:
        controlChartTitle = 'Unnammed Chart'
    if chartOptions:
        controlChartOptions = "        var options = {\n"
        titleSet = False
        for optionStr in chartOptions:
            if  "title:" in optionStr:
                if chartTitle:
                    print "dual title definition" 
                titleSet = True
            controlChartOptions += '          ' + optionStr + ',\n'
            # need to fix this
            #controlChartOptions = "title: '" + chartTitle + "'\n"+ controlChartOptions # add the title if it is passed separately 
        if (not titleSet) and controlChartTitle:
            controlChartOptions += "          title: '" + str(controlChartTitle) + "'\n" #sets title if there are options other than title 
        controlChartOptions += "        };\n"
    elif not controlChartOptions:
        controlChartOptions = "        var options = {\n        };\n" #creates a blank option block
    #handle different types of charts.
    if chartType == 'PieChart':
        htmlFollowingChart = htmlFollowingChart_Pie # no additional actions required as this default
    elif chartType == 'ColumnChart':
        #similar to pie chart just with different tag
        htmlFollowingChart = string.replace(htmlFollowingChart_Pie , 'PieChart','ColumnChart')
    if not controlChartLables: #create default labels if none passed
        workingLabel = "['Label'"
        lablesNeeded = chartDim
        while lablesNeeded > 0:
            workingLabel +=", 'Data" + str(lablesNeeded) + "'"
            lablesNeeded -= 1
        workingLabel +="],"
        htmlPriorToChart += workingLabel
    else: # use existing labels
        workingLabel ="['"+controlChartLables.pop(0)+"'"
        for l in controlChartLables:
            workingLabel +=", '" + l + "'"
        workingLabel +="],"
        htmlPriorToChart += workingLabel
    # Next we create the chart in HTML
    if chartDim == 1: 
        htmlDataChart = pg1VarTable(chartableDict) # single entry data
    else:
        htmlDataChart = pgXVarTable(chartableDict) # Data in lists 
    # write all 4 parts of HTML to the file.
    f = open( controlChartFilename ,'w')
    f.write(htmlPriorToChart)
    f.write(htmlDataChart)
    f.write(controlChartOptions)
    f.write(htmlFollowingChart)
    f.close()
    if popupChart:
        webbrowser.open_new_tab(controlChartFilename) # call web browser to open html file.
    return None


