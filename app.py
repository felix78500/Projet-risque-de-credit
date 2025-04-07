from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

app = Flask(__name__)

#pour pouvoir utiliser l'ia
with open('boite_a_IA.pkl', 'rb') as file:
    model = pickle.load(file)

#definir la premiere page lorsque on fait http://127.0.0.1:5000
@app.route('/')
def home():
    return render_template('index.html')

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
    prediction = model.predict(features)
    print("Résultat brut:", prediction)

    #La prédiction retournée
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)