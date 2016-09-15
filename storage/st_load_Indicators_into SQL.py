"""
This code will :
  1) create the indicator table in PostgreSQL database
  2) read and insert top 300 MSAs into table
  3) load indicator CSVs into indicators table and set NULL value for missing data
Ind1 to 10-->: Violent_Crime_Rate,Murder_Manslaughter,Rape,Robbery,Aggravated_Assault,Property_Crime_Rate,Burglary,Larceny_Theft,Motor_Vehicle_Theft,Total_Crime_Rate
Ind 11 to 14-->: Median_Gross_Rent,Median_Monthly_Mortgage,Rent_Burden,Mortgage_Burden
Ind 15 : Income Change 2012 to 2014
Ind 16 to 18: Median_Age_of_Men,Median_Age_of_Women,Median_Age
Ind 19: Median_Household_Income
Ind 20 to 24: Single_Men_Population,Single_Women_Population,Ratio_of_Single_Men_to_Single_Women,Population_Percent_of_Single_Men,Population_Percent_of_Single_Women
Ind 25 : population
Ind 26 : Education: edu_average_scale_score
Ind 27 to 31: Food: PCT_LACCESS_POP10,PCT_LACCESS_LOWI10,PCT_LACCESS_CHILD10,PCT_LACCESS_SENIORS10,PCT_LACCESS_HHNV10,Population_food
ind 32 to 34 : Event_mPMT,Fatalities_mPMT,Injuries_mPMT
Ind 35 to 37 : Walk_Score,Transit_Score,Bike_Score
Ind 38 to 40: BLS employment

"violent_crime_rate","murder_manslaughter","rape","robbery","aggravated_assault","property_crime_rate","burglary","larceny_theft","motor_vehicle_theft","total_crime_rate","median_gross_rent","median_monthly_mortgage","rent_burden","mortgage_burden","income_change_2012_to_2014","median_age_of_men","median_age_of_women","median_age","median_household_income","single_men_population","single_women_population","ratio_of_single_men_to_single_women","population_percent_of_single_men","population_percent_of_single_women","population","event_mpmt","fatalities_mpmt","injuries_mpmt","walk_score","transit_score","bike_score","unemploymentrate","employment","laborforce","employedshare","more_singles_sex","pop_category","safe_level","walkbility"
"""
import os
import psycopg2
import csv
import pandas as pd

def is_number(s):
    try:
        float(s)
        return str(s)
    except ValueError:
        return 'null'

