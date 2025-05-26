import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from flask import render_template
import joblib
import json
from modelDao.UtilisateurDao import UtilisateurDao
from model.fonction_dashboard import analyse_donnees

app = Flask(__name__)
CORS(app)
#instanciation de la manipulation de l'utilsateur via dao
dao = UtilisateurDao()

#importation du scaller et du model
chemin_scaler= os.path.join('ConcerneIa', 'scaler.joblib')
chemin_model= os.path.join('ConcerneIa', 'boite_a_IA.joblib')

scaler = joblib.load(chemin_scaler)
model = joblib.load(chemin_model)

dao = UtilisateurDao()

#les different liste pour simplifier la vie de l'utilisateur
liste_des_nom_simplifier=["Âge", 
                          "Sexe",
                          "Diplome", 
                          "Revenu", 
                          "Expérience professionnelle", 
                          "Situtation immobilière",
                          "Montant du prêt",
                          "Raison du prêt",
                          "Taux d'intérêt",
                          "% ,du revenu",
                          "Historique crédit",
                          "Score crédit",
                          "Defaut de dette auparavant"]

raison_si_positif = [
    "Âge approprié pour un prêt stable",  
    "Sexe sans impact significatif détecté",
    "Niveau d'études élevé, preuve de stabilité", 
    "Bon niveau de revenu, capacité de remboursement probable",
    "Expérience professionnelle solide",
    "Situation immobilière stable (propriétaire ou logement stable)",
    "Montant du prêt raisonnable par rapport aux revenus", 
    "Raison du prêt jugée responsable (ex. : achat immobilier, investissement)", 
    "Taux d'intérêt acceptable pour la situation financière", 
    "Faible pourcentage du revenu alloué au remboursement", 
    "Bon historique de crédit",
    "Score de crédit élevé",
    "Ancien prêt bien remboursé, preuve de fiabilité" 
]

raison_si_negatif = [
    "Âge jugé trop jeune ou trop vieux pour un prêt long terme",
    "Le genre n'influence pas directement, mais pourrait être corrélé à d'autres risques (à traiter avec prudence)", 
    "Diplôme faible, risque accru d'instabilité professionnelle", 
    "Revenu trop faible pour couvrir les mensualités",  
    "Manque d'expérience professionnelle",  
    "Situation immobilière instable (location précaire ou sans domicile fixe)", 
    "Montant du prêt trop élevé par rapport aux revenus", 
    "Raison du prêt considérée comme risquée (ex. : loisirs, dettes antérieures)",  
    "Taux d'intérêt trop élevé, risque de non-remboursement",  
    "Pourcentage du revenu trop élevé dédié au remboursement",
    "Historique de crédit négatif ou inexistant",  
    "Score de crédit faible",
    "Ancien prêt non remboursé ou en défaut" 
]

#importation des fichier json
chemin_json_prediction = os.path.join('static', 'json', 'predictions.json')
chemin_json_analyse = os.path.join('static', 'json', 'analyse.json')

#identifiant de connexion a la base de donnée
SUPABASE_URL = 'https://xcpqafebvepowoxxppsd.supabase.co'
SUPABASE_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjcHFhZmVidmVwb3dveHhwcHNkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NDEwNzc2NiwiZXhwIjoyMDU5NjgzNzY2fQ.66tUU4BoxxJ8KXcsrbstY3j8Jm38f-M8MadlycAdwUY'
HEADERS = {
    'apikey': SUPABASE_API_KEY,
    'Authorization': f'Bearer {SUPABASE_API_KEY}',
    'Content-Type': 'application/json'
}

#definir la premiere page lorsque on fait http://127.0.0.1:5000
@app.route('/')

#premiere page
def home():
    return render_template('login.html')

#page de prevision
@app.route('/prevision')
def prevision():
    return render_template('prevision.html')

