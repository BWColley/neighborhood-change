## Create GTU database for Capstone project

import psycopg2

#update next 3 lines for your sepcific setup:
hostname = 'localhost'
username = 'postgres'
password = '1234'

conn = psycopg2.connect(host=hostname, user=username, password=password, port="5432")
cur = conn.cursor()

cur.execute("BEGIN")
cur.execute("COMMIT")

#drop database GTU if exists
cur.execute("DROP DATABASE IF EXISTS GTU;")

#create new database GTU
cur.execute('CREATE DATABASE "GTU" OWNER postgres TABLESPACE = pg_default;')

conn.close()
print "The database GTU has been created!"
