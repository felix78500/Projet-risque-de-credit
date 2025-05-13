import pandas as pd
from sklearn.model_selection import train_test_split, learning_curve, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('loan_data.csv')

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

mlp_model = MLPRegressor(hidden_layer_sizes=100, random_state=100)

mlp_model.fit(X_train, y_train)

print(f"MLPRegressor Score = {mlp_model.score(X_test, y_test)}")

y_pred_mlp = mlp_model.predict(X_test)

MSE_mlp = mean_squared_error(y_test, y_pred_mlp)
print(f"MLPRegressor MSE = {MSE_mlp}")

ABS_mlp = mean_absolute_error(y_test, y_pred_mlp)
print(f"MLPRegressor ABS = {ABS_mlp}")

for i in range(10):
    print(f"MLPRegressor Prédiction: {y_pred_mlp[i]}, Valeur réelle: {y_test[i]}")

train_sizes, train_scores, test_scores = learning_curve(mlp_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error',
                                                        train_sizes=np.linspace(0.1, 1.0, 10))

train_scores_mean = -np.mean(train_scores, axis=1)
test_scores_mean = -np.mean(test_scores, axis=1)

plt.figure()
plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='MLP Training set')
plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='MLP Validation set')

plt.xlabel('Taille du lot de donnée')
plt.ylabel('Erreur')
plt.title('MLPRegressor Learning Curve')
plt.legend(loc='best')
plt.grid()
plt.show()

kf = KFold(n_splits=5, shuffle=True, random_state=100)
cv_scores_mlp = cross_val_score(mlp_model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
cv_scores_mlp = -cv_scores_mlp  

print(f"MLPRegressor Cross-validation MSE scores: {cv_scores_mlp}")
print(f"MLPRegressor Mean cross-validation MSE: {cv_scores_mlp.mean()}")


lr_model = LinearRegression()


lr_model.fit(X_train, y_train)


print(f"Linear Regression Score = {lr_model.score(X_test, y_test)}")

y_pred_lr = lr_model.predict(X_test)

MSE_lr = mean_squared_error(y_test, y_pred_lr)
print(f"Regretion lineraire MSE = {MSE_lr}")

ABS_lr = mean_absolute_error(y_test, y_pred_lr)
print(f"Regretion lineraire ABS = {ABS_lr}")


for i in range(10):
    print(f"Regretion lineraire Prédiction: {y_pred_lr[i]}, Valeur réelle: {y_test[i]}")


train_sizes, train_scores, test_scores = learning_curve(lr_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error',
                                                        train_sizes=np.linspace(0.1, 1.0, 10))

train_scores_mean = -np.mean(train_scores, axis=1)
test_scores_mean = -np.mean(test_scores, axis=1)

plt.figure()
plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='LR Training error')
plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='LR Validation error')

plt.xlabel('Taille du lot de donnée')
plt.ylabel('Erreur')
plt.title('Regretion lineraire Learning Curve')
plt.legend(loc='best')
plt.grid()
plt.show()

cv_scores_lr = cross_val_score(lr_model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
cv_scores_lr = -cv_scores_lr  

print(f"Regretion lineraire Cross-validation MSE scores: {cv_scores_lr}")
print(f"Regretion lineraire Mean cross-validation MSE: {cv_scores_lr.mean()}")
