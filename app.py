from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from flask import render_template
import joblib
import json
from modelDao.UtilisateurDao import UtilisateurDao
from fonction_dashboard import analyse_donnees

app = Flask(__name__)
CORS(app)
dao = UtilisateurDao()
scaler = joblib.load('scaler.joblib')
model = joblib.load('boite_a_IA.joblib')

dao = UtilisateurDao()

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
                          "Ancien prêt remboursé ?"]

raison_si_positif = [
    "Âge approprié pour un prêt stable",  # Âge
    "Sexe sans impact significatif détecté",  # Sexe (peut être neutre ou inclusif selon votre modèle)
    "Niveau d'études élevé, preuve de stabilité",  # Diplome
    "Bon niveau de revenu, capacité de remboursement probable",  # Revenu
    "Expérience professionnelle solide",  # Expérience professionnelle
    "Situation immobilière stable (propriétaire ou logement stable)",  # Situtation immobilière
    "Montant du prêt raisonnable par rapport aux revenus",  # Montant du prêt
    "Raison du prêt jugée responsable (ex. : achat immobilier, investissement)",  # Raison du prêt
    "Taux d'intérêt acceptable pour la situation financière",  # Taux d'intérêt
    "Faible pourcentage du revenu alloué au remboursement",  # % du revenu
    "Bon historique de crédit",  # Historique crédit
    "Score de crédit élevé",  # Score crédit
    "Ancien prêt bien remboursé, preuve de fiabilité"  # Ancien prêt remboursé ?
]

raison_si_negatif = [
    "Âge jugé trop jeune ou trop vieux pour un prêt long terme",  # Âge
    "Le genre n'influence pas directement, mais pourrait être corrélé à d'autres risques (à traiter avec prudence)",  # Sexe
    "Diplôme faible, risque accru d'instabilité professionnelle",  # Diplome
    "Revenu trop faible pour couvrir les mensualités",  # Revenu
    "Manque d'expérience professionnelle",  # Expérience professionnelle
    "Situation immobilière instable (location précaire ou sans domicile fixe)",  # Situtation immobilière
    "Montant du prêt trop élevé par rapport aux revenus",  # Montant du prêt
    "Raison du prêt considérée comme risquée (ex. : loisirs, dettes antérieures)",  # Raison du prêt
    "Taux d'intérêt trop élevé, risque de non-remboursement",  # Taux d'intérêt
    "Pourcentage du revenu trop élevé dédié au remboursement",  # % du revenu
    "Historique de crédit négatif ou inexistant",  # Historique crédit
    "Score de crédit faible",  # Score crédit
    "Ancien prêt non remboursé ou en défaut"  # Ancien prêt remboursé ?
]


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
    open("predictions.json", "w").close()

    #La prédiction mise dans le json
    with open("predictions.json", "a") as f:
        record = {
            "prediction": prediction.tolist()
        }
        f.write(json.dumps(record) + "\n")
    
@app.route('/get_prediction')
def get_prediction():
    with open('predictions.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

#ajouter des utilisateur (tester mais pas implementer)
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

@app.route('/analyse', methods=['POST'])
def analyse():
    data = request.json
    
    test = [int(data['person_age']), int(data['person_gender']), int(data['person_education']), 
            float(data['person_income']), int(data['person_emp_exp']), int(data['person_home_ownership']), 
             float(data['loan_amnt']), float(data['loan_intent']), float(data['loan_int_rate']), 
             float(data['loan_percent_income']), float(data['cb_person_cred_hist_length']), float(data['credit_score']), int(data['previous_loan_defaults_on_file'])]
    
    test_normalise = scaler.transform(np.array(test).reshape(1, -1))[0]

    resultat = analyse_donnees(model, test_normalise, liste_des_nom_simplifier, afficher_graphique=False, sauvegarder_graphique=True, nom_fichier='analyse_impact_caracteristiques')

    open("analyse.json", "w").close()

    results = []
    i=0
    for nom, valeur in resultat.items():
        if not nom.startswith('_'):
            if resultat['_prediction'] < 0.70:
                results.append({
                    "nom": nom,
                    "valeur": valeur,
                    "nom_simplifié": liste_des_nom_simplifier[i], 
                    "raison": raison_si_negatif[i]
                })
                i+=1
            else : 
                results.append({
                    "nom": nom,
                    "valeur": valeur,
                    "nom_simplifié": liste_des_nom_simplifier[i], 
                    "raison": raison_si_positif[i]
                })
                i+=1

        

    with open("analyse.json", "w") as f:
        json.dump(results, f, indent=4)

@app.route('/get_analyse')
def get_analyse():
    with open('analyse.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)