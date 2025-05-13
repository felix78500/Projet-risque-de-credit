document.getElementById('submit').addEventListener('click', function (event) {
    event.preventDefault();
    //recuperation des champ
    const login = document.getElementById('username').value;
    const mdp = document.getElementById('password').value;

    //utilisation de la route api pour acceder a la bdd et verifier les champ
    fetch('http://localhost:5000/verif-utilisateur', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, mdp })
    })
    //message d'erreur si l'utilisateur n'existe pas
    .then(response => {
        if (!response.ok) {
            throw new Error('Identifiants incorrects');
        }
        return response.json();
    })
    //envoie a la page de prévision si l'utilisateur est dans la bdd
    .then(data => {
        window.location.href = '/prevision';
    })
    .catch(err => {
        alert(err.message);
        console.error('Erreur :', err);
    });
});
