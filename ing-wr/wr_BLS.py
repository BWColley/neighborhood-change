import csv
import os
import pandas as pd
import numpy as np


datapath = os.path.join(os.getcwd(), "data")

filename = datapath + "/BLSMetroData.txt"

data = pd.read_csv(filename, sep='\t')
df=pd.DataFrame(data)
unemrate = df.loc[(data['BLSCODE']==3) & (data['YEAR']==2014)]
unem = unemrate.groupby(['CBSA']).agg({'VALUE': np.mean})

employment = df.loc[(data['BLSCODE']==5) & (data['YEAR']==2014)]
emp = employment.groupby(['CBSA']).agg({'VALUE': np.mean})

laborforce = df.loc[(data['BLSCODE']==6) & (data['YEAR']==2014)]
labf = laborforce.groupby(['CBSA']).agg({'VALUE': np.mean})

hdata=pd.merge(unem, emp, how='left', left_index='CBSA', right_index='CBSA')

hdata=pd.merge(hdata, labf, how='left', left_index='CBSA', right_index='CBSA')


hdata=hdata.rename(columns = {'VALUE_x':'UnemRate','VALUE_y':'TotalEmp','VALUE':'TotalLabor'})


hdata['UnemRate']=hdata['UnemRate'].fillna(0.0).round(1)
hdata['TotalEmp']=hdata['TotalEmp'].fillna(0.0).astype(int)
hdata['TotalLabor']=hdata['TotalLabor'].fillna(0.0).astype(int)


#final data from BLS saved to ./data/BLSEmploymentData.txt with CBSA, Unemployment Rate, Total Employment and Total Labor Force data.
filename = datapath + "/BLSEmploymentData.txt"

f1 = open(filename, "w")
f1.write("{}\t{}\t{}\t{}\n".format("CBSA","UnemRate","TotalEmp","TotalLabor"))

for index, row in hdata.iterrows():
    f1.write("{}\t{}\t{}\t{}\n".format(index, row['UnemRate'],row['TotalEmp'],row['TotalLabor']))
f1.close() 
