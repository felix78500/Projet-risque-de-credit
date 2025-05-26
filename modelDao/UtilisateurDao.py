import os
from supabase import create_client, Client

# Définir les clés d'environnement (faites ceci une fois, ou configurez-les dans votre système)
os.environ["SUPABASE_URL"] = "https://xcpqafebvepowoxxppsd.supabase.co"
os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjcHFhZmVidmVwb3dveHhwcHNkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NDEwNzc2NiwiZXhwIjoyMDU5NjgzNzY2fQ.66tUU4BoxxJ8KXcsrbstY3j8Jm38f-M8MadlycAdwUY"

# Récupérer l'URL et la clé à partir des variables d'environnement
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Créer le client Supabase
supabase: Client = create_client(url, key)

class UtilisateurDao:
    def __init__(self):
        print("Instance de UtilisateurDao créée.")

    # Inserer un l'utilisateur
    def insert_user(self, login, mdp):
        print("Insertion de donnée user :"+login, mdp)
        data = {"login" : login, "mdp" : mdp} 
        response = supabase.table("Utilisateur").insert(data).execute()
        print(response.data)
        return response.data
 
    # Permet de verifier si l'utilisateur existe dans la bdd 
    # (utile lorsque il faut verifier l'existant d'un utilisateur)
    def verif_user(self, user_a_verif, user_mdp_a_verif):
        print("verif de la donnée user")
        response = supabase.table("Utilisateur").select("login", "mdp").eq("login", user_a_verif).eq("mdp", user_mdp_a_verif).execute()
        print(response.data)
        if response.data and len(response.data)>0:
            print(True)
            return True
        else :
            print(False)
            return False