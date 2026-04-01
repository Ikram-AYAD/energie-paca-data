"""
Prédiction de la consommation électrique en région PACA
---------------------------------------------------------
Suite du projet d'analyse (analyse_energie.py).
On ajuste un modèle de régression polynomiale (degré 2) sur l'ensemble
des données disponibles (2011-2024) pour capturer la forme en cloche
(montée jusqu'en 2017, baisse ensuite), puis on prédit 2025-2027.

Note méthodologique :
    Avec seulement 14 points de données annuelles, un découpage
    train/test classique n'est pas adapté. On évalue ici la qualité
    de l'ajustement sur l'ensemble des données (R² global), ce qui
    est la pratique standard pour les séries temporelles courtes.

Source des données : data.gouv.fr
Dataset : https://www.data.gouv.fr/fr/datasets/consommation-annuelle-delectricite-et-gaz-par-region/

Usage :
    Placer energie.csv sur le Bureau, puis lancer :
    python prediction_energie.py
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # moteur sans interface graphique — force la sauvegarde fichier
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error, r2_score

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
# Chemin du Bureau détecté automatiquement + fallback manuel
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
if not os.path.isdir(DESKTOP):
    DESKTOP = os.path.expanduser("~")  # fallback : dossier home

FILE_PATH    = os.path.join(DESKTOP, "energie.csv")
OUTPUT_PATH  = os.path.join(DESKTOP, "prediction_paca.png")
REGION_FILTRE = "Provence|PACA"
DEGRE         = 2

print(f"Bureau détecté  : {DESKTOP}")
print(f"CSV attendu     : {FILE_PATH}")
print(f"PNG sortie      : {OUTPUT_PATH}")

# ─── 1. CHARGEMENT ────────────────────────────────────────────────────────────
print("\nChargement du fichier...")
try:
    df = pd.read_csv(FILE_PATH, sep=None, engine='python', decimal=",")
except FileNotFoundError:
    print(f"Erreur : fichier introuvable à '{FILE_PATH}'")
    print("Vérifiez que 'energie.csv' est bien sur le Bureau.")
    sys.exit(1)

df.columns = [c.replace('"', '').strip() for c in df.columns]
print(f"{len(df)} lignes chargées.")

# ─── 2. DÉTECTION DES COLONNES ────────────────────────────────────────────────
def find_col(df, keywords):
    for key in sorted(keywords, key=len, reverse=True):
        for col in df.columns:
            if key.lower() in col.lower():
                return col
    return None

col_annee  = find_col(df, ['Année', 'annee', 'year'])
col_region = find_col(df, ['Nom Région', 'nom région', 'nom_region'])
col_conso  = find_col(df, ['Conso totale (MWh)', 'Conso totale'])

colonnes_manquantes = [nom for nom, col in
    [("Année", col_annee), ("Région", col_region), ("Consommation", col_conso)]
    if col is None]

if colonnes_manquantes:
    print(f"Erreur : colonnes introuvables : {colonnes_manquantes}")
    sys.exit(1)

# ─── 3. NETTOYAGE ─────────────────────────────────────────────────────────────
df[col_conso] = pd.to_numeric(
    df[col_conso].astype(str).str.replace(',', '.', regex=False),
    errors='coerce'
)
df = df.dropna(subset=[col_conso])

# ─── 4. FILTRAGE & AGRÉGATION ─────────────────────────────────────────────────
df_paca = df[df[col_region].str.contains(REGION_FILTRE, case=False, na=False)].copy()

if df_paca.empty:
    print(f"Erreur : aucune donnée pour '{REGION_FILTRE}'.")
    sys.exit(1)

stats = df_paca.groupby(col_annee)[col_conso].sum().sort_index()
print(f"{len(stats)} années disponibles : {list(stats.index)}")

# ─── 5. PRÉPARATION DES DONNÉES ───────────────────────────────────────────────
X = stats.index.values.reshape(-1, 1).astype(float)
y = stats.values

# ─── 6. MODÈLE POLYNOMIAL ─────────────────────────────────────────────────────
modele = make_pipeline(
    PolynomialFeatures(degree=DEGRE, include_bias=False),
    LinearRegression()
)
modele.fit(X, y)

# ─── 7. ÉVALUATION ────────────────────────────────────────────────────────────
y_pred_all = modele.predict(X)
mae = mean_absolute_error(y, y_pred_all)
r2  = r2_score(y, y_pred_all)

print(f"\nQualité d'ajustement (degré {DEGRE}) :")
print(f"  Score R²                     : {r2:.3f}")
print(f"  Erreur absolue moyenne (MAE) : {mae:,.0f} MWh")

# ─── 8. PRÉDICTION ANNÉES FUTURES ─────────────────────────────────────────────
annees_futures = np.array([2025, 2026, 2027]).reshape(-1, 1).astype(float)
y_pred_futures = modele.predict(annees_futures)
X_courbe       = np.linspace(X.min(), 2027, 300).reshape(-1, 1)
y_courbe       = modele.predict(X_courbe)

print(f"\nPrédictions futures :")
for annee, pred in zip([2025, 2026, 2027], y_pred_futures):
    print(f"  {int(annee)} → {pred/1e6:.2f} TWh")

# ─── 9. VISUALISATION ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(stats.index, stats.values / 1e6, 'o',
        color='steelblue', markersize=7, zorder=3,
        label='Consommation réelle (TWh)')

ax.plot(X_courbe.flatten(), y_courbe / 1e6, '--',
        color='tomato', linewidth=2,
        label=f'Régression polynomiale degré {DEGRE}')

ax.axvspan(2024.5, 2027.5, alpha=0.07, color='tomato', label='Années prédites')

for annee, pred in zip([2025, 2026, 2027], y_pred_futures):
    ax.plot(annee, pred / 1e6, 's', color='tomato', markersize=7, zorder=3)
    ax.annotate(f"{pred/1e6:.1f} TWh",
                xy=(annee, pred / 1e6),
                xytext=(0, 12), textcoords='offset points',
                ha='center', fontsize=8, color='tomato')

ax.set_title(
    f"Consommation électrique PACA — Ajustement polynomial (degré {DEGRE}) & Prédiction",
    fontsize=13, fontweight='bold', pad=15
)
ax.set_xlabel("Année", fontsize=11)
ax.set_ylabel("Consommation (TWh)", fontsize=11)
ax.legend(fontsize=9)
ax.grid(alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

textstr = f"R² = {r2:.3f}  (ajustement global)\nMAE = {mae/1e6:.2f} TWh"
ax.text(0.02, 0.97, textstr, transform=ax.transAxes,
        fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()

# Sauvegarde forcée avec chemin absolu
print(f"\nSauvegarde en cours : {OUTPUT_PATH}")
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches='tight')
plt.close()

# Vérification
if os.path.isfile(OUTPUT_PATH):
    taille = os.path.getsize(OUTPUT_PATH)
    print(f"Fichier créé avec succès ({taille/1024:.1f} Ko) : {OUTPUT_PATH}")
else:
    print("ERREUR : le fichier n'a pas été créé. Vérifiez les droits d'écriture.")
