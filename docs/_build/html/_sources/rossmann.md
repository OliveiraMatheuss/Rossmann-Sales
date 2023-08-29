# api.rossmann.Rossmann
# Documentação da Classe Rossmann

A classe Rossmann é usada para realizar a previsão de vendas utilizando um modelo treinado. Ela inclui métodos para limpeza e engenharia de características dos dados, preparação dos dados e previsão de vendas.

## Importações

```python
import inflection
import pandas as pd
import math
import datetime
import pickle
import numpy as np
```



## Classe Rossmann

Classe para realizar a previsão de vendas utilizando o modelo treinado da Rossmann.
Esta classe contém métodos para realizar a limpeza e engenharia de características dos dados,
preparar os dados para a previsão, e fazer a previsão de vendas usando o modelo treinado.

### Atributos:

**home_path (str):** O caminho para o diretório raiz do projeto.

**competition_distance_scaler (object):** O objeto do scalerilizado para escalonar a coluna 'CompetitionDistance'.

**competition_time_month_scaler (object):** O objeto do scaler utilizado para escalonar a coluna 'CompetitionTimeMonth'.

**promo_time_month_scaler (object):** O objeto do scaler utilizado para escalonar a coluna 'PromoTimeWeek'.

**year_scaler (object):** O objeto do scaler utilizado para escalonar a coluna 'Year'.

**store_type_encoder (object):** O objeto do encoder utilizado para codificar a coluna 'StoreType'.


### Métodos: 
| Método                                                         | Descrição                              |
|----------------------------------------------------------------|----------------------------------------|
| [Rosmann.data_cleaning(df)](data_cleaning.md)                                       | Realiza a limpeza dos dados            |
| [Rosmann.feature_engineering(df)](feature_engineering.md)                                 | Realiza a engenharia de características|
| [Rosmann.data_preparation(df)](data_preparation.md)                                     | Prepara os dados para a previsão       |
|[Rossmann.get_prediction(model, original_data, test_data)](get_prediction)        | Realiza a previsão de vendas           |
