
## (c) Karen Belita
## Team Neighborhood
## Last Updated 8/5/2016

##################################
## INGESTION OF ACS DATA ########
##################################

#####################
### Dependencies ####
####################

import os
import requests

###########################
###  Variables  ###########
###########################

censusKey="8d8c26917724beb2b09b2907e75f4f810f9ccaf1"
varlist="NAME,B01003_001E,B12001_003E,B12001_012E,B19013_001E,B25064_001E,B25088_002E,B01002_002E,B01002_003E"

## population  = B01003_001E
## male only never married total = B12001_003E
## female only never married total = B12001_012E
## median househould income = B19013_001E
## median gross rent = B25064_001E
## median monthly mortgage cost of those with a mortage = 25088_002E
## median age of males = B01002_002E
## median age of females B01002_003E

years = ["2014", "2012"] 

###########################
###  Functions  ###########
###########################


def api_download(year):

    path_year = os.path.join(os.getcwd(),"ACS", year)
    file_name = path_year + "/" + "ACS" + year + ".txt"
    url="http://api.census.gov/data/"+year+"/acs1?get="+varlist+"&for=metropolitan+statistical+area/micropolitan+statistical+area:*&key="+censusKey
    
    if not os.path.exists(path_year):
        os.makedirs(path_year)

    if os.path.isfile(file_name):
        pass
    else:
        census_data = requests.get(url)
        f = open(file_name, "w")
        f.write(census_data.text.encode('utf-8'))
        f.close()


def main():
    """
    Main execution
    """
    for year in years:
        api_download(year)

#######################
### Execution ########
#######################

if __name__ == '__main__':
    main()