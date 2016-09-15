
# coding: utf-8

"""
Imports for this script
"""
import urllib2
import unicodecsv
import xlrd
import os
import os.path
import pandas as pd


"""
Define URL for the Federal Transit Authority Safety (FTA) xls file.
"""
url = "https://www.transit.dot.gov/sites/fta.dot.gov/files/SSTimeSeries-March2016-160701.xls"


"""
Pull down FTA xls file.
"""
if os.path.isfile("TimeSeriesTransitData_March2016.xls"):
    pass
else:
    response = urllib2.urlopen(url)
    chunksize = 16 * 1024
    with open("TimeSeriesTransitData_March2016.xls", "wb") as f:
        while True:
            chunk = response.read(chunksize)
            if not chunk: break
            f.write(chunk)


"""
Covert FTA xls file to csv.
"""
def xls_to_csv():
    workbook = xlrd.open_workbook("TimeSeriesTransitData_March2016.xls")
    worksheet = workbook.sheet_by_name("2014")
    csvfile = open("TSTD2014.csv", "wb")
    writecsv = unicodecsv.writer(csvfile, quoting=unicodecsv.QUOTE_ALL)

    for rownum in xrange(worksheet.nrows):
        writecsv.writerow(worksheet.row_values(rownum))

    csvfile.close()

xls_to_csv()


"""
Pull in the CBSA to City-St file as a dataframe.
"""
citystate_dataset = pd.read_csv('CBSA-CITY-ST.csv')


"""
Insert a new column in the citystate dataframe that's a unique identifier concatenating State & City.
"""
citystate_dataset['StateCity'] = citystate_dataset['STATE'].map(str) + citystate_dataset['CITY']



"""
Read in the FTA Safety csv as a dataframe.
Create new dataframe with only the relevant columns.
"""
FedTransit = pd.read_csv('TSTD2014.csv', skiprows=2, skip_footer=31)
FTA_dataframe = FedTransit[['NTDID',
                            'City',
                            'State',
                            'Mode',
                            'PMT',
                            '    Event Total',
                            '    Total Fatalities',
                            '    Total Injuries'
                           ]]


"""
Insert a new column in the FTA dataframe that's a unique identifier concatenating State & City.
"""
FTA_dataframe['StateCity'] = FTA_dataframe['State'].map(str) + FTA_dataframe['City']


"""
Merge the two dataframes on the StateCity unique identifier.
Group the merged data set on CBSA.
"""
TransitSafetyCBSA = pd.merge(FTA_dataframe,citystate_dataset,on='StateCity')
TransitSafetyCBSAsum = TransitSafetyCBSA.groupby(['CBSA'],as_index=False).sum()


"""
Insert three new columns in the merged dataframe for the three relevant safety metrics.
mPMT = millions of Passenger Miles Traveled
Per the FTA, an Event represents a Collision, Derailment, Fire, or other reportable event.
"""
TransitSafetyCBSAsum['Event/mPMT'] = TransitSafetyCBSAsum['    Event Total']/TransitSafetyCBSAsum['PMT'] * 1000000
TransitSafetyCBSAsum['Fatalities/mPMT'] = TransitSafetyCBSAsum['    Total Fatalities']/TransitSafetyCBSAsum['PMT'] * 1000000
TransitSafetyCBSAsum['Injuries/mPMT'] = TransitSafetyCBSAsum['    Total Injuries']/TransitSafetyCBSAsum['PMT'] * 1000000


"""
Create final dataframe with only the revelent
"""
FTA_by_CBSA = TransitSafetyCBSAsum[['CBSA',
                                                'Event/mPMT',
                                                'Fatalities/mPMT',
                                                'Injuries/mPMT'
                                              ]]


"""
Change the infinite value error for City = Lima to NaN
"""
inf_correct = {30620:0}
FTA_by_CBSA.loc[FTA_by_CBSA['CBSA'].isin(inf_correct.keys()), 'Event/mPMT'] = FTA_by_CBSA['CBSA'].map(inf_correct)
print FTA_by_CBSA.describe()

"""
Return final CSV file.
"""
FTA_by_CBSA.to_csv('FTA_by_CBSA.csv')
