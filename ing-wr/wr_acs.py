
## (c) Karen Belita
## Team Neighborhood
## Last Updated 8/5/2016

##################################
## WRANGLING OF ACS DATA ########
##################################

########################
## ACS VARIABLES USED ##
########################

## population  = B01003_001E
## male only never married total for 15 years and over = B12001_003E
## female only never married total  for 15 years and over= B12001_012E
## median househould income = B19013_001E
## median gross rent = B25064_001E
## median monthly mortgage cost of those with a mortage = 25088_002E
## median age of males = B01002_002E
## median age of females  = B01002_003E 

##############
## OUTPUT ###
#############

## population300.csv 
## single_population.csv 
## housing_costs.csv 
## income_change.csv
## median_income.csv
## median_age

##########################
## VARIABLES FOR CBSA ###   =  15 TOTAL 
##########################

## Population in population300.csv 
## Single Men Population in single_population.csv
## Single Women Population in single_population.csv
## Ratio of Single Men to Single Women in single_population.csv (Single Men Population / Single Women Population)
## Population Percent of Single Men in single_population.csv (Single Men Population / Population)
## Population Percent of Single Women in single_population.csv (Single Women Population / Population)
## Median Gross Rent in housing_costs.csv
## Median Monthly Mortgage in housing_costs.csv
## Rent Burden in housings.csv (Median Gross Rent / Median Household Income)
## Mortgage Burden in housing_costs.csv (Median Monthly Mortgage / Median Household Income)
## Income Change from 2012 to 2014 in income_change.csv ((Median Household Income 2014 - Median Household Income 2012) / Median Household Income)
## Median Household Income in median_income.csv
## Median Age of Men in median_age.csv
## Median Age of Women in median_age.csv
## Median Age in median_age.csv ((Median Age of Men + Median Age of Women) / 2)



#####################
### Dependencies ####
####################

import pandas as pd
import os 
import csv
import xlrd

# !!!!!!!!! #
# ing_acs.py was ran
# WITHIN directory "ACS2014.txt" & "ACS2012.txt" exist

filepath = os.path.join(os.getcwd(),"ACS", "2014", "ACS2014.txt")

df = pd.read_csv(filepath)




##################################
## Cleaning of Rows and Columns ##
##################################

df.reset_index(level=0, inplace=True) ## reset index 

## rename of column names
df.columns = ["MSA1", "MSA2", "Population", "Male Never Married",  "Female Never Married", "Median Household Income",  "Median Gross Rent", "Median Monthly Mortgage","Median Age of Male Population",  "Median Age of Female Population",  "CBSA", "EMPTY"]


df["CBSA"] = df["CBSA"].map(lambda x: str(x)[:-1]) ## removes the  ] at the end of numbers is CBSA
df["MSA Name"] = df["MSA1"].map(str) + df["MSA2"].map(str) ## creates new long column called Name since it was split in two
df.drop(df.columns[[0,1,11]], axis=1, inplace=True) ## drop unnecessary columns
df["MSA Name"]= df["MSA Name"].map(lambda x: str(x)[:-1]) ## removes the  '' at the end of numbers is CBSA
df["MSA Name"]= df["MSA Name"].map(lambda x: str(x)[2:]) ## removes the  ]'' at the end of numbers is CBSA

##########################
## Sorted by Population ##
##########################

## df_ranked is data sorted by population

df_ranked = df.sort("Population", ascending = False)
df_ranked.reset_index(level=0, inplace=True) ## rest index
df_ranked.drop(df_ranked.columns[[0]], axis=1, inplace=True) ## remove first column


#############################################
## TOP 100 MSA by POP includes all columns ##
#############################################

df_ranked_100 = df_ranked.head(100)

############################################
## TOP 300 MSA by POP includes all columns ##
#############################################

df_ranked_300 = df_ranked.head(300)


#######################
## MSA and POPULATION #
#######################


df_population = df_ranked.drop(df.columns[[1,2,3,4,5,6,7]], axis=1) ## removes columns 1:7  ## FOR POPULATION

cols = df_population.columns.tolist() #create list using columns

df_population = df_population[["CBSA", "Population", "MSA Name"]] #changed order 


# df_population.to_csv("MSA_population_complete.csv") ## to save in file if necessary

###############################
## TOP 100 MSA and POPULATION #
###############################

df_population_100 = df_population.head(100)  

# df_population_100.to_csv("MSA_Population_Top100.csv") ## to save in file if necessary

###############################
## TOP 300 MSA and POPULATION #
###############################

df_population_300 = df_population.head(300)  

df_population_300.to_csv("population300.csv")

###########################################
## MSA and RATIO OF SINGLE MEN TO WOMEN  ##
## and PERCENT OF SINGLE MEN             ##
## and PERCENT OF SINGLE WOMEN           ##
###########################################

# Unmarried men to Unmarried women 15 years and older 

df_single_M_F = df_ranked.drop(df_ranked.columns[[3,4,5,6,7,9]], axis=1,) 

cols_single = df_single_M_F.columns.tolist() ## allows to rearrange

