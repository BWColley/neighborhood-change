"""
Ingestion and Wrangling code for Walk Score data.
Includes Walk Score, Transit Score, and Bike Score from walkscore.com
Code was modified from  https://github.com/evilsoapbox/RandomPython/blob/master/grab_walkscore_data.py
"""

"""
There's a dependency that CBSA-CITY-ST.csv file has been created.
There's a dependency that MSA_300.csv file has been created.
"""


"""
Imports for this script
"""
import argparse
import re
import requests
import unicodecsv
import pandas as pd


"""
Create constant variables for parsing from the walkscore url.
"""
BASE_URL = 'https://www.walkscore.com/%s/%s'
NULL_SCORE_VALUE = 0
REGEX_FILTERS = {
    'walkscore': '\/\/pp.walk.sc\/badge\/walk\/score\/(\d+)\.svg',
    'transitscore': '\/\/pp.walk.sc\/badge\/transit\/score\/(\d+)\.svg',
    'bikescore': '\/\/pp.walk.sc\/badge\/bike\/score\/(\d+)\.svg'
    }


"""
Parse the score data on the walkscore page.
"""
def parse_score_data(content):
    return_data = [0,0,0]
    score_hash = dict()
    for score_type in REGEX_FILTERS.keys():
        score_data = re.search(REGEX_FILTERS[score_type], content)
        if score_data is not None:
            score_hash[score_type] = score_data.group(1)
        else:
            score_hash[score_type] = NULL_SCORE_VALUE
    return score_hash


"""
Return a well-formatted Walkscore URL
"""
def return_walkscore_url(state, city):
    return BASE_URL % (state, city.replace(' ', '_'))


"""
Pull in the CBSA to City-St file as a dataframe.
"""
citystate_dataset = pd.read_csv("CBSA-CITY-ST.csv")


"""
Clean up Washington DC for walkscore.com
"""
DCcorrection = {'DC':'Washington D.C.'}
citystate_dataset.loc[citystate_dataset['STATE'].isin(DCcorrection.keys()), 'CITY'] = citystate_dataset['STATE'].map(DCcorrection)


"""
Create clean dataframe and count number of cities for loop.
"""
subset = citystate_dataset[['CBSA','CITY','STATE']]
CityStateList = [tuple(x) for x in subset.values]

NoCities = len(CityStateList)


"""
Loop through the city-state dataframe pulling down the scores from walkscore.com.
Return a list of typles.
This takes ~8 minutes on my computer.
"""
MultiList = []

K = 0

while K < NoCities:
    SingleTuple = CityStateList[K]
    CBSA = SingleTuple[0]
    City = SingleTuple[1]
    State = SingleTuple[2]

    city_url = return_walkscore_url(State, City)

    r = requests.get(city_url)
    page_data = str(r.content)
    score_data = parse_score_data(page_data)
    MultiList.insert(K,
                     (CBSA,
                      City,
                      State,
                      score_data['walkscore'],
                      score_data['transitscore'],
                      score_data['bikescore']
                     )
                    )

    K = K + 1


"""
Create a dataframe with the Walk_Score, Transit_Score, and Bike_Score.
"""
df_Walk_Score = pd.DataFrame(MultiList)
df_Walk_Score.columns = ['CBSA','City','St','Walk_Score','Transit_Score','Bike_Score']


"""
Put Washington, DC back to original format.
"""
DCrevert = {'DC':'Washington'}
df_Walk_Score.loc[df_Walk_Score['St'].isin(DCrevert.keys()), 'City'] = df_Walk_Score['St'].map(DCrevert)


"""
Pull in the MSA_300 file as a dataframe and merge with Walk Score on CBSA.
Drop columns leaving only index, MSA and scores.
Convert Walk, Transit, and Bike scores from strings to floats.
"""
df_MSA = pd.read_csv("MSA_300.csv")
df_MSA_Walk_Merge = pd.merge(df_MSA, df_Walk_Score, on = 'CBSA')
df_MSA_Walk = df_MSA_Walk_Merge.drop(df_MSA_Walk_Merge.columns[[0,1,2,4,5]], 1)

df_MSA_Walk.Walk_Score = df_MSA_Walk.Walk_Score.astype(float).fillna(0.0)
df_MSA_Walk.Transit_Score = df_MSA_Walk.Transit_Score.astype(float).fillna(0.0)
df_MSA_Walk.Bike_Score = df_MSA_Walk.Bike_Score.astype(float).fillna(0.0)


"""
Create average score per MSA.
"""
Walk_by_MSA = df_MSA_Walk.groupby(['MSA Name']).mean()


"""
Return final CSV file.
"""
Walk_by_MSA.to_csv('Walk_by_MSA.csv')
