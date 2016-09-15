
## (c) Karen Belita
## Team Neighborhood
## Last Updated 8/7/2016

#############################################
## INGESTION FOR MSA TOP 300 by POPULATION ##
#############################################

###################
## DEPENDENCIES ##
###################

import os
import requests
import pandas as pd
import csv

###########################
###  Variables  ###########
###########################

censusKey="8d8c26917724beb2b09b2907e75f4f810f9ccaf1"
varlist="NAME,B01003_001E"
years = ["2014"] 


def api_download(year):

    path_year = os.path.join(os.getcwd())
    file_name = path_year + "/" + "MSA" + ".txt"
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

def MSA_clean():

    filepath = os.path.join(os.getcwd(), "MSA.txt")
    df = pd.read_csv(filepath)


    ##################################
    ## Cleaning of Rows and Columns ##
    ##################################

    df.reset_index(level=0, inplace=True)  ## reset index

    df.columns = ["MSA1", "MSA2", "Population", "CBSA", "DELETE"]

    df["CBSA"] = df["CBSA"].map(lambda x: str(x)[:-1]) ## removes the  ] at the end of numbers is CBSA

    df["MSA Name"] = df["MSA1"].map(str) + df["MSA2"].map(str) ## creates new wrong column called MSA

    df.drop(df.columns[[0,1,4,]], axis=1, inplace=True) ## drop extra columns

    df["MSA Name"]= df["MSA Name"].map(lambda x: str(x)[:-1]) ## removes the "" at the end of numbers is CBSA

    df["MSA Name"]= df["MSA Name"].map(lambda x: str(x)[2:]) ## removes the  ]"" at the end of numbers is CBSA

    df_ranked = df.sort("Population", ascending = False) ## sort by population

    df_ranked.reset_index(level=0, inplace=True) ## reset index

    df_ranked.drop(df_ranked.columns[[0]], axis=1, inplace=True) ## remove first row because shuffled index

    ####################
    ## Finalzing Data ##
    ####################
    
    ## take only first 300
    df_ranked_300 = df_ranked.head(300)
    ## convert to csv
    df_ranked_300.to_csv("MSA_300.csv")



def main():
    """
    Main execution
    """
    for year in years:
        api_download(year)

    MSA_clean()

#######################
### Execution ########
#######################

if __name__ == '__main__':
    main()