df_single_M_F = df_single_M_F[["CBSA", "Population", "Male Never Married", "Female Never Married"]] 

## change column name
df_single_M_F.columns = ["CBSA", "Population", "Single Men Population", "Single Women Population"] 

## CALCULATING RATIO ##
df_single_M_F["Ratio of Single Men to Single Women"] = df_single_M_F["Single Men Population"] / df_single_M_F["Single Women Population"] 

## CALCULATING PERCENT SINGLE MEN POPULATION TO TOTAL POPULATION ##
df_single_M_F["Population Percent of Single Men"] = (df_single_M_F["Single Men Population"] / df_single_M_F["Population"]) * 100 

## CALCULATING PERCENT SINGLE WOMEN POPULATION TO TOTAL POPULATION ##
df_single_M_F["Population Percent of Single Women"] = (df_single_M_F["Single Women Population"] / df_single_M_F["Population"]) * 100

## Delete population column 
df_single= df_single_M_F.drop(df_single_M_F.columns[[1,]], axis=1) 

## save to csv complete list
# df_single.to_csv("single_population_complete.csv") ## save if necessary

###################################################
## TOP 300 MSA and RATIO OF SINGLE MEN TO WOMEN  ##
## and PERCENT OF SINGLE MEN            		 ##
## and PERCENT OF SINGLE WOMEN      		     ##
####################################################

df_single_100= df_single.head(100)

##df_single_100.to_csv("single_population_100.csv")## SAVE IF NECESSARY 


###################################################
## TOP 300 MSA and RATIO OF SINGLE MEN TO WOMEN  ##
## and PERCENT OF SINGLE MEN            		 ##
## and PERCENT OF SINGLE WOMEN         			 ##
###################################################

df_single_300= df_single.head(300)

df_single_300.to_csv("single_population.csv") ## SAVE IF NECESSARY 

################################################
## MSA and RENT BURDEN & MORTGAGE BURDEN#  	  ##
## and MEDIAN GROSS RENT 				      ##
## and MEDIAN MORTGAGE MONTHLY MORTGAGE COSTS ##
################################################

df_housing = df_ranked.drop(df_ranked.columns[[0,1,2,6,7,9]], axis=1) ## removes columns 1:7  ## FOR housing burden

cols_housing= df_housing.columns.tolist() ## allows to rearrange

df_housing = df_housing[["CBSA", "Median Household Income", "Median Gross Rent", "Median Monthly Mortgage"]] 


## CALCULATING RENT BURDEN ##
# MULTIPLYING MEDIAN GROSS RENT BY 12 then DIVIDED BY MEDIAN HOUSEHOLD INCOME
## RENT BURDEN ##
df_housing["Rent Burden"] = ((df_housing["Median Gross Rent"].map(int) * 12) / df_housing["Median Household Income"].map(int)) * 100

## CALCULATING MORTGAGE BURDEN
# MULTIPLYING MEDIAN GROSS RENT BY 12 then DIVIDED BY MEDIAN HOUSEHOLD INCOME
## MORTGAGE BURDEN ##
df_housing["Mortgage Burden"] = ((df_housing["Median Monthly Mortgage"] * 12) / df_housing["Median Household Income"] * 100)


## REMOVING MEDIAN HH INCOME ##
df_housing_costs = df_housing.drop(df_housing.columns[[1,]], axis=1) 

#df_housing_costs.to_csv("housing_costs_complete.csv") ## to save in file if necessary

###################################################
## TOP 100 MSA and RENT BURDEN & MORTGAGE BURDEN ##
## and MEDIAN GROSS RENT 				    	 ##
## and MEDIAN MORTGAGE MONTHLY MORTGAGE COSTS    ##
###################################################

df_housing_costs_100 = df_housing_costs.head(100)

## df_housing_costs_100.to_csv("housing_costs_100.csv") ## save if necessary

###################################################
## TOP 100 MSA and RENT BURDEN & MORTGAGE BURDEN ##
## and MEDIAN GROSS RENT 				    	 ##
## and MEDIAN MORTGAGE MONTHLY MORTGAGE COSTS    ##
###################################################

df_housing_costs_300 = df_housing_costs.head(300)

df_housing_costs_300.to_csv("housing_costs.csv")

###########################################
## MSA & INCOME CHANGE FROM 2012 to 2014 ##
###########################################

################
## INCOME 2014 #
################

df_inc2014 = df_ranked.drop(df_ranked.columns[[0,1,2,4,5,6,7,9]], axis=1, ) ## unnecessary rows

cols_income14= df_inc2014.columns.tolist() ## allows to rearrange

df_inc2014 = df_inc2014[["CBSA", "Median Household Income"]] ## rearrange columns

df_inc2014.columns = ["CBSA", "Median HH Income 2014"] ## change columns

# df_inc2014.to_csv("income_2014_complete.csv") ## save if necessary

## TOP 100
df_inc2014_100 = df_inc2014.head(100)

## TOP 300
df_inc2014_300 = df_inc2014.head(300)

################
## INCOME 2012 #
################

