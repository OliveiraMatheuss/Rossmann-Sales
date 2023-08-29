# Rossmann.get_prediction
Realiza a previsão de vendas usando o modelo treinado

### Parâmetros:

   **model:** O modelo treinado a ser utilizado para a previsão

   **original_data (pandas.DataFrame):** O DataFrame original com os dados de entrada.

   **test_data (pandas.DataFrame):** O DataFrame contendo os dados preparados para a previsão
### Retorna:

    str: Uma string contendo o DataFrame com as previsões de vendas em formato JSON.

```python
    def get_prediction(self, model, original_data, test_data):
        
        
        #prediction
        pred = model.predict(test_data)
        
        # join pred into the original data
        
        original_data['prediction'] = np.expm1(pred)
        
        return original_data.to_json(orient= 'records', date_format= 'iso')

```