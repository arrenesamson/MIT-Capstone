# loading all the libraries necessary

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Bar, Gauge
from pyecharts import options as opts
import streamlit.components.v1 as components
from pyecharts.globals import ThemeType
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode,GridUpdateMode
import os
import streamlit_authenticator as stauth


import functions as func

def dashboard():
    ##########Header
    st.write(f"""
        # Dashboard
            """)
    ############################this function will predict all the csv in the df predict folder##########################
    file_list = []
    path = r'data_predict/' 
    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_path = os.path.join(path, file)
            file_list.append(file_path)
    file_list
    print(file_list)
    dfs = []
    for path in file_list:
                                    # df = pd.read_csv(os.path.join(path, path))
        df = pd.read_csv(path)
        df = func.predict_given_df(df)   #predicting the dataset
        dfs.append(df)
       
    concat_df = pd.concat(dfs, ignore_index=True)
    
    result = concat_df.groupby(['Year Graduated','predicted_response']).agg(['count']).reset_index()
    #grouping the employable and unemployable and trying to feed into the graph
    
    employed = []
    unemployed = []
    total_empolyable = 0
    total_count = 0
    
    
    for year in set(result['Year Graduated']):
        
        count_employed = result[(result['Year Graduated'] == year) & (result['predicted_response'] == 'Employable')]['Course/Major']
        count_unemployed = result[(result['Year Graduated'] == year) & (result['predicted_response'] == 'Less Employable')]['Course/Major']
        if count_employed['count'].values.size> 0:
            employed.append(int(count_employed['count'].values[0]))
            total_empolyable += int(count_employed['count'].values[0])
            total_count += int(count_employed['count'].values[0])
            
        else:
            employed.append(0)
        
        if count_unemployed['count'].values.size>0 :
            unemployed.append(int(count_unemployed['count'].values[0]))
            total_count += int(count_unemployed['count'].values[0])
        else:
            unemployed.append(0)
            
        years = set(result['Year Graduated'])
    
    # print(max(employed), max(unemployed))
    # print(len(years),len(employed), len(unemployed))
    
    # print(result.columns)
    # print(concat_df)
    
    
    col1, col2 = st.columns([10,2],gap = 'small')
    
    c = (Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
     
    .add_xaxis(list(years),)
    .add_yaxis('Employable', employed, color='#64cff6')
    .add_yaxis("Less Employable", unemployed, color="#706e97")
    # .add_xaxis(["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"],)
    # .add_yaxis('Employed', random.sample(range(100),12),color='#64cff6')
    # .add_yaxis("Unemployed", random.sample(range(100), 12),color="#706e97")
    .set_global_opts(title_opts=opts.TitleOpts(title="Analytics"))
    .render_embed() # generate a local HTML file
    )
    # with col1:
    components.html(c,height=500)
    
    
        
    percentage = total_empolyable/total_count *100
    g = (Gauge(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        #  .add('Percentage',data_pair={'df':23,"ds":45},split_number=10,)
        .add('Percentage',data_pair=[["Employable percentage", round(percentage,2)]],split_number=10,radius='85%',max_=100)    
        .set_global_opts(title_opts=opts.TitleOpts(title=f"Total Employable: {total_empolyable} out of {total_count}"))
        .render_embed()
        )

    # with col2:
    components.html(g,width=1000, height=1000)
        
def predict():
    st.write(f"""
        # Predict
            """)
    ###########HEader
    df_upload = st.file_uploader('file',label_visibility='hidden')
    csv_name = st.text_input("Name your dataset")
    if df_upload:
        if csv_name:
            df_upload = pd.read_csv(df_upload)
            df_upload.to_csv(f"data_predict\{csv_name}.csv")
    
def result():
    st.write(f"""
        # Result
            """)
    
    file_list = func.read_file_make_list(r'data_predict/' , 'csv')
    
    modified_time_list = [os.path.getmtime(files) for files in file_list]
    
    now = int(datetime.datetime.now().timestamp())
    start_ts = now - 3 * 30 * 24 * 60 * 60

    @st.cache(allow_output_mutation=True)
    def make_data():
        df = pd.DataFrame(
            {
                
                "upload_time": modified_time_list,                
                "file name": [list(file.split('\\'))[-1] for file in file_list],  # [np.random.choice(["SBA-Batch 2022", "SBA-Batch 2022"]) for i in range(5)]  file_list
                "path" : file_list,
                "prediction": [np.random.choice(["View Result"]) for i in range(len(file_list))], 
                
            }
        )
        # df["cost"] = round(df.amount * df.price, 2)
        df.insert(
            0,
            "datetime",
            df.upload_time.apply(lambda ts: datetime.datetime.fromtimestamp(ts)),
        )

        return df.sort_values("upload_time").drop("upload_time", axis=1)


    
    BtnCellRenderer = JsCode('''
    class BtnCellRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `
            <span>
                <button id='click-button' 
                    class='btn-simple' 
                    style='color: ${this.params.color}; background-color: ${this.params.background_color}'>Predict</button>
            </span>
        `;

            this.eButton = this.eGui.querySelector('#click-button');

            this.btnClickedHandler = this.btnClickedHandler.bind(this);
            this.eButton.addEventListener('click', this.btnClickedHandler);

        }

        getGui() {
            return this.eGui;
        }

        refresh() {
            return true;
        }

        destroy() {
            if (this.eButton) {
                this.eGui.removeEventListener('click', this.btnClickedHandler);
            }
        }

        btnClickedHandler(event) {
            if (confirm('Are you sure you want to CLICK?') == true) {
                if(this.params.getValue() == 'clicked') {
                    this.refreshTable('');
                } else {
                    this.refreshTable('clicked');
                }
                    console.log(this.params);
                    console.log(this.params.getValue());
                }
            }

        refreshTable(value) {
            this.params.setValue(value);
        }
    };
    ''')

    df = make_data()
    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(editable=True)
    grid_options = gb.build()

    grid_options['columnDefs'].append({
        "field": "clicked",
        "header": "Prediction",
        "cellRenderer": BtnCellRenderer,
        "cellRendererParams": {
            "color": "red",
            "background_color": "black",
        },
    })

    

    response = AgGrid(df,
                    theme="streamlit",
                    key='table1',
                    gridOptions=grid_options,
                    allow_unsafe_jscode=True,
                    fit_columns_on_grid_load=True,
                    reload_data=False,
                    try_to_convert_back_to_original_types=False
                    )

    
    try:
        st.write(response['data'][response['data'].clicked == 'clicked'])
        
        selected_path_list = list((response['data'][response['data'].clicked == 'clicked']['path']).to_frame()['path'])
        df_to_predict_path = selected_path_list[0]
        
        pred_df = func.predict_df(df_to_predict_path)
        
        
    except:
        st.write('Nothing was clicked')
        


def about():
    st.write(f"""
        # About - Ensemble Learning
        
            """)
    st.write(f""""
             Definition: — Ensemble learning is a machine learning paradigm where multiple models (often called “weak learners”) are trained to solve the same problem and combined to get better results. The main hypothesis is that when weak models are correctly combined, we can obtain more accurate and/or robust models.
             """
    )
    st.image("ensemble.jpg",width=500,output_format='JPG')
    st.write(f"""
             ### 1. BAGGING

            · Bagging stands for Bootstrap Aggregation.

            · In real-life scenarios, we don’t have multiple different training sets on which we can train our model separately and at the end combine their result. Here, bootstrapping comes into the picture.

            · Bootstrapping is a technique of sampling different sets of data from a given training set by using replacement. After bootstrapping the training dataset, we train the model on all the different sets and aggregate the result. This technique is known as Bootstrap Aggregation or Bagging.
             
              ### 2. Boosting

           · Boosting models fall inside this family of ensemble methods.

            · Boosting, initially named Hypothesis Boosting, consists of the idea of filtering or weighting the data that is used to train our team of weak learners, so that each new learner gives more weight or is only trained with observations that have been poorly classified by the previous learners..

            · By doing this our team of models learns to make accurate predictions on all kinds of data, not just on the most common or easy observations. Also, if one of the individual models is very bad at making predictions on some kind of observation, it does not matter, as the other N-1 models will most likely make up for it. 
             
             """
    )