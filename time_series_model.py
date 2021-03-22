# LIBRARIES
import itertools
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.filterwarnings('ignore')

# READ DATA SET
data = sm.datasets.co2.load_pandas()
y = data.data
y = y['co2'].resample('MS').mean()
y.shape
y = y.fillna(y.bfill())

# TIME SERIES VISUALIZATION
y.plot(figsize=(15, 6))
plt.show()

# The train was installed from 1958 to the end of 1997.
train = y[:'1997-12-01']
len(train)

# Test set from the first month of 1998 to the end of 2001.
test = y['1998-01-01':]
len(test)

# Stationarity Test


def is_stationary(y):
    print("HO: Seri Durağan değildir.")
    print("H1: Seri Durağandır.")
    p_value = sm.tsa.stattools.adfuller(y)[1]
    if p_value < 0.05:
        print(F"Sonuç: Seri Durağandır ({p_value}).")
    else:
        print(F"Sonuç: Seri Durağan Değildir ({p_value}).")


is_stationary(y)

# TES Model
tes_model = ExponentialSmoothing(train,
                                 trend="add",
                                 seasonal="add",
                                 seasonal_periods=12).fit(smoothing_level=0.5,
                                                          smoothing_slope=0.5,
                                                          smoothing_seasonal=0.5)

y_pred = tes_model.forecast(48)
train["1985":].plot(title="Triple Exponential Smoothing")
test.plot()
y_pred.plot()
plt.show()
mean_absolute_error(test, y_pred)

# Optimizing Triple Exponential Smoothing
alphas = betas = gammas = np.arange(0.20, 1, 0.10)
abg = list(itertools.product(alphas, betas, gammas))


def optimize_tes(train, abg, step=48):
    print("Optimizing parameters...")
    results = []
    for comb in abg:
        tes_model = ExponentialSmoothing(train, trend="add",
                                         seasonal="add",
                                         seasonal_periods=12).\
            fit(smoothing_level=comb[0],
                smoothing_slope=comb[1],
                smoothing_seasonal=comb[2])

        y_pred = tes_model.forecast(step)
        mae = mean_absolute_error(test, y_pred)

        print([round(comb[0], 2), round(comb[1], 2), round(comb[2], 2), round(mae, 2)])

        results.append([round(comb[0], 2), round(comb[1], 2), round(comb[2], 2), round(mae, 2)])
    results = pd.DataFrame(results, columns=["alpha", "beta", "gamma", "mae"]).sort_values("mae")
    print(results)


alphas = betas = gammas = np.arange(0.10, 1, 0.20)
abg = list(itertools.product(alphas, betas, gammas))
optimize_tes(train, abg)

#################################
# Final TES Model
#################################
final_tes_model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12).\
            fit(smoothing_level=0.5, smoothing_slope=0.1, smoothing_seasonal=0.1)
y_pred = final_tes_model.forecast(48)
train["1985":].plot(title="Triple Exponential Smoothing")
test.plot()
y_pred.plot()
plt.show()
mean_absolute_error(test, y_pred)

# MODEL TO SAVE
pickle.dump(final_tes_model, open('final_tes_model.pkl', 'wb'))


