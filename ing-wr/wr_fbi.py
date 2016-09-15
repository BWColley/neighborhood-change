
## (c) Karen Belita
## Team Neighborhood
## Last Updated 8/6/2016

##################################
## WRANGLING OF FBI DATA ########
##################################

##############
## OUTPUT ###
#############

## crime_rates.csv
## Crime Rate for 2014, NaNs are filled with 2013 data 

##########################
## VARIABLES FOR CBSA ###   = 10 TOTAL 
##########################
# Violent Crime
# Murder Manslaughter
# Rape
# Robbery
# Aggravated Assault
# Property Crime Rate
# Burglary
# Larceny Theft
# Motor Vehicle Theft
# Total Crime Rate 



####################
## DEPENDENCIES ####
####################

import pandas as pd
import os 
import csv
import xlrd
import numpy as np
# "ing_fbi.py" was ran
# "ing_wr_MSA300.py" as ran
# "MSA_300.csv" in directory 
# 'Table_6_Crime_in_the_United_States_by_Metropolitan_Statistical_Area_2014.xls" is in FBI directory
# 'Table_6_Crime_in_the_United_States_by_Metropolitan_Statistical_Area_2013.xls" is in FBI directory 



#############################
### Cleaning 2014 FBI Data ##
#############################

xls_file = os.path.join(os.getcwd(),'FBI', 'ZIP', '2014', 'Table_6_Crime_in_the_United_States_by_Metropolitan_Statistical_Area_2014.xls')

data_xls = pd.read_excel(xls_file, '14tbl06', index_col=None)
data_xls.to_csv('fbi14.csv', encoding='utf-8')

df = pd.read_csv('fbi14.csv')

df = df.drop([0, 1]) ## remove first two rows

# column names rename
df.columns = ["DELETE", "MSA Name", "MSA_AREA", "Population", "Violent_Crime_Rate", "Murder_Manslaughter", "Rape", "Robbery", "Aggravated_Assault", "Property_Crime_Rate", "Burglary", "Larceny_Theft", "Motor_Vehicle_Theft"]

df = df.drop([2]) ## drop 2nd row which is same as colum title 

df = df.drop(df.columns[[0]], axis=1)  ## drop first column

col = "MSA Name"

df[col] = df[col].ffill() ##forward fill


df.reset_index(level=0, inplace=True) ## makes numbers the row names ## reset

df.drop(df.columns[[0]], axis=1, inplace=True) ## drop columns old index

df.drop(df.tail(6).index, inplace=True) ## remove the bottom


# convert all NaN in MSA Areas into blank for sorting purposes
df1 = df.fillna(" ") 

df1 = df1[df1["MSA_AREA"].str.contains("Rate per 100,000 inhabitants")] ## matches only "Rate per 100,00 inhabitants

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = 'M.S.A.', value = "Metro Area", regex=True)

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = 'M.S.A', value = "Metro Area", regex=True)

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = 'Metro Area ', value = "Metro Area", regex=True) ## 1 space

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = 'Metro Area  ', value = "Metro Area", regex=True) ## 1 space

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = 'Puerto Rico', value = "PR", regex=True)

df1 = df1[df1["MSA Name"].str.contains("M.D.") == False]

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = "\d" , value = "", regex=True) # if there is m.d in MSA column remove that row

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = "-+" , value = "", regex=True) 

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = ",.", value = "", regex=True) ## remove all comass

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = " *", value = "", regex=True) ## remove all spaces

df1["MSA Name"] = df1["MSA Name"].str.lower()

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = "louisville.*", value = "louisvillejeffersoncountykyinmetroarea", regex = True) 

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = "sacramento.*", value = "sacramentorosevilleardenarcadecametroarea", regex = True) 

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = "scranton.*", value = "scrantonwilkesbarrehazletonpametroarea", regex = True) 

df1["MSA Name"] = df1["MSA Name"].replace(to_replace = "nashville.*", value = "nashvilledavidsonmurfreesborofranklintnmetroarea", regex = True) 


df1.reset_index(level=0, inplace=True) ## reset

df1.drop(df1.columns[[0]], axis=1, inplace=True) ## remove column 0

## drop to leave just crime rates
df1 = df1.drop(df1.columns[[1,2]], axis=1)  ## drop second column


####################
## 2014 CRIME DATA #
###################

df_FBI = df1

###############################################################
## Cleaning of MSA300 data to be able to merge on "MSA NAME" ##
###############################################################

