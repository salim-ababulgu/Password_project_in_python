# Importation du module tkinter pour créer une interface graphique
import tkinter as tk
from tkinter import messagebox
import re
import hashlib
import json
import random

# Fonction pour vérifier si le mot de passe respecte les exigences de sécurité
def verify_password(password):
    # Vérifier la longueur du mot de passe
    if len(password) < 8:
        return False, "Il doit contenir au moins 8 caractères."
    # Vérifier s'il contient au moins une lettre majuscule
    if not any(char.isupper() for char in password):
        return False, "Il doit contenir au moins une lettre majuscule."
    # Vérifier s'il contient au moins une lettre minuscule
    if not any(char.islower() for char in password):
        return False, "Il doit contenir au moins une lettre minuscule."
    # Vérifier s'il contient au moins un chiffre
    if not any(char.isdigit() for char in password):
        return False, "Il doit contenir au moins un chiffre."
    # Vérifier s'il contient au moins un caractère spécial
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Il doit contenir au moins un caractère spécial (!, @, #, $, %, ^, &, *)."
    # Si toutes les conditions sont satisfaites, le mot de passe est valide
    return True, ""

# Fonction pour crypter un mot de passe avec SHA-256
def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

# Fonction pour charger les mots de passe enregistrés depuis un fichier JSON
def load_passwords():
    try:
        with open("passwords.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Fonction pour enregistrer un mot de passe haché dans un fichier JSON
def save_password(username, password_hash):
    passwords = load_passwords()
    # Vérifier si le mot de passe est déjà enregistré
    for entry in passwords:
        if entry['password_hash'] == password_hash:
            return False
    passwords.append({"username": username, "password_hash": password_hash})
    with open("passwords.json", "w") as file:
        json.dump(passwords, file)
    return True

# Fonction pour vérifier si un mot de passe est déjà enregistré
def is_password_registered(password):
    hashed_password = hash_password(password)
    passwords = load_passwords()
    for entry in passwords:
        if entry['password_hash'] == hashed_password:
            return True
    return False

# Fonction pour générer un mot de passe aléatoire qui respecte les exigences
def generate_random_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    while True:
        password = ''.join(random.choice(characters) for i in range(12))
        if verify_password(password)[0] and not is_password_registered(password):
            return password

# Fonction pour gérer la soumission du formulaire
def submit_form():
    username = username_entry.get()
    password = password_entry.get()
    is_valid, error_message = verify_password(password)
    if is_valid:
        hashed_password = hash_password(password)
        if save_password(username, hashed_password):
            success_label = tk.Label(center_frame, text="Mot de passe enregistré avec succès.", fg="green", bg="#000")
            success_label.pack(pady=5) # Ajouter un label de succès avec la couleur verte
            root.after(5000, root.destroy)  # Fermer la fenêtre après 5 secondes
        else:
            error_message_label.config(text="Ce mot de passe est déjà enregistré.", fg="yellow")
    else:
        error_label.config(text=error_message, fg="red")

# Fonction pour générer et afficher un mot de passe aléatoire
def generate_and_show_random_password():
    random_password = generate_random_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, random_password)

# Fonction pour dévoiler ou cacher le mot de passe
def toggle_password_visibility():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_button.config(text="Cacher le mot de passe")
    else:
        password_entry.config(show="*")
        toggle_button.config(text="Dévoiler le mot de passe")

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Gestionnaire de mots de passe")
root.geometry("500x500")
root.configure(bg="#000")

# Frame pour centrer le contenu
center_frame = tk.Frame(root, bg="#000", padx=5, pady=5)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Création des éléments de l'interface
error_message_label = tk.Label(center_frame, text="", fg="yellow", bg="#000")
error_message_label.pack(pady=(25, 5))  # Marge de 25px en bas du message d'erreur

username_label = tk.Label(center_frame, text="Nom d'utilisateur:", fg="#fff", bg="#000")
username_label.pack(pady=(0, 5))  # Marge de 5px en bas du label

username_entry = tk.Entry(center_frame)
username_entry.pack(pady=(5, 5))  # Marge de 5px en bas de l'entrée de l'utilisateur

password_label = tk.Label(center_frame, text="Mot de passe:", fg="#fff", bg="#000")
password_label.pack(pady=(25, 5))  # Marge de 25px en bas du label Mot de passe

password_entry = tk.Entry(center_frame, show="*")
password_entry.pack(pady=(0, 5))  # Marge de 5px en bas de l'entrée du mot de passe

# Bouton pour dévoiler ou cacher l  e mot de passe
toggle_button = tk.Button(center_frame, text="Dévoiler le mot de passe", command=toggle_password_visibility, bg="#fff")
toggle_button.pack(pady=(5, 5))  # Marge de 5px en bas du bouton de dévoilement de mot de passe

generate_password_button = tk.Button(center_frame, text="Générer un mot de passe aléatoire", command=generate_and_show_random_password, bg="#fff")
generate_password_button.pack(pady=(25, 5))  # Marge de 5px en bas du bouton de génération de mot de passe aléatoire

submit_button = tk.Button(center_frame, text="Valider", command=submit_form, bg="#fff")
submit_button.pack(pady=(25, 0))  # Marge de 50px en bas du bouton Valider

error_label = tk.Label(center_frame, text="", fg="red", bg="#000")
error_label.pack(pady=(0, 5))  # Marge de 5px en bas du label d'erreur

# Lancer l'interface
root.mainloop()
