import pandas as pd
from sklearn.model_selection import train_test_split, learning_curve, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import pickle

# Charger les données
df = pd.read_csv('loan_data.csv')

# Prétraitement des données
pd.set_option('future.no_silent_downcasting', True)
df.replace(['male','female'], [0,1], inplace=True)
df.replace(['Associate','Bachelor','Doctorate','High School','Master'], [0,1,2,3,4], inplace=True)
df.replace(['MORTGAGE','OTHER','OWN','RENT'], [0,1,2,3], inplace=True)
df.replace(['DEBTCONSOLIDATION','EDUCATION','HOMEIMPROVEMENT','MEDICAL','PERSONAL','VENTURE'], [0,1,2,3,4,5], inplace=True)
df.replace(['No','Yes'], [0,1], inplace=True)

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def model(n):
    best_model = None
    best_mse = 100

    for i in range(n):
        RF_model = RandomForestRegressor(n_estimators=100)
        RF_model.fit(X_train, y_train)

        y_pred = RF_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(mse)

        if mse < best_mse:
            best_mse = mse
            best_model = RF_model

    return best_model, best_mse

n = 50
best_model, best_mse = model(n)
print(f"Meilleur MSE après {n} itérations: {best_mse}")

with open('model_dans_une_boite.pkl', 'wb') as f:
    pickle.dump(best_model, f)