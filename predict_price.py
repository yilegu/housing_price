import pandas as pd
import numpy as np
from os.path import join, dirname
from collections import defaultdict
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#Function To Read Data
def read_zillow_csv(filename, skip=7):
    df=pd.read_csv(filename)
    dfcopy = df.copy()
    df["County+State"] = df["RegionName"].str.upper() + df["State"]
    countystate_choices = df["County+State"].tolist()
    df=df.set_index('County+State')
    df=df.T[skip:]
    df['dates']=df.index
    df['dates']=pd.to_datetime(df['dates'])
    county_choices=defaultdict(list)
    for ind in range(len(dfcopy.State)):
        county_choices[dfcopy.loc[ind]['State']].append(dfcopy.loc[ind]['RegionName'])
    return (df, county_choices, countystate_choices)

#Function to Preprocess Data for Analysis
def organize_data(data, past, future):

    future = future  
    width = past
    length = len(data)-future-past
    y = data[past+future:]
    X=np.empty([length,width])
    for i in range(length):
        for j in range(width):
            X[i,j] = data[i+j]
    X2=np.empty([length+future+1,width])
    for i in range(length+future+1):
        for j in range(width):
            X2[i,j] = data[i+j]
    y = np.array(y)
    return X,X2, y

def error_analysis(ypred, ytrue):
    return np.mean(np.abs(ypred-ytrue)/ytrue)


file_name= 'data/County_Zhvi_AllHomes.csv'
file_name=(join(dirname(__file__), file_name))


zillow_df, county_choices, countystate_choices = read_zillow_csv(file_name, 7)
zillow_df = zillow_df.reindex(zillow_df['dates'])

k = 12 #Number of previous months to look at
h = 12 #To predict how many months from now
m = 200 # size of traning sets
error_dict = {} #For Error Analysis
price_dict ={}


for countystate in countystate_choices: #countystate_choices:
    if len(zillow_df[countystate]) == zillow_df[countystate].count():
        data=(zillow_df[countystate].values)
        X,X2,y= organize_data(data,k,h)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        regressor = LinearRegression(normalize=True)
        regressor.fit(X_train, y_train)
        error_dict[countystate]=error_analysis(regressor.predict(X_test),y_test)
        predict = regressor.predict(X2)
        price_dict[countystate]=predict
        

        
price_db = pd.DataFrame(price_dict)
price_db['dates'] = pd.date_range(start=pd.datetime(1998, 4, 1), end=pd.datetime(2018, 2, 1), freq='MS')
error_db = pd.DataFrame.from_dict(error_dict, orient='index')
error_db = error_db.transpose()
file_name_error= 'data/predict_error_new.csv'
file_name_error=(join(dirname(__file__), file_name_error))
error_db.to_csv(file_name_error)
file_name_price_withpredictions= 'data/Price_WithPredictions_new.csv'
file_name_price_withpredictions=(join(dirname(__file__), file_name_price_withpredictions))
price_db.to_csv(file_name_price_withpredictions)


    