## get MSA 300 list ##
df_MSA300 = pd.read_csv("MSA_300.csv")

df_MSA300["MSA Name"] = df_MSA300["MSA Name"].replace(to_replace = "\d" , value = "", regex=True) 
# if there is m.d in MSA column remove that row
df_MSA300["MSA Name"] = df_MSA300["MSA Name"].replace(to_replace = "-+" , value = "", regex=True) 
df_MSA300["MSA Name"] = df_MSA300["MSA Name"].replace(to_replace = ",.", value = "", regex=True) ## remove all comass
df_MSA300["MSA Name"] = df_MSA300["MSA Name"].replace(to_replace = " *", value = "", regex=True) ## remove all spaces
df_MSA300["MSA Name"] = df_MSA300["MSA Name"].str.lower()


######################################
## MERGE MSA 300 and 2014 CRIME DATA #
#####################################


df_fbitemp = pd.merge(df_MSA300, df_FBI, how = "left", on = "MSA Name")

df_fbitemp= df_fbitemp.drop(df_fbitemp.columns[[0,1]], axis=1)  ## drop first column

df_fbitemp = df_fbitemp.replace(" ", np.NaN) ## put NaN instead of 0 (put back later)

## Convert data into float
df_fbitemp["Violent_Crime_Rate"] = df_fbitemp["Violent_Crime_Rate"].astype("float") ## converts to float
df_fbitemp["Property_Crime_Rate"] = df_fbitemp["Property_Crime_Rate"].astype("float") ## converts to float

# ASSIGN VARIABLE FOR  MERGED 2014 DATA FOR MERGING WITH 2013 and CALCULATION
df_MSA2014 = df_fbitemp

# ASSIGN VARIABLE FOR MERGED 2014 DATA FOR CALCULATION
df_MSA2014_comb = df_fbitemp




#############################
### Cleaning 2013 FBI Data ##
#############################


xls_file13 = os.path.join(os.getcwd(),'FBI', 'ZIP', '2013', 'Table_6_Crime_in_the_United_States_by_Metropolitan_Statistical_Area_2013.xlsx')

data_xls13 = pd.read_excel(xls_file13, '13tbl6', index_col=None)
data_xls13.to_csv('fbi13.csv', encoding='utf-8')

df13 = pd.read_csv('fbi13.csv')

df13 = df13.drop([0, 1]) ## remove first two rows

df13.columns = ["DELETE", "MSA Name", "MSA_AREA", "Population", "Violent_Crime_Rate", "Murder_Manslaughter", "Rape", "Robbery", "Aggravated_Assault", "Property_Crime_Rate", "Buglary", "Larceny_Theft", "Motor_Vehicle_Theft"]

df13 = df13.drop([2]) ## drop 2nd row which is same as colum title 

df13 = df13.drop(df13.columns[[0]], axis=1)  ## drop first column

col = "MSA Name"
df13[col] = df13[col].ffill() ##forward fill on MSA Name

df13.reset_index(level=0, inplace=True) ## makes numbers the row names ## reset

df13.drop(df13.columns[[0]], axis=1, inplace=True) ## drop columns old index

df13.drop(df13.tail(7).index, inplace=True) ## remove the bottom


df13 = df13.fillna(" ") 

df13 = df13[df13["MSA_AREA"].str.contains("Rate per 100,000 inhabitants")] ## matches only "Rate per 100,00 inhabitants


df13["MSA Name"] = df13["MSA Name"].replace(to_replace = 'M.S.A', value = "Metro Area", regex=True)

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = 'Metro Area ', value = "Metro Area", regex=True) ## 1 space

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = 'Metro Area  ', value = "Metro Area", regex=True) ## 1 space

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = 'Puerto Rico', value = "PR", regex=True)

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = "Metro Area.", value = "Metro Area", regex=True) ## remove all spaces

df13 = df13[df13["MSA Name"].str.contains("M.D.") == False]

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = "\d" , value = "", regex=True) 

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = "-+" , value = "", regex=True) 

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = ",.", value = "", regex=True) ## remove all comass

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = " *", value = "", regex=True) ## remove all spaces

df13["MSA Name"] = df13["MSA Name"].str.lower()

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = "louisville.*", value = "louisvillejeffersoncountykyinmetroarea", regex = True) 

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = "sacramento.*", value = "sacramentorosevilleardenarcadecametroarea", regex = True) 

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = "scranton.*", value = "scrantonwilkesbarrehazletonpametroarea", regex = True) 

