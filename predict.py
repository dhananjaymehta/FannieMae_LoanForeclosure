import os
import numpy as np 
import pandas as pd
import settings as st
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

'''
********************* STAGE 3: MAKING PREDICTION ************************

The training dataset is very unbalanced with very few loans foreclosed compared to the loans that
were not foreclosed. This would make a biased prediction.

Therefore to predict foreclosures correctly this imbalance needs to be accounted.

False Negative is more dangerous here than False Positive, as False Negative would indicate 
a risky loan being acquired.

Error Metric: FP / FN

Classifier : Logistic Regression (sklearn library) to classify the loan. The class needs to be
balanced as the dataset is biased to non-foreclosures. use : class_weight = balanced

OverFitting : Cross Validation (sklearn library) to counter OverFitting of model.

'''

def prediction_model(train):
	model=LogisticRegression(random_state=1,class_weight="balanced")
	
	predictors=train.columns.tolist()

	predictors = [p for p in predictors if p not in st.NON_PREDICTORS]

	predictions = cross_validation.cross_val_predict(model,train[predictors],train[st.TARGET],cv=st.CV_FOLDS)

	return predictions

def compute_error(target,predictions):
	return metrics.accuracy_score(target,predictions)

def compute_false_negatives(target,predictions):
	false_negatives=pd.DataFrame({"target":target,"predictions":predictions})
	neg_rate=false_negatives[(false_negatives["target"]==1) & (false_negatives["predictions"]==0)].shape[0]/(false_negatives[(false_negatives["target"]==1)].shape[0]+1)
	return neg_rate

def compute_false_positive(target,predictions):
	false_positives=pd.DataFrame({"target":target,"predictions":predictions})
	pos_rate=false_positives[(false_positives["target"]==0) & (false_positives["predictions"]==1)].shape[0]/(false_positives[(false_positives["target"]==0)].shape[0]+1)
	return pos_rate

def read():
	train=pd.read_csv(os.path.join(st.PROCESSED_DIR,"train.csv"))
	return train

if __name__=="__main__":
	train=read()
	train=train.drop(["origination_date","first_payment_date"],1)
	predictions=prediction_model(train)
	model_error=compute_error(train[st.TARGET],predictions)
	FN=compute_false_negatives(train[st.TARGET],predictions)
	FP=compute_false_positive(train[st.TARGET],predictions)
	print("Accuracy of the model:{}".format(model_error))
	print("False Negatives:{}".format(FN))
	print("False Positive:{}".format(FP))
