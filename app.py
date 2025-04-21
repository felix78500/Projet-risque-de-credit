from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from flask import render_template
import pickle
import joblib
from modelDao.UtilisateurDao import UtilisateurDao

app = Flask(__name__)
CORS(app)
dao = UtilisateurDao()
scaler = joblib.load('scaler.joblib')
model = joblib.load('boite_a_IA.joblib')

test = np.array([int(22), int(0), int(0), float(71948.0), int(0), int(3), float(35000.0), float(4), float(16.02), float(0.49), float(3.0), float(561), int(0)]).reshape(1, -1)

test = scaler.transform(test)
print(model.predict(test))

dao = UtilisateurDao()

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

# la methode pour envoyer des donnée a l'ia
@app.route('/predict', methods=['POST'])
def predict():

    #récupere les donnée provenant de index.html
    data = request.json
    print("Données reçues:", data)

    #les colonnes afilliée au données pour que l'ia comprenne
    features = np.array([float(data['person_age']), int(data['person_gender']), int(data['person_education']), float(data['person_income']), int(data['person_emp_exp']), int(data['person_home_ownership']), float(data['loan_amnt']), float(data['loan_intent']), float(data['loan_int_rate']), float(data['loan_percent_income']), float(data['cb_person_cred_hist_length']), float(data['credit_score']), int(data['previous_loan_defaults_on_file'])]).reshape(1, -1)
    print("Features avant prédiction:", features)

    #l'utilisation de l'ia
    features = scaler.transform(features)
    prediction = model.predict(features)
    print("Résultat brut:", prediction)

    #La prédiction retournée
    return jsonify({'prediction': prediction.tolist()})

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

if __name__ == '__main__':
    app.run(debug=False)
