import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, learning_curve, KFold, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.impute import SimpleImputer

# Configurer les options d'affichage
pd.set_option('display.max_columns', None)
np.set_printoptions(precision=3, suppress=True)

# Charger les données
df = pd.read_csv('loan_data.csv')

# Exploratory Data Analysis (EDA)
print("Aperçu des données:")
print(df.head())
print("\nInformations sur le dataset:")
print(df.info())
print("\nStatistiques descriptives:")
print(df.describe())

# Vérifier les valeurs manquantes
print("\nValeurs manquantes par colonne:")
print(df.isnull().sum())

# Visualiser la distribution de la variable cible
plt.figure(figsize=(10, 6))
sns.histplot(df.iloc[:, -1], kde=True)
plt.title('Distribution de la variable cible')
plt.tight_layout()
plt.savefig('target_distribution.png')

# Identifier les colonnes catégorielles et numériques
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
numerical_cols.remove(df.columns[-1])  # Enlever la variable cible des colonnes numériques

print(f"\nColonnes catégorielles: {categorical_cols}")
print(f"Colonnes numériques: {numerical_cols}")

# Préparation des données
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Division des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Prétraitement avec pipeline et gestion appropriée des types de données
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Fonction pour évaluer et comparer les modèles
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    # Entraînement
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    
    # Métriques
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\n{model_name} Évaluation:")
    print(f"R² Score: {r2:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    
    # Échantillon de prédictions
    print(f"\nComparaison des prédictions ({model_name}):")
    comparison = pd.DataFrame({'Réel': y_test[:10], 'Prédit': y_pred[:10], 'Différence': y_test[:10] - y_pred[:10]})
    print(comparison)
    
    # Learning Curve
    train_sizes, train_scores, test_scores = learning_curve(
        model, X_train, y_train, cv=5, scoring='neg_mean_squared_error',
        train_sizes=np.linspace(0.1, 1.0, 10), random_state=42
    )
    
    train_scores_mean = -np.mean(train_scores, axis=1)
    test_scores_mean = -np.mean(test_scores, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label=f'{model_name} - Erreur d\'entraînement')
    plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label=f'{model_name} - Erreur de validation')
    plt.xlabel('Taille de l\'échantillon d\'entraînement')
    plt.ylabel('Erreur quadratique moyenne (MSE)')
    plt.title(f'Courbe d\'apprentissage - {model_name}')
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{model_name.replace(" ", "_").lower()}_learning_curve.png')
    
    # Cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train, y_train, cv=kf, scoring='neg_mean_squared_error')
    cv_scores = -cv_scores
    
    print(f"\n{model_name} - Cross-validation MSE scores: {cv_scores}")
    print(f"{model_name} - Moyenne de cross-validation MSE: {cv_scores.mean():.4f}")
    print(f"{model_name} - Écart-type de cross-validation MSE: {cv_scores.std():.4f}")
    
    return model, y_pred, mse

# Définir et comparer différents modèles
models = {
    'Régression Linéaire': Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ]),
    'Ridge Regression': Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', Ridge(alpha=1.0))
    ]),
    'MLP Regressor': Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42))
    ]),
    'Random Forest': Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ]),
    'Gradient Boosting': Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', GradientBoostingRegressor(n_estimators=100, random_state=42))
    ])
}

# Évaluer tous les modèles
results = {}
for name, model in models.items():
    print(f"\n{'='*50}")
    print(f"Évaluation du modèle: {name}")
    print(f"{'='*50}")
    fitted_model, predictions, mse = evaluate_model(model, X_train, X_test, y_train, y_test, name)
    results[name] = {'model': fitted_model, 'mse': mse, 'predictions': predictions}

# Identifier le meilleur modèle
best_model_name = min(results, key=lambda k: results[k]['mse'])
print(f"\nMeilleur modèle: {best_model_name} avec MSE = {results[best_model_name]['mse']:.4f}")

# Optimisation du meilleur modèle par GridSearchCV
if best_model_name == 'MLP Regressor':
    print("\nOptimisation des hyperparamètres pour MLP Regressor...")
    param_grid = {
        'regressor__hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
        'regressor__alpha': [0.0001, 0.001, 0.01],
        'regressor__learning_rate_init': [0.001, 0.01]
    }
    
    grid_search = GridSearchCV(
        results[best_model_name]['model'],
        param_grid,
        cv=3,
        scoring='neg_mean_squared_error',
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"Meilleurs paramètres: {grid_search.best_params_}")
    print(f"Meilleur score MSE: {-grid_search.best_score_:.4f}")
    
    # Évaluer le modèle optimisé
    best_model = grid_search.best_estimator_
    evaluate_model(best_model, X_train, X_test, y_train, y_test, 'MLP Optimisé')

# Comparaison visuelle des modèles
model_names = list(results.keys())
mse_values = [results[name]['mse'] for name in model_names]

plt.figure(figsize=(12, 6))
bars = plt.bar(model_names, mse_values)
plt.title('Comparaison des MSE pour différents modèles')
plt.xlabel('Modèles')
plt.ylabel('Erreur quadratique moyenne (MSE)')
plt.xticks(rotation=45)

# Ajouter les valeurs numériques sur les barres
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height:.4f}', ha='center', va='bottom', rotation=0)

plt.tight_layout()
plt.savefig('model_comparison.png')
plt.show()

# Analyse des caractéristiques d'importance (pour Random Forest)
if 'Random Forest' in results:
    rf_model = results['Random Forest']['model']
    feature_names = numerical_cols + [f"{col}_{cat}" for col in categorical_cols 
                                     for cat in df[col].unique()[1:]]
    
    # Accéder au regressor après le prétraitement
    rf_regressor = rf_model.named_steps['regressor']
    
    # Obtenir l'importance des caractéristiques
    importances = rf_regressor.feature_importances_
    
    # Créer un DataFrame pour l'affichage
    feature_importance = pd.DataFrame({'Feature': feature_names[:len(importances)], 
                                       'Importance': importances})
    feature_importance = feature_importance.sort_values('Importance', ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importance.head(15))
    plt.title('Top 15 des caractéristiques les plus importantes')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    plt.show()

print("\nAnalyse terminée. Les visualisations ont été sauvegardées dans le répertoire courant.")