df13["MSA Name"] = df13["MSA Name"].replace(to_replace = "nashville.*", value = "nashvilledavidsonmurfreesborofranklintnmetroarea", regex = True) 

df13.reset_index(level=0, inplace=True) ## makes numbers the row names ## reset

df13.drop(df13.columns[[0]], axis=1, inplace=True) ## remove column 0

df13 = df13.drop(df13.columns[[1,2]], axis=1)  ## drop second column


######################################
## MERGE MSA 300 and 2014 CRIME DATA #
######################################

##MERGE WITH MSA300

df_fbitemp2 = pd.merge(df_MSA300, df13, how = "left", on = "MSA Name")

df_fbitemp2= df_fbitemp2.drop(df_fbitemp2.columns[[0,1]], axis=1)  ## drop first column

df_fbitemp2 = df_fbitemp2.replace(" ", np.NaN)

df_fbitemp2["Violent_Crime_Rate"] = df_fbitemp2["Violent_Crime_Rate"].astype("float") ## converts to float

df_fbitemp2["Property_Crime_Rate"] = df_fbitemp2["Property_Crime_Rate"].astype("float") ## converts to float

# ASSIGN VARIABLE FOR  MERGED 2013 DATA FOR MERGING WITH 2014 and CALCULATION
df_MSA2013 = df_fbitemp2

# ASSIGN VARIABLE FOR  MERGED 2014 DATA FOR CALCULATION
df_MSA2013_comb = df_fbitemp2



##########################################
# COMBINE DATA SETS OF YEARS TO FILL NA ###
##########################################


df_rem_nan_14 =  df_MSA2014.fillna(df_MSA2013)

df_rem_nan_13 =  df_MSA2013.fillna(df_MSA2014)

##############################
## CALCULATE TOTAL CRIME RATE
#############################

## FOR 2014 ONLY
df_MSA2014_comb["Total_Crime_Rate"] = np.where((df_MSA2014_comb["Violent_Crime_Rate"].notnull() &  df_MSA2014_comb["Property_Crime_Rate"].notnull()), (df_MSA2014_comb["Violent_Crime_Rate"] + df_MSA2014_comb["Property_Crime_Rate"]), np.NaN) 

## FOR 2013 ONLY
df_MSA2013_comb["Total_Crime_Rate"] = np.where((df_MSA2013_comb["Violent_Crime_Rate"].notnull() &  df_MSA2013_comb["Property_Crime_Rate"].notnull()), (df_MSA2013_comb["Violent_Crime_Rate"] + df_MSA2013_comb["Property_Crime_Rate"]), np.NaN) 

## FOR 2014 with 2013 data for NaN values
df_rem_nan_14["Total_Crime_Rate"] = np.where((df_rem_nan_14["Violent_Crime_Rate"].notnull() &  df_rem_nan_14["Property_Crime_Rate"].notnull()), (df_rem_nan_14["Violent_Crime_Rate"] + df_rem_nan_14["Property_Crime_Rate"]), np.NaN) 

## FOR 2013 with 2014 data for NaN values
df_rem_nan_13["Total_Crime_Rate"] = np.where((df_rem_nan_13["Violent_Crime_Rate"].notnull() &  df_rem_nan_13["Property_Crime_Rate"].notnull()), (df_rem_nan_13["Violent_Crime_Rate"] + df_rem_nan_13["Property_Crime_Rate"]), np.NaN) 


###############################
## REMOVE "MSA NAME" COLUMN ##
#############################

df_MSA2014_comb.drop(df_MSA2014_comb.columns[[1]], axis=1, inplace=True) ## drop columns old index

df_MSA2013_comb.drop(df_MSA2013_comb.columns[[1]], axis=1, inplace=True) ## drop columns old index

df_rem_nan_14.drop(df_rem_nan_14.columns[[1]], axis=1, inplace=True) ## drop columns old index

df_rem_nan_13.drop(df_rem_nan_13.columns[[1]], axis=1, inplace=True) ## drop columns old index




###################
## SAVE INTO CSV ##
##################


#df_MSA2014_comb.to_csv("crime_rate14.csv") ## only 2014
#df_MSA2014_comb.to_csv("crime_rate13.csv") ## only 2013
df_rem_nan_14.to_csv("crime_rates.csv") ##missing values in 2014 filled with 2013 (if it exists)
#df_rem_nan_14.to_csv("crime_rate13w14.csv") ## missing values in 2014 filled with 2013 (if it exists)






