import numpy as np
import shap
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os
import matplotlib.ticker as mtick

def analyse_donnees(modele, caracteristiques, noms_caracteristiques=None, afficher_graphique=True, 
                   sauvegarder_graphique=False, nom_fichier='analyse_shap.png'):
    """
    Analyse l'impact de chaque caractéristique sur une prédiction en utilisant les valeurs SHAP.
    
    Paramètres:
    -----------
    modele : modèle ML entraîné ou chemin d'accès
        Un modèle d'apprentissage automatique entraîné avec une méthode predict ou chemin vers un modèle sauvegardé
        
    caracteristiques : tableau ou liste
        Un échantillon unique à analyser sous forme de liste ou tableau
        
    noms_caracteristiques : liste, optionnel
        Liste des noms de caractéristiques correspondant aux entrées
        
    afficher_graphique : bool, par défaut=True
        Indique s'il faut afficher la visualisation
        
    sauvegarder_graphique : bool, par défaut=False
        Indique s'il faut sauvegarder la visualisation dans un fichier
        
    nom_fichier : str, par défaut='analyse_shap.png'
        Nom du fichier pour enregistrer la visualisation
        
    Retourne:
    --------
    dict : Dictionnaire contenant les noms des caractéristiques comme clés et les valeurs SHAP comme valeurs
    """
    
    # Convertir l'entrée en tableau numpy et redimensionner pour un seul échantillon
    tableau_caracteristiques = np.array(caracteristiques).reshape(1, -1)
    
    # Vérifier si le modèle est un chemin d'accès vers un modèle sauvegardé
    if isinstance(modele, str):
        try:
            modele = joblib.load(modele)
        except:
            raise ValueError("Échec du chargement du modèle depuis le chemin fourni")
    
    # Créer l'explainer SHAP
    explainer = shap.TreeExplainer(modele)
    
    # Calculer les valeurs SHAP
    valeurs_shap = explainer(tableau_caracteristiques)
    
    # Si les noms de caractéristiques ne sont pas fournis, créer des noms génériques
    if noms_caracteristiques is None:
        noms_caracteristiques = [f"Caracteristique_{i}" for i in range(len(caracteristiques))]
    
    # Créer un dictionnaire associant les noms de caractéristiques aux valeurs SHAP
    resultats = {}
    for i, nom in enumerate(noms_caracteristiques):
        resultats[nom] = float(valeurs_shap.values[0][i])
    
    # Stocker également la valeur de base et la valeur prédite
    resultats["_valeur_base"] = float(valeurs_shap.base_values[0])
    resultats["_prediction"] = float(modele.predict(tableau_caracteristiques)[0])
    
    # Créer la visualisation
    if afficher_graphique or sauvegarder_graphique:
        plt.figure(figsize=(14, 8))
        
        # Graphique 1: Diagramme en cascade (gauche)
        plt.subplot(1, 2, 1)
        shap.plots.waterfall(valeurs_shap[0], max_display=len(noms_caracteristiques), show=False)
        plt.title("Diagramme en cascade SHAP: Impact des caractéristiques sur la prédiction", fontsize=12)
        
        # Graphique 2: Diagramme à barres d'importance des caractéristiques (droite)
        plt.subplot(1, 2, 2)
        # Créer les valeurs d'importance
        valeurs_importance = np.abs(valeurs_shap.values[0])
        # Trier les caractéristiques par importance absolue
        indices_tries = np.argsort(valeurs_importance)
        noms_tries = [noms_caracteristiques[i] for i in indices_tries]
        valeurs_triees = valeurs_importance[indices_tries]
        
        # Créer un diagramme à barres horizontal
        plt.barh(range(len(noms_tries)), valeurs_triees)
        plt.yticks(range(len(noms_tries)), noms_tries)
        plt.xlabel("Valeur SHAP absolue (Magnitude de l'impact des caractéristiques)")
        plt.title("Impact des caractéristiques sur la prédiction", fontsize=12)
        
        plt.tight_layout()
        
        if sauvegarder_graphique:
            chemin_fichier = os.path.join('static', 'image', nom_fichier + '.png')
            plt.savefig(chemin_fichier, dpi=300, bbox_inches='tight')
        
        if afficher_graphique:
            plt.show()

        #graphique plus client-friendly
        valeurs = valeurs_shap.values[0]
        noms = noms_caracteristiques
        couleurs = ['#ff3333' if v > 0 else '#33bbff' for v in valeurs] 
        valeurs_arrondies = [round(v*100, 3) for v in valeurs]
        

        # Taille du graphique
        fig, ax = plt.subplots(figsize=(12, 0.7 * len(noms))) 

        # Barres
        bars = ax.barh(noms, valeurs_arrondies, color=couleurs, edgecolor='grey', height=0.8)

        ax.axvline(0, color='black', linewidth=0.8)
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.2f}'))

        ax.tick_params(axis='y', labelsize=15)
        ax.tick_params(axis='x', labelsize=11)
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')

        # Ajout des valeurs
        for i, bar in enumerate(bars):
            width = bar.get_width()
            align = 'left'
            offset = 0.05
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    f'{valeurs_arrondies[i]}', va='center', ha=align, fontsize=11)

        # Supprimer les bordures du graphique
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.tight_layout()
        
        chemin_fichier2 = os.path.join('static', 'image', nom_fichier + '_simple.png')
        plt.savefig(chemin_fichier2, dpi=300, bbox_inches='tight')
        
    return resultats


# Exemple d'utilisation:
# if __name__ == "__main__":
#     # Charger le modèle sauvegardé et le scaler
#     modele = joblib.load('rf_model.joblib')
#     scaler = joblib.load('scaler.joblib')
    
#     # Définir les noms des caractéristiques à partir des données originales
#     noms_caracteristiques = ['age_personne', 'genre_personne', 'education_personne', 'revenu_personne',
#                            'experience_emploi_personne', 'propriete_maison_personne', 'montant_pret', 
#                            'intention_pret', 'taux_interet_pret', 'pourcentage_revenu_pret', 
#                            'longueur_historique_credit_personne', 'score_credit', 'defauts_pret_precedents']
    
#     # Créer un échantillon de test et le normaliser
#     test = [int(22), int(0), int(0), float(71948.0), int(0), int(3), 
#             float(35000.0), float(4), float(16.02), float(0.49), 
#             float(3.0), float(561), int(0)]
    
#     test_normalise = scaler.transform(np.array(test).reshape(1, -1))[0]
    
#     # Analyser les données avec visualisation
#     resultats = analyse_donnees(modele, test_normalise, noms_caracteristiques, 
#                                afficher_graphique=True, sauvegarder_graphique=True,
#                                nom_fichier='analyse_impact_caracteristiques.png')
    
#     print("\nValeurs SHAP (impacts des caractéristiques) pour la prédiction de test:")
#     for nom, valeur in resultats.items():
#         if not nom.startswith('_'):
#             print(f"{nom}: {valeur:.4f}")
    
#     print(f"\nValeur de base: {resultats['_valeur_base']:.4f}")
#     print(f"Prédiction: {resultats['_prediction']:.4f}")