import streamlit as st
import pandas as pd
import requests
import json
import numpy as np



def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


# loading test dataset

def load_dataset(store_ids,test, store):

    # merge test dataset + store
    df_test = pd.merge(test, store, how='left', on='Store')
    
    # choose store for prediction
    df_test = df_test[df_test['Store'].isin(store_ids)]
    
    if not df_test.empty:
        # remove closed days
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop('Id', axis=1)

        # convert Dataframe to json
        data = json.dumps(df_test.to_dict(orient='records'))
    return data

# Streamlit app code
def main():
    test = pd.read_csv('/Users/55329/Documents/3.Repos/Rossmann-sales/data/test.csv')
    store = pd.read_csv('/Users/55329/Documents/3.Repos/Rossmann-sales/data/store.csv')
    tab1, tab2 = st.tabs(['Slider','Multiselect'])
    with tab1:
        st.title('Sales Prediction App')
        
        col1, col2 = st.columns(2)
        
        with col1:
            store_ids = st.slider('Escolha as Lojas', value = [1,1115] )
            store_ids = np.arange(store_ids[0], store_ids[1]+1, 1)
        
        with col2:
            budget = st.slider('Percentual para Orçamento', 0,100,1)
            budget = budget/100
        
        if st.button('Predict '):
            predictions = get_predictions(load_dataset(store_ids, test, store))
            predictions['budget'] = budget*predictions['prediction']
            
            #Show Dataframe
            st.dataframe(predictions, use_container_width= True)
            
            #converter para excel
            csv = convert_df(predictions)
            
            # download
            st.download_button(
            label="Download CSV",
            data= csv,
            file_name='predictions.csv',
            mime='text/csv',     )       
            
    with tab2:
        st.title('Sales Prediction App')

        budget = st.slider('Percentual para Orçamento ', 0,100,1)
        budget = budget/100
        
        store_ids = st.multiselect('Escolha as Lojas',test['Store'].unique())
        if st.button('Predict'):
            predictions = get_predictions(load_dataset(store_ids, test, store))
            predictions['budget'] = budget*predictions['prediction']
            
            #Show Dataframe
            st.dataframe(predictions, use_container_width= True)
            
            #converter para excel
            csv = convert_df(predictions)
            
            # download
            st.download_button(
            label="Download CSV",
            data= csv,
            file_name='predictions.csv',
            mime='text/csv',
                        )

def get_predictions(data):
    # Calling the API
    url = 'http://localhost:5000/rossmann/predict'
    #url = 'https://rossmann-api-45ni.onrender.com/rossmann/predict'
    headers = {'Content-type': 'application/json'}

    r = requests.post(url, json=data, headers=headers)

    if r.status_code == 200:
        df_result = pd.DataFrame(r.json(), columns= r.json()[0].keys())
        df_result = df_result[['store','prediction']].groupby('store').sum().reset_index()
        return df_result
    else:
        return 'Error occurred during prediction.'


if __name__ == '__main__':
    main()
