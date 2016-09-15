## (c) Karen Belita
## Team Neighborhood
## Last Updated 8/5/2016

##################################
## INGESTION OF FBI DATA########
##################################

###################
## OUTPUT ########
##################

# 2014.zip in FBI folder
# 2013.zip in FBI folder

#####################
### Dependencies ####
####################

import urllib2
import zipfile
import os
import os.path

###########################
###  Variables ############
###########################

## WARNING ## !!!!!!!!!
# ALWAYS CHECK FIRST LINKS ARE WORKING ##

year_2014 = "https://ucr.fbi.gov/crime-in-the-u.s/2014/crime-in-the-u.s.-2014/resource-pages/downloads/cius2014datatables.zip"
year_2013 = "https://ucr.fbi.gov/crime-in-the-u.s/2013/crime-in-the-u.s.-2013/resource-pages/downloads/cius2013datatables.zip"
year_2012 = "https://ucr.fbi.gov/crime-in-the-u.s/2012/crime-in-the-u.s.-2012/resource-pages/cius2012datatables.zip"
year_2011 = "https://ucr.fbi.gov/crime-in-the-u.s/2011/crime-in-the-u.s.-2011/CIUS2011datatables.zip"
year_2010 = "https://ucr.fbi.gov/crime-in-the-u.s/2010/crime-in-the-u.s.-2010/CIUS2010datatables.zip"
year_2009 = "https://www2.fbi.gov/ucr/cius2009/documents/cius2009datatables.zip"
year_2008 = "https://www2.fbi.gov/ucr/cius2008/documents/cius2008datatables.zip"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

years = [year_2014, year_2013]

###########################
###  Functions  ###########
###########################

def zip_download(year):
    path_zip = os.path.join(os.getcwd(),"FBI", "ZIP")
    path_year = os.path.join(os.getcwd(),"FBI", "ZIP", year[-18:-14])
    zip_name = path_zip + "/" + year[-18:-14] + ".zip"
    
    if not os.path.exists(path_year):
        os.makedirs(path_year)

    if os.path.isfile(zip_name):
        pass
    else:
        request = urllib2.Request(year, headers = hdr)
        response = urllib2.urlopen(request)
        chunksize = 64 * 1024
        with open(zip_name, "wb") as f:
            while True:
                chunk = response.read(chunksize)
                if not chunk: break
                f.write(chunk)
                
    if os.listdir(path_year) == []:
        zip = zipfile.ZipFile(zip_name.encode("utf-8"), "r")
        zip.extractall(path_year)


def main():
    """
    Main executions
    """
    for year in years: 
        zip_download(year)

#######################
### Execution ########
#######################

if __name__ == '__main__':
    main()
