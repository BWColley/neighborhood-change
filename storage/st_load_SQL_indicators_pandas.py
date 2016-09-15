
import pandas as pd
import os
import psycopg2

hostname = 'localhost'
username = 'postgres'
password = '1234'
database = 'GTU'

conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port="5432")

# save indicators table to a CSV file
filename = os.getcwd() + "/indicators.csv"

#load SQL indicators (select all fields * ) into DataFrame
sql = "select * from Indicators order by id;"
df = pd.read_sql(sql, conn, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)

#save dataframe to CSV
df.to_csv(filename, sep=',', na_rep='', float_format=None, columns=None, header=True, index=False, index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None)

print "The final indicators' CSV file has been created at "+filename + "!"
conn.close()