# Rosmann.data_preparation

Prepara os dados no DataFrame df para a previsão

### Parâmetros:
    df (pandas.DataFrame): O DataFrame contendo os dados a serem preparados
### Retorna:
            pandas.DataFrame: O DataFrame com os dados preparados para a previsão.

```python
def data_preparation(self, df):
        """

        """
        
        ## 5.1 Rescaling

        # competition distance
        df['competition_distance'] = self.competition_distance_scaler.fit_transform(df[['competition_distance']].values)

        # competition time month
        df['competition_time_month'] = self.competition_time_month_scaler.fit_transform( df[['competition_time_month']].values )

        # promo time week
        df['promo_time_week'] = self.promo_time_month_scaler.fit_transform( df[['promo_time_week']].values )

        # year
        df['year'] = self.year_scaler.fit_transform( df[['year']].values )

        ## 5.2 Transformacao
        ### 5.2.1 Encoding
        
        # state_holiday - One Hot Encoding
        df = pd.get_dummies( df, prefix=['state_holiday'], columns=['state_holiday'] )

        # store_type - Label Encoding
        
        df['store_type'] = self.store_type_encoder.fit_transform( df['store_type'] )

        # assortment - Ordinal Encoding
        assortment_dict = {'basic': 1,  'extra': 2, 'extended': 3}
        df['assortment'] = df['assortment'].map( assortment_dict )
        
        ### 5.2.2 Response Variable Transformation
        
        ### 5.2.3 Nature Transformation
        # day of week
        df['day_of_week_sin'] = df['day_of_week'].apply( lambda x: np.sin( x * ( 2. * np.pi/7 ) ) )
        df['day_of_week_cos'] = df['day_of_week'].apply( lambda x: np.cos( x * ( 2. * np.pi/7 ) ) )

        # month
        df['month_sin'] = df['month'].apply( lambda x: np.sin( x * ( 2. * np.pi/12 ) ) )
        df['month_cos'] = df['month'].apply( lambda x: np.cos( x * ( 2. * np.pi/12 ) ) )

        # day 
        df['day_sin'] = df['day'].apply( lambda x: np.sin( x * ( 2. * np.pi/30 ) ) )
        df['day_cos'] = df['day'].apply( lambda x: np.cos( x * ( 2. * np.pi/30 ) ) )

        # week of year
        df['week_of_year_sin'] = df['week_of_year'].apply( lambda x: np.sin( x * ( 2. * np.pi/52 ) ) )
        df['week_of_year_cos'] = df['week_of_year'].apply( lambda x: np.cos( x * ( 2. * np.pi/52 ) ) )
        
        cols_select = ['store',
                'promo',
                'store_type',
                'competition_distance',
                'competition_open_since_month',
                'competition_open_since_year',
                'promo2_since_week',
                'competition_time_month',
                'promo_time_week',
                'day_of_week_sin',
                'day_of_week_cos',
                'month_cos',
                'month_sin',
                'day_sin',
                'day_cos']
        return df[cols_select]
    
```