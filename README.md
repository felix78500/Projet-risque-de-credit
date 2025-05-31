
# Projet Risque de Crédit

## Présentation

Ce projet a pour objectif de prédire le risque de crédit d'un client à partir de données issues d’un ensemble de prêts. Il utilise des techniques de machine learning, notamment un modèle de forêt aléatoire (Random Forest), déployé via une application web construite avec Flask.

## Modèle de Machine Learning

Le modèle est entraîné à l’aide du dataset `loan_data.csv` via le script `Random_forest.py` qui est ensuite enregistrée dans `ConcerneIa/boite_a_IA.joblib` pour pouvoir l'utiliser via Flask. Il permet de déterminer la probabilité de défaut de paiement d’un client. Le modèle entraîné est ensuite utilisé dans l'application Flask.

## Interface

L’interface web est développée avec Flask dans `app.py`, qui permet de :
- Utiliser l'IA via une jolie interface,
- Obtenir une prédiction du risque de crédit à partir de plusieurs donnée (age, situation immobilière, etc...).
- Obtenir les détails de la prédiction (raison, statut, schéma, etc...)

## Structure du Projet
```
Projet-risque-de-credit/
│
├── app.py                  # Point d'entrée de l'application Flask
├── Random_forest.py        # Entraînement du modele
├── loan_data.csv           # Jeu de données utilisé pour l'entraînement
├── AfficheBDD.py           # Script pour afficher la base de données
├── La doc technique .pdf   # Document décrivant le projet
│
├── model/                  # Contient la classe utilisateur
├── modelDao/               # Gestion des données utilisateur via bdd
├── static/                 # Fichiers CSS, JS, les graphique IA et les JSON utilisée pour les détail de la prédiction
├── templates/              # Templates HTML (interface utilisateur)
└── ConcerneIa/             # Contient le modèle enregistré de l'IA
```

### Prérequis

- Python ≥ 3.8
- `pip` pour installer les dépendances

Puis accéder à : [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📄 Documentation

La documentation technique est **La doc technique.pdf**, qui explique :
- Le processus de nettoyage des données
- Le choix du modèle
- La structure de l’application