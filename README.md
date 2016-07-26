Overview:
The goal of this project is to analyse the Fannie Mae Single-Family Loan Performance Data. Fannie Mae release data for Acquisition and Performance of loans every quearter, we will be using this data to answer some questions. 

What question I am looking to answer?
We can look for answers to following questions - 
1. Figuring out which banks sold loans to Fannie Mae that were foreclosed on the most.
2. Figuring out trends in borrower credit scores.
3. Exploring which types of homes are foreclosed on most often.
4. Exploring the relationship between loan amounts and foreclosure sale prices
5. Predict the payment history of a borrower.
6. Figure out a score for each loan at acquisition time.
7. Predict whether a loan will be foreclosed on in the future
8. Predict if a bank should have issued the loan.
9. Figure patterns in data at state or zip code level.

Some of the questions are focused on storytelling whereas some are good for operational viewpoint.

What question I want to answer?
"Predict whether a loan will be foreclosed on in the future."
This is the single most relevant question in terms of business if we need to find an answer.

There are other relevant questions as well - "Figure patterns in data at state or zip code level", "Predict if a bank should have issued the loan". I am currently working on these two questions.

What data did I use?
I used the Fannie Mae Single-Family Loan Performance Data(http://www.fanniemae.com/portal/funding-the-market/data/loan-performance-data.html). The data is a year old from current date.

Where I got the data?
The datasets are located at :https://loanperformancedata.fanniemae.com/lppub/index.html
To acquire the data one shall register with Fannie Mae.

How was the data sampled?
Data from 2012 to 2015 was used in the project rather than using data from early 2000. The reason for this being that the later years have more data than prior years as the data gets accumulated over years.

What is the data pipeline?
There are three stages in the data pipeline:
Data Gathering : Collect data from Fannie Mae and process the data.
Data Transformation: Transform the downloaded data by adding new features to the training data.
Data Processing : Use pre-processed training data and feed to the model.

How was the data preprocessed?
The data from Fannie Mae comes as set of text files. These text files are processed to combine Acquisition and Performance Data. 

Was there any data transformation?
Yes, the Acquisition dataset was transformed to add new columns - 
"foreclosure_status" to know if the loan was foreclosed
"performance_count" to know how many times the payment has been made for the loan.
"first_payment_date" split into "first_payment_month", "first_payment_year" 
"origination_date" split into "origination_month","origination_year"
columns ["channel","seller","first_time_homebuyer","loan_purpose","property_type","occupancy_status","property_state","product_type"] were changed from strings to category variables.

How did I explore the data?
I am not interactively exploring the data so I read the resources available online with Fannie Mae - 
Overview(http://www.fanniemae.com/portal/funding-the-market/data/loan-performance-data.html)
Glossary of Useful Terms(https://loanperformancedata.fanniemae.com/lppub-docs/lppub_glossary.pdf)
FAQS(https://loanperformancedata.fanniemae.com/lppub-docs/lppub_faq.pdf)
Columns in Data Acquired(https://loanperformancedata.fanniemae.com/lppub-docs/lppub_file_layout.pdf)
Sample Acquisition File(https://loanperformancedata.fanniemae.com/lppub-docs/acquisition-sample-file.txt)
Sample Performance File(https://loanperformancedata.fanniemae.com/lppub-docs/performance-sample-file.txt)

What model did I use?
We are looking to clasifiy if a loan acquired by Fannie Mae will go for foreclosure or not. This is a binary classification task and therefore we will use Logistic Regression as it is quick and uses less memory. We can also use RandomForest Classifier but that would need lots of resources.

How did you fit the model?
Will be using 3 fold cross validation to aavoid overfit.

How did you validated the model?
The evaluation model uses Precision Recall as a quality metrics.
False Negatives:0.2635561160151324
False Positives:0.33669903448739996

What next steps I would take with this project?
I am working on the below questions - 
Predict if a bank should have issued the loan?
Figure patterns in data at state or zip code level?