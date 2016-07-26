import os
import pandas as pd 
import numpy as np
import settings as st

'''
******************** STAGE 2: DATA CLEANING AND TRANSFORMATION ***************

Function to counts number of performance rows for each Loan Id.
counts dictionary: get the count of id and their count of occurance
'''

def count_performance_rows():
	foreclosure_counts={}
	# read data from files
	# NOTE: Opening a file handler to read rather than Pandas.
	# Reason : We want to re
	with open(os.path.join(st.PROCESSED_DIR,"Performance.csv"),"r") as f:
		for i,line in enumerate(f):
			if i==0:
				continue
			loan_id,date=line.split(",")
			loan_id=int(loan_id)
			if loan_id not in foreclosure_counts:
				foreclosure_counts[loan_id]= {
                    "foreclosure_status": False,
                    "performance_count": 0
                } # initialize dict
			
			foreclosure_counts[loan_id]["performance_count"]+=1
			if len(date.strip())>0:
				foreclosure_counts[loan_id]["foreclosure_status"]=True
	return foreclosure_counts

'''
Function to extract values from the dictionary if a loan_id and a key are passed in
This function will enable us to assign a foreclosure_status value and a performance_count value to each row in the Acquisition data.
'''
def get_summary_of_performance(loan_id,key,foreclosure_count_dictionary):
	#The get method on dictionaries returns a default value if a key isn’t found.
	summary_value=foreclosure_count_dictionary.get(loan_id,{ 
		"foreclosure_status": False,
        "performance_count": 0
        })
	return summary_value[key]

'''
This step will involve:

A. data transformation -
- Converting all columns to numeric.
- Filling in any missing values.
- Assigning a performance_count and a foreclosure_status to each row.
- Removing any rows that don’t have a lot of performance history (where performance_count is low).

B. data cleaning - 
This will prepare training dataset that can be used in a machine learning algorithm.
There are few different category codes, like R, S, that will be converted to 1 , 2.
For columns that contain dates we will split them into 2 columns - Month , Year

'''

def data_transform(acquisition,counts):
	# add "foreclosure_status" column in acquisition dataframe by getting the values from the counts dictionary
	acquisition["foreclosure_status"]=acquisition["id"].apply(lambda x: get_summary_of_performance(x,"foreclosure_status",counts))
	
	# add "performance_count" column in acquisition dataframe by getting the values from the counts dictionary.
	acquisition["performance_count"]=acquisition["id"].apply(lambda x: get_summary_of_performance(x,"performance_count",counts))
	
	# convert following columns to int - These are category variables
	#["channel","seller","first_time_homebuyer","loan_purpose","property_type","occupancy_status","property_state","product_type"]
	string_columns = ["channel","seller","first_time_homebuyer","loan_purpose","property_type","occupancy_status","property_state","product_type"]
	for column in string_columns:
		acquisition[column]=acquisition[column].astype("category").cat.codes	

	# convert date values - "first_payment_date" and "origination_date"
	for date in ["first_payment","origination"]:
		cols="{}_date".format(date)
		acquisition["{}_month".format(date)]= pd.to_numeric(acquisition[cols].str.split('/').str.get(0))
		acquisition["{}_year".format(date)] = pd.to_numeric(acquisition[cols].str.split('/').str.get(1))

	acquisition = acquisition.fillna(-1)
	acquisition = acquisition[acquisition["performance_count"] > st.MINIMUM_TRACKING_QUARTERS]
	return acquisition
		
'''
Read the Acquisition dataset
'''
def read():
    acquisition = pd.read_csv(os.path.join(st.PROCESSED_DIR, "Acquisition.csv"))
    return acquisition	

'''
write the training dataset to train.csv
'''
def write(acquisition):
	acquisition.to_csv(os.path.join(st.PROCESSED_DIR, "train.csv"),index=False)

if __name__=="__main__":
	acquisition=read()
	counts=count_performance_rows()
	acquisition=data_transform(acquisition,counts)
	write(acquisition)






