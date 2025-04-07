import pandas as pd
from sklearn.model_selection import train_test_split, learning_curve, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import pickle

df = pd.read_csv('loan_data.csv')

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

RF_model = RandomForestRegressor(n_estimators=100)


RF_model.fit(X_train, y_train)


print(f"MLPRegressor Score = {RF_model.score(X_test, y_test)}")

y_pred_mlp = RF_model.predict(X_test)

MSE_RF = mean_squared_error(y_test, y_pred_mlp)
print(f"MLPRegressor MSE = {MSE_RF}")

ABS_RF = mean_absolute_error(y_test, y_pred_mlp)
print(f"MLPRegressor ABS = {ABS_RF}")


for i in range(25):
    print(f"MLPRegressor Prédiction: {y_pred_mlp[i]}, Valeur réelle: {y_test[i]}, Difference : { y_test[i] - y_pred_mlp[i] } ")


train_sizes, train_scores, test_scores = learning_curve(RF_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error',
                                                        train_sizes=np.linspace(0.1, 1.0, 10))

train_scores_mean = -np.mean(train_scores, axis=1)
test_scores_mean = -np.mean(test_scores, axis=1)

plt.figure()
plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='RF Training set')
plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='RF Validation set')

plt.xlabel('Taille du lot de donnée')
plt.ylabel('Erreur')
plt.title('RF Learning Curve')
plt.legend(loc='best')
plt.grid()
plt.show()


kf = KFold(n_splits=5, shuffle=True, random_state=100)
cv_scores_RF = cross_val_score(RF_model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
cv_scores_RF = -cv_scores_RF  

with open('boite_a_IA.pkl','wb') as f:
    pickle.dump(RF_model,f)


print(f"MLPRegressor Cross-validation MSE scores: {cv_scores_RF}")
print(f"MLPRegressor Mean cross-validation MSE: {cv_scores_RF.mean()}")
