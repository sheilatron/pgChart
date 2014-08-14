#NapalmHorn Code
#pgChart is an ultralightweight easy to use solution to creating charts in python
#it use Google's Chart API 
#Thus it creates good looking reasonable charts in a fast and easy way.
#basiclly I wanted a fast easy lightweight(no big packages, dependences of complex api's) way to 
#Take a log file count some stuff and make a chart.
import os.path
import webbrowser
import string

def pgChart(chartableDict , popupChart=None, chartType='PieChart' , returnhtml=None , chartOptions=None , chartFileName=None, chartTitle=None, chartLabels=None):
    """Takes a dictionary with the subset of data that we want and makes a chart 
    Input : chartableDict 
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
    use http://www.pythoncentral.io/fun-with-python-function-parameters/ to remove silly dict entries for chart control.
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
        #this covers the most common cases that will break js/HTML but I should simplify with RE
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
    if not chartLabels: #create default labels if none passed
        workingLabel = "['Label'"
        while chartDim > 0:
            workingLabel +=", 'Data" + str(chartDim) + "'"
            chartDim -= 1
        workingLabel +="],"
        htmlPriorToChart += workingLabel
    else: # use existing labels
        workingLabel ="['"+chartLabels.pop(0)+"'"
        for l in chartLabels:
            workingLabel +=", '" + l + "'"
        workingLabel +="],"
        htmlPriorToChart += workingLabel
    # Next we create the chart in HTML
    for datum in chartableDict.keys():
        # add a label and data row to the htmlDataChart
        if htmlDataChart:
            htmlDataChart +=',' # if its not blank put a comma at the end, saves unneeded trailing comma         
        if datum.find("'") + 1 : # fix raw ' in labels 
            fixed_datum = datum
            fixed_datum = fixed_datum.replace("'","feet")
            htmlDataChart += "\n          ['" + fixed_datum  + "',   " + str(chartableDict[datum]) + '  ]' 
        else: 
            htmlDataChart += "\n          ['" + str(datum) + "',   " + str(chartableDict[datum]) + '  ]' 
    htmlDataChart += '\n        ]);\n'    #close char
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