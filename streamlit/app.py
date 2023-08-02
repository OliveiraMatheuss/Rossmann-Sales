import streamlit as st
import pandas as pd
import requests
import json
import numpy as np
from typing import List, Union



def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


# loading test dataset

from typing import List
import pandas as pd
import json

def load_dataset(store_ids: List[int], test: pd.DataFrame, store: pd.DataFrame) -> str:
    """
    Carrega e prepara o conjunto de dados para a previsão de vendas.

    Esta função realiza as seguintes etapas:
    1. Realiza um merge entre o conjunto de dados de teste e as informações das lojas com base na coluna 'Store'.
    2. Filtra o conjunto de dados para incluir apenas as lojas cujos IDs estão presentes na lista de IDs fornecida.
    3. Remove os dias em que as lojas estavam fechadas ('Open' == 0) e as linhas com valores nulos na coluna 'Open'.
    4. Remove a coluna 'Id' do conjunto de dados.
    5. Converte o DataFrame resultante em formato JSON.

    Parâmetros:
        store_ids (list): Uma lista contendo os IDs das lojas que serão incluídas na previsão.
        test (DataFrame): O DataFrame contendo os dados de teste das vendas das lojas.
        store (DataFrame): O DataFrame contendo informações sobre as lojas.

    Retorna:
        str: Uma string contendo os dados filtrados e preparados no formato JSON.

    Exemplo:
        >>> store_ids = [1, 2, 3]
        >>> test_data = pd.read_csv('test.csv')
        >>> store_data = pd.read_csv('store.csv')
        >>> data_json = load_dataset(store_ids, test_data, store_data)
    """
    # Realiza o merge do conjunto de dados de teste com as informações das lojas
    df_test = pd.merge(test, store, how='left', on='Store')

    # Filtra o conjunto de dados para incluir apenas as lojas cujos IDs estão presentes na lista fornecida
    df_test = df_test[df_test['Store'].isin(store_ids)]

    if not df_test.empty:
        # Remove os dias em que as lojas estavam fechadas ('Open' == 0) e as linhas com valores nulos na coluna 'Open'
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]

        # Remove a coluna 'Id' do conjunto de dados
        df_test = df_test.drop('Id', axis=1)

        # Converte o DataFrame resultante em formato JSON
        data = json.dumps(df_test.to_dict(orient='records'))
    else:
        data = 'error'

    return data




# Streamlit app code
def main():
    """
    Função principal para o aplicativo de Previsão de Vendas.

    Esta função cria um aplicativo web usando o Streamlit com duas abas: 'Slider' e 'Multiselect'.
    Na aba 'Slider', os usuários podem selecionar um intervalo de IDs de lojas e um percentual de orçamento usando sliders.
    Após fazer as seleções, os usuários podem clicar no botão 'Prever' para obter previsões de vendas para as lojas selecionadas.
    Os resultados são exibidos em um DataFrame e podem ser baixados como um arquivo CSV.

    Na aba 'Multiselect', os usuários podem selecionar vários IDs de lojas em um menu suspenso e um percentual de orçamento usando um slider.
    Após fazer as seleções, os usuários podem clicar no botão 'Prever' para obter previsões de vendas para as lojas selecionadas.
    Os resultados são exibidos em um DataFrame e podem ser baixados como um arquivo CSV.

    Retorna:
        None
    """
    
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
            budget = st.slider('Percentual para Orçamento', 0,100,10)
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

from typing import List, Union
import pandas as pd
import requests

def get_predictions(data: str) -> Union[pd.DataFrame, str]:
    """
    Faz uma chamada para a API de previsão de vendas.

    Esta função envia os dados no formato JSON para a API da rota '/rossmann/predict'
    e recebe a resposta da API. Caso a resposta da API seja bem-sucedida (status_code == 200),
    os resultados de previsão são extraídos e retornados em um DataFrame contendo a soma das
    previsões para cada loja.

    Parâmetros:
        data (str): Uma string contendo os dados no formato JSON.

    Retorna:
        pandas.DataFrame: Um DataFrame contendo os resultados das previsões para cada loja,
                          com as colunas 'store' (ID da loja) e 'prediction' (previsão de vendas).

        str: Uma string de erro caso ocorra um problema durante a previsão.

    Exemplo:
        >>> data_json = '{"Store": 1, "DayOfWeek": 3, "Open": 1, "Promo": 0, "StateHoliday": "0", ...}'
        >>> result_df = get_predictions(data_json)
    """
    url = 'http://localhost:5000/rossmann/predict'
    #url = 'https://rossmann-api-45ni.onrender.com/rossmann/predict'
    headers = {'Content-type': 'application/json'}

    r = requests.post(url, json=data, headers=headers)

    if r.status_code == 200:
        df_result = pd.DataFrame(r.json(), columns=r.json()[0].keys())
        df_result = df_result[['store', 'prediction']].groupby('store').sum().reset_index()
        return df_result
    else:
        return 'Error occurred during prediction.'

if __name__ == '__main__':
    """
    Executa a função 'main' ao iniciar o script.
    
    Quando este script é executado diretamente (não como um módulo importado em outro script),
    o bloco de código dentro do 'if' é executado, o que chama a função 'main'.
    """
    main()


