document.getElementById('submit').addEventListener('click', function (event) {
    event.preventDefault();

    const login = document.getElementById('username').value;
    const mdp = document.getElementById('password').value;

    fetch('http://localhost:5000/verif-utilisateur', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, mdp })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Identifiants incorrects');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = '/prevision';
    })
    .catch(err => {
        alert(err.message);
        console.error('Erreur :', err);
    });
});
