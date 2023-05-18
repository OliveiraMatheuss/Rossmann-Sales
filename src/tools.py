from sys import displayhook
import pandas as pd
import numpy as np
from scipy import stats  as ss
import seaborn as sns
from matplotlib import pyplot as plt
from IPython.core.display import HTML
from sklearn.metrics       import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import TimeSeriesSplit



def timeSeries_CV(X, y, model_name, model, kfold = 5, verbose = False):
        mae_list = []
        mape_list = []
        rmse_list = []
        tscv = TimeSeriesSplit(n_splits= kfold)
        for i, (train_index, test_index) in enumerate(tscv.split(X)):
                if verbose:
                        print(f"Fold {i+1}:")
                
                # model
                m = model.fit( X.iloc[train_index], y.iloc[train_index]  )

                # prediction
                yhat = m.predict(X.iloc[test_index])

                # performance
                m_result = ml_error( model_name, np.expm1( y.iloc[test_index] ), np.expm1( yhat ) )

                # store performance of each kfold iteration
                mae_list.append(  m_result['MAE'] )
                mape_list.append( m_result['MAPE'] )
                rmse_list.append( m_result['RMSE'] )

        return pd.DataFrame( {'Model Name': model_name,
                                'MAE CV': np.round( np.mean( mae_list ), 2 ).astype( str ) + ' +/- ' + np.round( np.std( mae_list ), 2 ).astype( str ),
                                'MAPE CV': np.round( np.mean( mape_list ), 2 ).astype( str ) + ' +/- ' + np.round( np.std( mape_list ), 2 ).astype( str ),
                                'RMSE CV': np.round( np.mean( rmse_list ), 2 ).astype( str ) + ' +/- ' + np.round( np.std( rmse_list ), 2 ).astype( str ) }, index=[0] )


def ml_error( model_name, y, yhat ):
    mae = mean_absolute_error( y, yhat )
    mape = mean_absolute_percentage_error( y, yhat )
    rmse = np.sqrt( mean_squared_error( y, yhat ) )
    
    return pd.DataFrame( {  'Model Name': model_name, 
                            'MAE': mae, 
                            'MAPE': mape,
                            'RMSE': rmse }, index=[0] )

def cramer_v( x, y ):
    cm = pd.crosstab( x, y ).as_matrix()
    n = cm.sum()
    r, k = cm.shape
    
    chi2 = ss.chi2_contingency( cm )[0]
    chi2corr = max( 0, chi2 - (k-1)*(r-1)/(n-1) )
    
    kcorr = k - (k-1)**2/(n-1)
    rcorr = r - (r-1)**2/(n-1)
    
    return np.sqrt( (chi2corr/n) / ( min( kcorr-1, rcorr-1 ) ) )

def jupyter_settings():

    plt.style.use( 'bmh' )
    plt.rcParams['figure.figsize'] = [25, 12]
    plt.rcParams['font.size'] = 24
    
    displayhook( HTML( '<style>.container { width:100% !important; }</style>') )
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None
    pd.set_option( 'display.expand_frame_repr', False )
    
    sns.set()