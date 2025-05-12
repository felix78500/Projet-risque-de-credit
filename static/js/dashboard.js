fetch('/get_prediction')
  .then(res => res.json())
  .then(data => {
    x100 = data.prediction[0] * 100
    document.getElementById('prediction-percentage').innerText = `Prédiction : ${x100}%`;
    
    fetch('/get_analyse')
    .then(res => res.json())
    .then(data => {
      if(x100 < 70){
      document.getElementById('prediction-status').innerText = `Refuser`;
      const minItem = data.find(item => item.valeur === Math.min(...data.map(i => i.valeur)))
      document.getElementById('prediction-reason').innerText = `${minItem.nom}`;
      document.getElementById('prediction-desc').innerText = `${minItem.raison}`;


    }
    else{
      document.getElementById('prediction-status').innerText = `Accepter`;
      const maxItem = data.find(item => item.valeur === Math.max(...data.map(i => i.valeur)))
      document.getElementById('prediction-reason').innerText = `${maxItem.nom}`;
      document.getElementById('prediction-desc').innerText = `${maxItem.raison}`;

    }
    });
    
  });

  document.addEventListener("DOMContentLoaded", function () {
    const imageElement = document.querySelector("#chart-container img");
    const changeBtn = document.getElementById("change-image-btn");

    const images = [
        "/static/image/analyse_impact_caracteristiques_simple.png",
        "/static/image/analyse_impact_caracteristiques.png"
    ];

    let currentImageIndex = 0;

    changeBtn.addEventListener("click", () => {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        imageElement.src = images[currentImageIndex];
    });
});