def main():

    #Make sure you change next 4 lines to your database setup correctly before running
    hostname = 'localhost'
    username = 'postgres'
    password = '1234'
    database = 'gtu'

    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port="5432")

    cur = conn.cursor()
    # Drop Indocators table if it exists
    cur.execute('DROP TABLE IF EXISTS Indicators;')

    #Create Indicators table
    cur.execute('''CREATE TABLE Indicators
            (ID INT PRIMARY KEY  NOT NULL,
            CBSA  CHAR(5),
            MSA_Name  CHAR(100),
            Violent_Crime_Rate float,
            Murder_Manslaughter float,
            Rape float,
            Robbery float,
            Aggravated_Assault float,
            Property_Crime_Rate float,
            Burglary float,
            Larceny_Theft float,
            Motor_Vehicle_Theft float,
            Total_Crime_Rate float,
            Median_Gross_Rent float,
            Median_Monthly_Mortgage float,
            Rent_Burden float,
            Mortgage_Burden float,
            Income_Change_2012_to_2014 float,
            Median_Age_of_Men float,
            Median_Age_of_Women float,
            Median_Age float,
            Median_Household_Income float,
            Single_Men_Population float,
            Single_Women_Population float,
            Ratio_of_Single_Men_to_Single_Women float,
            Population_Percent_of_Single_Men float,
            Population_Percent_of_Single_Women float,
            population float,

            edu_average_scale_score float,

            PCT_LACCESS_POP10 float,
            PCT_LACCESS_LOWI10 float,
            PCT_LACCESS_CHILD10 float,
            PCT_LACCESS_SENIORS10 float,
            PCT_LACCESS_HHNV10 float,
            Event_mPMT float,
            Fatalities_mPMT float,
            Injuries_mPMT float,
            Walk_Score float,
            Transit_Score float,
            Bike_Score float,
            unemploymentrate float,
            employment float,
            laborforce float,
            CompositeScore float,
            Memo CHAR(100));''')
    print "Indicators created successfully"

    # Load the Top 300 MSAs into Indicators table.  The individual indicator will be loaded after.
    with open(os.getcwd() +'/MSATop300.txt', 'r') as f:
        next(f) # skip headings
        reader=csv.reader(f,delimiter='\t')
        n=0
        for id,name in reader:
            if not (id=='' or name==''):
                sql="INSERT INTO Indicators (ID,CBSA,MSA_Name) VALUES ("+ str(n) + ",'" + id + "','" + name.replace("'","''") +"');"
                cur.execute(sql)
                n += 1
    f.close()
    print "Top 300 MSAs Inserted successfully"

    # Now loading the indicators into each MSA
    datapath = os.path.join(os.getcwd(), "data")
    # 1 to 10) load FBI crime_rate.txt ......
    filename = datapath + "/crime_rate.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        n=0
        for id,Violent_Crime_Rate,Murder_Manslaughter,Rape,Robbery,Aggravated_Assault,Property_Crime_Rate,Burglary,Larceny_Theft,Motor_Vehicle_Theft,Total_Crime_Rate in reader:
            sql="UPDATE Indicators SET Violent_Crime_Rate = " + is_number(Violent_Crime_Rate) + ","
            sql=sql+"Murder_Manslaughter = " + is_number(Murder_Manslaughter) + ","
            sql+="Rape = " + is_number(Rape) + ","
            sql+="Robbery = " + is_number(Robbery) + ","
            sql+="Aggravated_Assault = " + is_number(Aggravated_Assault) + ","
            sql+="Property_Crime_Rate = " + is_number(Property_Crime_Rate) + ","
            sql+="Burglary = " + is_number(Burglary) + ","
            sql+="Larceny_Theft = " + is_number(Larceny_Theft) + ","
            sql+="Motor_Vehicle_Theft = " + is_number(Motor_Vehicle_Theft) + ","
            sql+="Total_Crime_Rate = " + is_number(Total_Crime_Rate)
            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()

    # 11 to 14) load ACS housing_cost.txt ......
    filename = datapath + "/housing_cost.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        n=0
        for id,Median_Gross_Rent,Median_Monthly_Mortgage,Rent_Burden,Mortgage_Burden in reader:
            sql="UPDATE Indicators SET Median_Gross_Rent = " + is_number(Median_Gross_Rent) + ","
            sql=sql+"Median_Monthly_Mortgage = " + is_number(Median_Monthly_Mortgage) + ","
            sql+="Rent_Burden = " + is_number(Rent_Burden) + ","
            sql+="Mortgage_Burden = " + is_number(Mortgage_Burden)

            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()

    # 15 load ACS income_change.txt ......
    filename = datapath + "/income_change.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        for id,Income_Change_2012_to_2014 in reader:
            sql="UPDATE Indicators SET Income_Change_2012_to_2014 = " + is_number(Income_Change_2012_to_2014)

            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()

    # 16 to 18) load ACS median_age.txt ......
    filename = datapath + "/median_age.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        n=0
        for id,Median_Age_of_Men,Median_Age_of_Women,Median_Age in reader:
            sql="UPDATE Indicators SET Median_Age_of_Men = " + is_number(Median_Age_of_Men) + ","
            sql=sql+"Median_Age_of_Women = " + is_number(Median_Age_of_Women) + ","
            sql+="Median_Age = " + is_number(Median_Age)
            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()


    # 19 load ACS median_income.txt ......
    filename = datapath + "/median_income.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        for id,Median_Household_Income in reader:
            sql="UPDATE Indicators SET Median_Household_Income = " + is_number(Median_Household_Income)

            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()

    # 20 to 24) load ACS Single_population.txt ......
    filename = datapath + "/single_population.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        n=0
        for id,Single_Men_Population,Single_Women_Population,Ratio_of_Single_Men_to_Single_Women,Population_Percent_of_Single_Men,Population_Percent_of_Single_Women in reader:
            sql="UPDATE Indicators SET Single_Men_Population = " + is_number(Single_Men_Population) + ","
            sql=sql+"Single_Women_Population = " + is_number(Single_Women_Population) + ","
            sql=sql+"Ratio_of_Single_Men_to_Single_Women = " + is_number(Ratio_of_Single_Men_to_Single_Women) + ","
            sql+="Population_Percent_of_Single_Men = " + is_number(Population_Percent_of_Single_Men) + ","
            sql+="Population_Percent_of_Single_Women = " + is_number(Population_Percent_of_Single_Women)
            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()

    # 25 load ACS population300.txt ......
    filename = datapath + "/population300.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        for id,population in reader:
            sql="UPDATE Indicators SET population = " + is_number(population)

            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()

    # 26 load Education_msa.txt ......
    filename = datapath + "/Education_msa.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        for id,edu_average_scale_score in reader:
            sql="UPDATE Indicators SET edu_average_scale_score = " + is_number(edu_average_scale_score)

            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()


    # 27 to 31 load Food_msa.txt ......
    filename = datapath + "/Food_msa.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        n=0
        for id,PCT_LACCESS_POP10,PCT_LACCESS_LOWI10,PCT_LACCESS_CHILD10,PCT_LACCESS_SENIORS10,PCT_LACCESS_HHNV10,dump in reader:
            sql="UPDATE Indicators SET PCT_LACCESS_POP10 = " + is_number(PCT_LACCESS_POP10) + ","
            sql=sql+"PCT_LACCESS_LOWI10 = " + is_number(PCT_LACCESS_LOWI10) + ","
            sql=sql+"PCT_LACCESS_CHILD10 = " + is_number(PCT_LACCESS_CHILD10) + ","
            sql=sql+"PCT_LACCESS_SENIORS10 = " + is_number(PCT_LACCESS_SENIORS10) + ","
            sql+="PCT_LACCESS_HHNV10 = " + is_number(PCT_LACCESS_HHNV10)
            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()



    # 32 to 34 load FTA_by_CBSA.txt ......
    filename = datapath + "/FTA_by_CBSA.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        n=0
        for id,Event_mPMT,Fatalities_mPMT,Injuries_mPMT in reader:
            sql="UPDATE Indicators SET Event_mPMT = " + is_number(Event_mPMT) + ","
            sql=sql+"Fatalities_mPMT = " + is_number(Fatalities_mPMT) + ","
            sql+="Injuries_mPMT = " + is_number(Injuries_mPMT)
            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()


    # 35 to 37 load Walk Walk_by_MSA.txt ......
    filename = datapath + "/Walk_by_MSA.txt"
    with open(filename, 'r') as f:
        #next(f) # skip headings

        reader=csv.reader(f,delimiter='\t')
        headers = reader.next()
        n=0
        for id,Walk_Score,Transit_Score,Bike_Score in reader:
            sql="UPDATE Indicators SET Walk_Score = " + is_number(Walk_Score) + ","
            sql=sql+"Transit_Score = " + is_number(Transit_Score) + ","
            sql+="Bike_Score = " + is_number(Bike_Score)
            sql+=" WHERE CBSA='" + str(id) + "';"
            cur.execute(sql)

    f.close()




    # 38 - 40) Indicator BLS Unemployment and Total Employment
    filename = datapath + "/BLSEmploymentData.txt"
    with open(filename, 'r') as f:
        next(f) # skip headings
        reader=csv.reader(f,delimiter='\t')
        n=0
        for id,unemploymentrate,employment,laborforce in reader:
            #if not (id=='' or rate=='' or emp=='' or labor==''):
            sql="UPDATE Indicators SET unemploymentrate = " + is_number(unemploymentrate) + ",employment = " + is_number(employment) + ",laborforce = " + is_number(laborforce) + " WHERE CBSA=case '" + str(id) + "' when '31100' then '31080' when '71650' then '14460' when '77200' then '39300' when '73450' then '25540' when '26000' then '23420' when '75700' then '35300' when '78100' then '44140' when '14060' then '14010' when '26180' then '46520' when '79600' then '49340' when '76750' then '38860' when '42060' then '42200' when '74950' then '31700' when '76450' then '35980' when '72500' then '17200' when '72400' then '15540' when '70900' then '12700' when '78400' then '45860' when '70750' then '12620' else '" + str(id) + "' end;"
            cur.execute(sql)

    f.close()
    conn.commit()

    print "All indicators have been inserted into SQL database!"

    # save indicators table to a CSV file
    filename = os.getcwd() + "/indicators.csv"
    sql = "select * from Indicators order by id;"
    newdf=pd.read_sql(sql, conn, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
    newdf.to_csv(filename, sep=',', na_rep='', float_format=None, columns=None, header=True, index=False, index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None)
    print "The final indicators' CSV file has been created at "+filename + "!"


    conn.close()

if __name__ == '__main__':
    main()