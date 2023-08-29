# Rosmann.feature_engineering


Realiza a engenharia de características no DataFrame df

### Parâmetros:
    df (pandas.DataFrame): O DataFrame contendo os dados a serem processados

### Retorna:
            pandas.DataFrame: O DataFrame com as novas características adicionadas.


```python
def feature_engineering(self, df):
        

        
        ### 2.4. Feature Engineering
        # year
        df['year'] = df['date'].dt.year

        # month
        df['month'] = df['date'].dt.month

        # day
        df['day'] = df['date'].dt.day

        # week of year
        df['week_of_year'] = df['date'].dt.isocalendar().week

        # year week
        df['year_week'] = df['date'].dt.strftime( '%Y-%W' )

        # competition since
        df['competition_since'] = df.apply( lambda x: datetime.datetime( year=x['competition_open_since_year'], month=x['competition_open_since_month'],day=1 ), axis=1 )
        df['competition_time_month'] = ( ( df['date'] - df['competition_since'] )/30 ).apply( lambda x: x.days ).astype( int )

        # promo since
        df['promo_since'] = df['promo2_since_year'].astype( str ) + '-' + df['promo2_since_week'].astype( str )
        df['promo_since'] = df['promo_since'].apply( lambda x: datetime.datetime.strptime( x + '-1', '%Y-%W-%w' ) - datetime.timedelta( days=7 ) )
        df['promo_time_week'] = ( ( df['date'] - df['promo_since'] )/7 ).apply( lambda x: x.days ).astype( int )

        # assortment
        df['assortment'] = df['assortment'].apply( lambda x: 'basic' if x == 'a' else 'extra' if x == 'b' else 'extended' )

        # state holiday
        df['state_holiday'] = df['state_holiday'].apply( lambda x: 'public_holiday' if x == 'a' else 'easter_holiday' if x == 'b' else 'christmas' if x == 'c' else 'regular_day' )

        ## 3.0. PASSO 03 - FILTRAGEM DE VARIÁVEIS
        ### 3.1. Filtragem das Linhas
        # Quero apenas dados onde a loja esta aberta e que valor de vendas seja maior que 0

        ### 3.2. Selecao das Colunas
        
        # Excluir colunas na qual eu não terei durante o processo de previsão
        cols_drop = ['open', 'promo_interval', 'month_map']
        df = df.drop( cols_drop, axis=1 )
        return df
```