//on prend le resultat de la prediction
fetch('/get_prediction')
  .then(res => res.json())
  .then(data => {
    //on l'affiche en le mettant sur un base d'un pourcentage sur 100
    x100 = data.prediction[0] * 100
    document.getElementById('prediction-percentage').innerText = `Prédiction : ${x100}%`;
    
    //on prend les analyse qui on été faite durant le prédiction
    fetch('/get_analyse')
    .then(res => res.json())
    .then(data => {
      //selon le pourcentage, on change les valeurs du dashboard
      if(x100 < 70){
      //mise a jour du status du prêt
      document.getElementById('prediction-status').innerText = `Refuser`;
      //on prend la caractéristique la plus dominante de la prédiction et on l'affiche
      const minItem = data.find(item => item.valeur === Math.min(...data.map(i => i.valeur)))
      document.getElementById('prediction-reason').innerText = `${minItem.nom}`;
      //on affiche l'explication de la prediction
      document.getElementById('prediction-desc').innerText = `${minItem.raison}`;


    }
    else{
      //mise a jour du status du prêt
      document.getElementById('prediction-status').innerText = `Accepter`;
      //on prend la caractéristique la plus dominante de la prédiction et on l'affiche
      const maxItem = data.find(item => item.valeur === Math.max(...data.map(i => i.valeur)))
      document.getElementById('prediction-reason').innerText = `${maxItem.nom}`;
      //on affiche l'explication de la prediction
      document.getElementById('prediction-desc').innerText = `${maxItem.raison}`;

    }
    });
    
  });

  //Pour changer le graphique en appuyant sur le boutton
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