## download 2012 ACS DATA
filepath12 = os.path.join(os.getcwd(),"ACS", "2012", "ACS2012.txt")
df12 = pd.read_csv(filepath12, error_bad_lines=False)


df12.reset_index(level=0, inplace=True) ## makes numbers the row names
# rename rows
df12.columns = ["MSA1", "MSA2", "Population", "Male Never Married",  "Female Never Married", "Median Household Income",  "Median Gross Rent", "Median Mortgage","Median Gross Rent/Median Household Income",  "Median Mortgage/Median Household Income",  "CBSA", "EMPTY"]

df12["CBSA"] = df12["CBSA"].map(lambda x: str(x)[:-1]) ## removes the  ] at the end of numbers is CBSA
df12["MSA Name"] = df12["MSA1"].map(str) + df12["MSA2"].map(str) ## creates new wrong column called MSA

df12.drop(df12.columns[[0,1,11]], axis=1, inplace=True) ## drop unnecessary columsn

df12["MSA Name"]= df12["MSA Name"].map(lambda x: str(x)[:-1]) ## removes the  " at the end of numbers is CBSA

df12["MSA Name"]= df12["MSA Name"].map(lambda x: str(x)[2:]) ## removes the  ]"" at the end of numbers is CBSA

## sort by population
df_ranked12 = df12.sort("Population", ascending = False)

df_ranked12.reset_index(level=0, inplace=True) ## reset index

df_ranked12.drop(df_ranked12.columns[[0]], axis=1, inplace=True) ## remove first row

## DELETE UNNECESSARY COLUMNS 
df_inc2012 = df_ranked12.drop(df_ranked12.columns[[0,1,2,4,5,6,7,9]], axis=1, ) ## remove first row

cols_income12= df_inc2012.columns.tolist() ## allows to rearrange

df_inc2012 = df_inc2012[["CBSA", "Median Household Income"]] # column roder

df_inc2012.columns = ["CBSA", "Median HH Income 2012"] # rename columns
df_inc2012["CBSA"] = df_inc2012["CBSA"].replace(to_replace = "31100.*", value = "31080", regex = True) 


# df_inc2012.to_csv("income_2012.csv") ## save if necessary

###################################
## Merge Income of 2012 and 2014 ##
###################################

#Merge Incomes on CBSA based on ranking of 2014

df_income = pd.merge(df_inc2014_300, df_inc2012, on = "CBSA")

## CALCULATING INCOME CHANGE FROM 2012 TO 2014
df_income["Income Change 2012 to 2014"] = (((df_income["Median HH Income 2014"]  - df_income["Median HH Income 2012"]) / df_income["Median HH Income 2012"]) * 100) 

## DROP COLUMNS WITH YEAR JUST LEAVE PERCENT CHANGE
df_income_change = df_income.drop(df_income.columns[[1,2]], axis=1) 

# df_income_change.to_csv("income_change_complete.csv") ## SAVE IF NECESSARY

##################################################
## TOP 300 MSA & INCOME CHANGE FROM 2012 to 2014 #
##################################################

df_income_change.to_csv("income_change.csv")


###################################
## MSA & MEDIAN HOUSEHOLD INCOME ##
###################################

df_inc = df_ranked.drop(df_ranked.columns[[0,1,2,4,5,6,7,9]], axis=1, ) ## unnecessary rows

cols_inc= df_inc.columns.tolist() ## allows to rearrange

df_inc = df_inc[["CBSA", "Median Household Income"]] ## rearrange columns

# df_inc.to_csv("income_complete.csv") ## save if necessary

#################################
## TOP 100 MSA & MEDIAN INCOME #
################################

df_inc_100 = df_inc.head(100)

## df_inc_300.to_csv("median_income_100.csv") # save if necessary

################################
## TOP 300 MSA & MEDIAN INCOME #
################################

df_inc_300 = df_inc.head(300)

df_inc_300.to_csv("median_income.csv")

########################
## MSA & MEDIAN AGE  ##
#######################

df_median_age = df_ranked.drop(df_ranked.columns[[0,1,2,3,4,5,9]], axis=1, ) ## unnecessary rows

cols_median_age= df_median_age.columns.tolist() ## allows to rearrange

# rearrange columns
df_median_age = df_median_age[["CBSA", "Median Age of Male Population", "Median Age of Female Population"]] ## rearrange columns

# rename
df_median_age.columns = ["CBSA", "Median Age of Men", "Median Age of Women"]

## CALCULATING MEDIAN AGE
df_median_age["Median Age"] = (df_median_age["Median Age of Men"] + df_median_age["Median Age of Women"]) / 2 

# df_median_age.to_csv("median_age_complete.csv") ## save if necessary


##############################
## TOP 100 MSA & MEDIAN AGE #
#############################

df_median_age_100 = df_median_age.head(100)

## df_inc_300.to_csv("median_income_100.csv") # save if necessary

##############################
## TOP 300 MSA & MEDIAN Age #
#############################

df_median_age_300 = df_median_age.head(300)

df_median_age_300.to_csv("median_age.csv")





