import requests
import csv
import json
import os

#check if data folder exists
datapath = os.path.join(os.getcwd(), "data")


if not os.path.exists(datapath):
    os.makedirs(datapath)

#Save inital BLS data to ./data/BLSMetroData.txt for processing:
filename = datapath + "/BLSMetroData.txt"

f1 = open(filename, "w")
f1.write("{}\t{}\t{}\t{}\t{}\n".format("CBSA","BLSCODE","YEAR","MONTH","VALUE"))
headers = {'Content-type': 'application/json'}
BLSID=[]
MSAName=[]

# read and loop thru MSA list to get BLS data for each MSA:
with open(os.getcwd() +'/MSA_BLS_CODE300.txt', 'r') as f:
    next(f) # skip headings
    reader=csv.reader(f,delimiter='\t')
    for id,name in reader:
        code = 'LAU'+id+'0000000'
        BLSID.append(code)
        MSAName.append(name)

        # next two line to use API without BLS Key, up to 25 total API requests daily:
        #data = json.dumps({"seriesid": [code+'03',code+'04',code+'05',code+'06'],"startyear":"2004", "endyear":"2014"})
        #p = requests.post('http://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)

        # Next two line to use BLS API key for up to 500 request daily:
        # get a KEY at http://data.bls.gov/registrationEngine/
        data = json.dumps({"seriesid": [code+'03',code+'04',code+'05',code+'06'],"startyear":"2014", "endyear":"2014","registrationKey":"<<YOUR BLS API KEY HERE>>"})
        p = requests.post('http://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

        json_data = json.loads(p.text)

        for series in json_data['Results']['series']:
            seriesID = series['seriesID']
            blstype = seriesID[len(seriesID)-2:len(seriesID)]
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                print id[4:8]+'0' + '--' + blstype + ' -- ' + year+' -- ' + period +' -- ' + value
                f1.write("{}\t{}\t{}\t{}\t{}\n".format(id[4:8]+'0',blstype, year,period,value))
        #break


f.close()
f1.close()
