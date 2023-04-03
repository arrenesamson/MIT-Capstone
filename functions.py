import pandas as pd
import pickle
import streamlit as st
import os


#pages will be included to functions
def predict_df(path, model_path = 'model/my_pipeline.pkl' ):
    #loading the dataset
    df1=pd.read_csv(path)
    
    #selecting only the column in the trained model
    cols  = ['Year Graduated', 'Graduation Term', 'Course/Major',"What honor's have you received during college days?",'Did you received any Latin Honors after Graduation?',
'Are you involved in any Student Organization during your college days?','How many academic award certifications have you received during your college days?',
'How many technical certifications have you received during your college days?','Do you have any portfolio related to your course/ major when you applied for your first job?',
'Technical Skills (Please select the option that best describes your skill set after graduation)']
    
    df1 = df1[cols]
    
    for col in df1.columns:
        df1[col] = df1[col].astype('str')
        df1[col] = df1[col].astype('category')
    
    
    #loading the pickle model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        
    preds = model.predict(df1)
        
    # df1['predicted_response'] = preds
    new_col = pd.Series(preds, name='predicted_response')  # create a new column as a pandas Series
    df1.insert(loc=0, column='predicted_response', value=new_col)  # use the insert method to add the new column at index 0

    
    st.write(df1)
    
def predict_given_df(df1, model_path = 'model/my_pipeline.pkl' ):
    #selecting only the column in the trained model
    cols  = ['Year Graduated', 'Graduation Term', 'Course/Major',"What honor's have you received during college days?",'Did you received any Latin Honors after Graduation?',
'Are you involved in any Student Organization during your college days?','How many academic award certifications have you received during your college days?',
'How many technical certifications have you received during your college days?','Do you have any portfolio related to your course/ major when you applied for your first job?',
'Technical Skills (Please select the option that best describes your skill set after graduation)']
    
    df1 = df1[cols]
    
    for col in df1.columns:
        df1[col] = df1[col].astype('str')
        df1[col] = df1[col].astype('category')
    
    
    #loading the pickle model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        
    preds = model.predict(df1)
        
    # df1['predicted_response'] = preds
    new_col = pd.Series(preds, name='predicted_response')  # create a new column as a pandas Series
    df1.insert(loc=0, column='predicted_response', value=new_col)  # use the insert method to add the new column at index 0

    
    return df1

def read_file_make_list(path,format):
    
    file_list = []
    path = r'data_predict/'
    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_path = os.path.join(path, file)
            file_list.append(file_path)
            
    return file_list

def read_predict (file_path):
    df = pd.read_csv(file_path)
    
    return df

    

