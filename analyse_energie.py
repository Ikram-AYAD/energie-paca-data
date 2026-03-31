"""
Analyse de la consommation électrique en région PACA
-----------------------------------------------------
Source des données : data.gouv.fr - Consommation annuelle d'électricité par région
Dataset : https://www.data.gouv.fr/fr/datasets/consommation-annuelle-delectricite-et-gaz-par-region/

Usage :
    Placer le fichier energie.csv sur le Bureau, puis lancer :
    python analyse_energie.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
# Détection automatique du Bureau, quel que soit l'utilisateur Windows
DESKTOP       = os.path.join(os.path.expanduser("~"), "Desktop")
FILE_PATH     = os.path.join(DESKTOP, "energie.csv")
OUTPUT_PATH   = os.path.join(DESKTOP, "conso_paca.png")
REGION_FILTRE = "Provence|PACA"  # Filtre région (modifiable)

print(f"Bureau détecté : {DESKTOP}")
print(f"CSV attendu    : {FILE_PATH}")
print(f"PNG sortie     : {OUTPUT_PATH}")

# ─── 1. CHARGEMENT ────────────────────────────────────────────────────────────
print("\nChargement du fichier...")
try:
    df = pd.read_csv(FILE_PATH, sep=None, engine='python', decimal=",")
except FileNotFoundError:
    print(f"Erreur : fichier introuvable à '{FILE_PATH}'")
    print("Vérifiez que 'energie.csv' est bien sur le Bureau.")
    sys.exit(1)

# Nettoyage des noms de colonnes
df.columns = [c.replace('"', '').strip() for c in df.columns]
print(f"{len(df)} lignes chargées.")

# ─── 2. DÉTECTION DES COLONNES ────────────────────────────────────────────────
def find_col(df, keywords):
    """Retourne la colonne dont le nom contient le mot-clé le plus précis en premier."""
    for key in sorted(keywords, key=len, reverse=True):
        for col in df.columns:
            if key.lower() in col.lower():
                return col
    return None

col_annee  = find_col(df, ['Année', 'annee', 'year'])
col_region = find_col(df, ['Nom Région', 'nom région', 'nom_region'])
col_conso  = find_col(df, ['Conso totale (MWh)', 'Conso totale'])

print(f"\nColonnes identifiées :")
print(f"  Année        → {col_annee}")
print(f"  Région       → {col_region}")
print(f"  Consommation → {col_conso}")

# Vérification : arrêt propre si colonne manquante
colonnes_manquantes = [nom for nom, col in
    [("Année", col_annee), ("Région", col_region), ("Consommation", col_conso)]
    if col is None]

if colonnes_manquantes:
    print(f"\nErreur : colonnes introuvables : {colonnes_manquantes}")
    print(f"Colonnes disponibles : {list(df.columns)}")
    sys.exit(1)

# ─── 3. NETTOYAGE ─────────────────────────────────────────────────────────────
df[col_conso] = pd.to_numeric(
    df[col_conso].astype(str).str.replace(',', '.', regex=False),
    errors='coerce'
)

nb_avant = len(df)
df = df.dropna(subset=[col_conso])
nb_apres = len(df)
if nb_avant != nb_apres:
    print(f"Attention : {nb_avant - nb_apres} ligne(s) ignorée(s) (valeur manquante).")

# ─── 4. FILTRAGE RÉGION ───────────────────────────────────────────────────────
df_paca = df[df[col_region].str.contains(REGION_FILTRE, case=False, na=False)].copy()

if df_paca.empty:
    print(f"\nErreur : aucune donnée pour le filtre '{REGION_FILTRE}'.")
    print("Régions disponibles :")
    for r in sorted(df[col_region].dropna().unique()):
        print(f"  - {r}")
    sys.exit(1)

print(f"{len(df_paca)} lignes trouvées pour la région PACA.")

# ─── 5. AGRÉGATION ────────────────────────────────────────────────────────────
stats = df_paca.groupby(col_annee)[col_conso].sum().sort_index()

print("\nConsommation totale par année (MWh) :")
print(stats.to_string())

# ─── 6. VISUALISATION ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))

bars = ax.bar(stats.index.astype(str), stats.values, color='steelblue', edgecolor='white')

ax.set_title("Consommation électrique annuelle en région PACA",
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Année", fontsize=11)
ax.set_ylabel("Consommation (MWh)", fontsize=11)
plt.xticks(rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

for bar in bars:
    hauteur = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        hauteur * 1.01,
        f"{hauteur:,.0f}",
        ha='center', va='bottom', fontsize=7, color='dimgray'
    )

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)
print(f"\nGraphique sauvegardé sur le Bureau : {OUTPUT_PATH}")
plt.show()
