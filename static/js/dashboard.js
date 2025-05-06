fetch('/get_prediction')
  .then(res => res.json())
  .then(data => {
    document.getElementById('prediction-percentage').innerText = `Prédiction : ${data.prediction[0] * 100}%`;
  });