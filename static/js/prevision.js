document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        person_age: document.getElementById('person_age').value,
        person_gender: document.getElementById('person_gender').value,
        person_education: document.getElementById('person_education').value,
        person_income: document.getElementById('person_income').value,
        person_emp_exp: document.getElementById('person_emp_exp').value,
        person_home_ownership: document.getElementById('person_home_ownership').value,
        loan_amnt: document.getElementById('loan_amnt').value,
        loan_intent: document.getElementById('loan_intent').value,
        loan_int_rate:document.getElementById('loan_int_rate').value,
        loan_percent_income: document.getElementById('loan_percent_income').value,
        cb_person_cred_hist_length: document.getElementById('cb_person_cred_hist_length').value,
        credit_score: document.getElementById('credit_score').value,
        previous_loan_defaults_on_file: parseInt(document.getElementById('previous_loan_defaults_on_file').value),
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });console.log('Status:', response.status);

        await fetch('/analyse',{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        //const result = await response.json();
        //document.getElementById('result').textContent = `Prédiction: ${result.prediction*100} %`;
    } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('result').textContent = `Erreur: ${error.message}`;
    }
});