#page du dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# la methode pour envoyer des donnée a l'ia
@app.route('/predict', methods=['POST'])
def predict():

    #récupere les donnée provenant de prediction.html
    data = request.json
    print("Données reçues:", data)

    #les colonnes afilliée au données pour que l'ia comprenne
    features = np.array([float(data['person_age']), int(data['person_gender']), int(data['person_education']), float(data['person_income']), int(data['person_emp_exp']), int(data['person_home_ownership']), float(data['loan_amnt']), float(data['loan_intent']), float(data['loan_int_rate']), float(data['loan_percent_income']), float(data['cb_person_cred_hist_length']), float(data['credit_score']), int(data['previous_loan_defaults_on_file'])]).reshape(1, -1)
    print("Features avant prédiction:", features)

    #l'utilisation de l'ia
    features = scaler.transform(features)
    prediction = model.predict(features)
    print("Résultat brut:", prediction)

    #Reinitialiser le json
    open(chemin_json_prediction, "w").close()

    #La prédiction mise dans le json
    with open(chemin_json_prediction, "a") as f:
        record = {
            "prediction": prediction.tolist()
        }
        f.write(json.dumps(record) + "\n")
    
#permet de prendre la prediction via le fichier json
@app.route('/get_prediction')
def get_prediction():
    with open(chemin_json_prediction, 'r') as f:
        data = json.load(f)
    return jsonify(data)

#ajouter des utilisateur (tester mais pas implementer, et ne seras probablement jamais)
@app.route('/ajout-utilisateur', methods=['POST'])
def ajout_utilisateur():
    data = request.json
    success = dao.insert_user(data['login'], data['mdp'])

    if success:
        return jsonify({'message': 'Utilisateur inséré avec succès'}), 200
    else:
        return jsonify({'message': 'Erreur insertion utilisateur'}), 500

#pour verifier si l'utilisateur existe dans la bdd
@app.route('/verif-utilisateur', methods=['POST'])
def verif_utilisateur():
    data = request.json
    if dao.verif_user(data['login'], data['mdp']):
        return jsonify({'message': 'OK'}), 200
    else:
        return jsonify({'message': 'Non trouvé'}), 404

#Analyse des données 
@app.route('/analyse', methods=['POST'])
def analyse():
    #les champs que l'utilisateur a pris
    data = request.json
    
    #on met tout sa dans un tableau en le transformant dans ce qui nous arrange le plus
    test = [int(data['person_age']), int(data['person_gender']), int(data['person_education']), 
            float(data['person_income']), int(data['person_emp_exp']), int(data['person_home_ownership']), 
             float(data['loan_amnt']), float(data['loan_intent']), float(data['loan_int_rate']), 
             float(data['loan_percent_income']), float(data['cb_person_cred_hist_length']), float(data['credit_score']), int(data['previous_loan_defaults_on_file'])]
    
    #normaliser le tout
    test_normalise = scaler.transform(np.array(test).reshape(1, -1))[0]

    #utilisation de la fonction d'analyse
    resultat = analyse_donnees(model, test_normalise, liste_des_nom_simplifier, afficher_graphique=False, sauvegarder_graphique=True, nom_fichier='analyse_impact_caracteristiques')

    #ouverture du fichier json pour effacer tout ce qui s'y trouve dedans
    open(chemin_json_analyse, "w").close()

    #le tableau results pour ensuite tout mettre dans le fichier json
    results = []
    i=0
    for nom, valeur in resultat.items():
            #ce if est la pour pas que la prediction et la valeur de base ne se mette dans le json
            if not nom.startswith('_'):
                #ce if est pour changer la raison selon le pourcentage
                if resultat['_prediction'] < 0.70:
                    results.append({
                        "nom": nom,
                        "valeur": valeur,
                        "nom_simplifie": liste_des_nom_simplifier[i], 
                        "raison": raison_si_negatif[i]
                    })
                    i+=1
                else : 
                    results.append({
                        "nom": nom,
                        "valeur": valeur,
                        "nom_simplifie": liste_des_nom_simplifier[i], 
                        "raison": raison_si_positif[i]
                    })
                    i+=1
    
    #mettre tout ce qui se trouve dans le tableau, dans notre fichier json
    with open(chemin_json_analyse, "w") as f:
        json.dump(results, f, indent=4)

    #ça, c'est pour debogguer en cas de probleme (il y en as eu)
    return jsonify({"status": "ok"})

#simplement pour prendre le fichier json
@app.route('/get_analyse')
def get_analyse():
    with open(chemin_json_analyse, 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)