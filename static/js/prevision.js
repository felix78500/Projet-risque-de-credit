document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    //tout les champ réuni dans data
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

    let champsVides = [];
    let champString = [];

    //verifier qu'il n'y a pas de lettre
    for (const [key, value] of Object.entries(data)) {
        if (!/^\d+(\.\d+)?$/.test(value)) {
            champString.push(key);
        }
    }

    //verifier qu'il n'y as pas de blanc
    for (const [key, value] of Object.entries(data)) {
        if (value === "" || value === null || value === undefined) {
            champsVides.push(key);
        }
    }

    if (champsVides.length > 0) {
            document.getElementById('result').innerText = `Tout les champs n'ont pas été remplie : ${champsVides.join(", ")}`;
    }else if(champString.length > 0){
            document.getElementById('result').innerText = `Certain champ ne sont pas dans le bon format (1234...) : ${champString.join(", ")}`;
    }else{
        //Utilisation de la prédiction et de l'analyse
        try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });console.log('Status:', response.status);

        const analyseResponse = await fetch('/analyse',{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });console.log("Analyse status:", analyseResponse.status);
        const analyseData = await analyseResponse.json();
        console.log("Analyse response:", analyseData);

        fetch('/get_prediction')
        .then(res => res.json())
        .then(data => {
            x100 = data.prediction[0] * 100
            document.getElementById('result').innerText = `Prédiction : ${x100}%`;
            
        });

        const detailsContainer = document.getElementById("details-container");

        //apres avoir cliquer sur la prediction, et qu'il n'y as pas d'erreur, affiche le boutton pour afficher plus de détail
        if (!document.getElementById("details-btn")) {
            const detailBtn = document.createElement("button");
            detailBtn.id = "details-btn";
            detailBtn.textContent = "Voir les détails de la prédiction";
            detailBtn.className = "detail-button";

            detailBtn.addEventListener("click", function () {
                window.location.href = "/dashboard";
            });

            detailsContainer.appendChild(detailBtn);
        }

        //const result = await response.json();
        //document.getElementById('result').textContent = `Prédiction: ${result.prediction*100} %`;
    } catch (error) {
        console.error('Erreur:', error);
        document.getElementById('result').textContent = `Erreur: ${error.message}`;
    }
    }
});