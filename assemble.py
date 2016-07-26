import settings as st
import os
import pandas as pd

'''
*************** STAGE 1: DATA GATHERING ***********************

Assemble all the different .txt files (Aquisition and Performance) into 2 files :
We’ll first need to define the headers for each file
https://loanperformancedata.fanniemae.com/lppub-docs/lppub_file_layout.pdf
'''

HEADERS = {
    "Acquisition": [
        "id",
        "channel",
        "seller",
        "interest_rate",
        "balance",
        "loan_term",
        "origination_date",
        "first_payment_date",
        "ltv",
        "cltv",
        "borrower_count",
        "dti",
        "borrower_credit_score",
        "first_time_homebuyer",
        "loan_purpose",
        "property_type",
        "unit_count",
        "occupancy_status",
        "property_state",
        "zip",
        "insurance_percentage",
        "product_type",
        "co_borrower_credit_score"
    ],
    "Performance": [
        "id",
        "reporting_period",
        "servicer_name",
        "interest_rate",
        "balance",
        "loan_age",
        "months_to_maturity",
        "maturity_date",
        "msa",
        "delinquency_status",
        "modification_flag",
        "zero_balance_code",
        "zero_balance_date",
        "last_paid_installment_date",
        "foreclosure_date",
        "disposition_date",
        "foreclosure_costs",
        "property_repair_costs",
        "recovery_costs",
        "misc_costs",
        "tax_costs",
        "sale_proceeds",
        "credit_enhancement_proceeds",
        "repurchase_proceeds",
        "other_foreclosure_proceeds",
        "non_interest_bearing_balance",
        "principal_forgiveness_balance"
    ]
}

# We will now define the columns we want to keep. Since all we’re measuring on an ongoing basis about the loan is
# whether or not it was ever foreclosed on, we can discard many of the columns in the performance data. 
# We’ll need to keep all the columns in the acquisition data, though, because we want to maximize the 
# information we have about when the loan was acquired 

SELECT = {
    "Acquisition": HEADERS["Acquisition"],
    "Performance": [
        "id",
        "foreclosure_date"
    ]
}

def concatenate(prefix="Acquisition"):
    dir_files = os.listdir(st.DATA_DIR)
    full_file = []
    # concatenate all the files in the directory
    
    for f in dir_files:
        if f.startswith(prefix):
            read_file=pd.read_csv(os.path.join(st.DATA_DIR,f),sep='|',header=None, names = HEADERS[prefix], index_col=False, error_bad_lines=False)
            read_file=read_file[SELECT[prefix]]
            full_file.append(read_file)
        else:
            continue
    full_file=pd.concat(full_file,axis=0)
    
    test=full_file.head(5)
    # get shape of the file
    # print(full_file.shape)

    # convert the processed files - 
    full_file.to_csv(os.path.join(st.PROCESSED_DIR, "{}.csv".format(prefix)), index=False)

if __name__=="__main__":
    #concatenate("Acquisition")
    concatenate("Performance")






