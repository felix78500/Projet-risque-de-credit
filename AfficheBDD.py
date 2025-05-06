import tkinter as tk
from tkinter import ttk
import requests

SUPABASE_URL = 'https://xcpqafebvepowoxxppsd.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhjcHFhZmVidmVwb3dveHhwcHNkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NDEwNzc2NiwiZXhwIjoyMDU5NjgzNzY2fQ.66tUU4BoxxJ8KXcsrbstY3j8Jm38f-M8MadlycAdwUY'
TABLE_NAME = "Utilisateur"

def get_data():
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

#Interface Tkinter
def create_table(data):
    root = tk.Tk()
    root.title("Données Supabase")

    if not data:
        tk.Label(root, text="Aucune donnée trouvée.").pack()
        root.mainloop()
        return

    columns = list(data[0].keys())

    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for row in data:
        values = [row[col] for col in columns]
        tree.insert("", tk.END, values=values)

    root.mainloop()

if __name__ == "__main__":
    try:
        data = get_data()
        create_table(data)
    except Exception as e:
        print("Erreur :", e)