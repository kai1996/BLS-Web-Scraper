'''
Scrape the BLS QCEW API for county level data
'''

import urllib.request


# *******************************************************************************
# qcewCreateDataRows : This function takes a raw csv string and splits it into
# a two-dimensional array containing the data and the header row of the csv file
#
def qcewCreateDataRows(csv):
    dataLines = csv.split(b'\r\n')
    dataRows = []
    for row in dataLines:
        dataRows.append(row.split(b','))
    return dataRows
# *******************************************************************************


# *******************************************************************************
# qcewGetAreaData : This function takes a year, quarter, and area argument and
# returns an array containing the associated area data. Use 'a' for annual
# averages. 
# For all area codes and titles see:
# http://www.bls.gov/cew/doc/titles/area/area_titles.htm
#
def qcewGetAreaData(year,qtr,area):
    urlPath = "http://www.bls.gov/cew/data/api/[YEAR]/[QTR]/area/[AREA].csv"
    urlPath = urlPath.replace("[YEAR]",year)
    urlPath = urlPath.replace("[QTR]",qtr)
    urlPath = urlPath.replace("[AREA]",area)
    httpStream = urllib.request.urlopen(urlPath)
    csv = httpStream.read()
    httpStream.close()
    return qcewCreateDataRows(csv)
# *******************************************************************************


# *******************************************************************************
# qcewGetIndustryData : This function takes a year, quarter, and industry code
# and returns an array containing the associated industry data. Use 'a' for 
# annual averages. Some industry codes contain hyphens. The CSV files use
# underscores instead of hyphens. So 31-33 becomes 31_33. 
# For all industry codes and titles see:
# http://www.bls.gov/cew/doc/titles/industry/industry_titles.htm
#
def qcewGetIndustryData(year,qtr,industry):
    urlPath = "http://www.bls.gov/cew/data/api/[YEAR]/[QTR]/industry/[IND].csv"
    urlPath = urlPath.replace("[YEAR]",year)
    urlPath = urlPath.replace("[QTR]",qtr)
    urlPath = urlPath.replace("[IND]",industry)
    httpStream = urllib.request.urlopen(urlPath)
    csv = httpStream.read()
    httpStream.close()
    return qcewCreateDataRows(csv)
# *******************************************************************************


all_industries = qcewGetIndustryData("2015","1","10")
#Print row 6 column 3
print(all_industries[5][2])

#all_industries is a list of lists.  Each cell is a quoted string in byte format.
#When printed to csv each cell will look like this:  b'"100"'
#To prevent that, decode the byte as utf-8 and strip the parentheses of the strings
#Create a new list of lists with the cleaned data
all_industries_clean = []
for i in range(0, len(all_industries)):
    newlist = []
    for j in all_industries[i]:
        newlist.append(j.decode().strip("\""))
    all_industries_clean.append(newlist)
#Print row 6 column 3 to verify the data has been cleaned
print(all_industries_clean[5][2])

import csv

csvFile = open("BLS_Industry_Data_by_County.csv", 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
for row in range(0, len(all_industries_clean)):
    #Write the first 16 columns - everything after that is junk
    writer.writerow(all_industries_clean[row][0:16])

csvFile.close()



