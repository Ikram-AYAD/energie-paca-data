# Analyse de la consommation électrique en région PACA
### Analysis of Electricity Consumption in the PACA Region

> ⚠️ **Travail personnel — © Ikram AYAD, 2025. Tous droits réservés.**
> Ce projet est un travail personnel réalisé et publié par Ikram AYAD.
> Toute reproduction, copie ou utilisation sans autorisation explicite est interdite.
>
> ⚠️ **Personal work — © Ikram AYAD, 2025. All rights reserved.**
> This project is a personal work created and published by Ikram AYAD.
> Any reproduction, copy or use without explicit permission is prohibited.

---

## 🇫🇷 Français

### Objectif

Analyser l'évolution de la consommation électrique annuelle en région
**Provence-Alpes-Côte d'Azur (PACA)** à partir des données officielles françaises,
en appliquant les étapes classiques d'un pipeline Data :
chargement → nettoyage → filtrage → agrégation → visualisation.

### Source des données

- **Jeu de données** : Consommation annuelle d'électricité et gaz par région
- **Fournisseur** : [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/consommation-annuelle-delectricite-et-gaz-par-region/)
- **Format** : CSV (~33 500 lignes, 40 colonnes)

### Résultat

![Consommation électrique PACA](conso_paca.png)

#### Observations

Les données couvrent la période **2011--2024** et révèlent plusieurs tendances :

- **Pic en 2016--2017** (~80 TWh) : probablement lié à des hivers rigoureux et à
  une forte part de chauffage électrique dans la région.
- **Tendance baissière depuis 2017** : cohérente avec les politiques nationales de
  sobriété énergétique et l'amélioration de l'efficacité des logements.
- **2024 au plus bas** (~60,7 TWh) : baisse de ~24% par rapport au pic de 2017.
- **2014 et 2018** : creux secondaires, potentiellement liés à des hivers doux.

### Installation

```bash
pip install pandas matplotlib
```

### Utilisation

1. Télécharger le dataset sur [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/consommation-annuelle-delectricite-et-gaz-par-region/)
2. Placer le fichier `energie.csv` sur le Bureau
3. Lancer :

```bash
python analyse_energie.py
```

Le graphique est automatiquement sauvegardé sur le Bureau sous `conso_paca.png`.

### Compétences mobilisées

- **Python** : pandas, matplotlib
- **Data** : chargement CSV, nettoyage, gestion des valeurs manquantes, agrégation
- **Visualisation** : graphique à barres annoté, export PNG automatique
- **Analyse** : lecture critique de tendances sur séries temporelles
- **Robustesse** : gestion d'erreurs, détection automatique de colonnes et de chemins

---

## 🇬🇧 English

### Objective

Analyze the evolution of annual electricity consumption in the
**Provence-Alpes-Côte d'Azur (PACA)** region using official French open data,
applying the classic steps of a Data pipeline:
loading → cleaning → filtering → aggregation → visualization.

### Data Source

- **Dataset**: Annual electricity and gas consumption by region
- **Provider**: [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/consommation-annuelle-delectricite-et-gaz-par-region/)
- **Format**: CSV (~33,500 rows, 40 columns)

### Output

![Electricity consumption PACA](conso_paca.png)

#### Key Findings

Data covers **2011--2024** and reveals several trends:

- **Peak in 2016--2017** (~80 TWh): likely driven by cold winters and a high share
  of electric heating in the region.
- **Downward trend since 2017**: consistent with national energy efficiency policies
  and improvements in building insulation.
- **2024 at its lowest** (~60.7 TWh): a ~24% drop compared to the 2017 peak.
- **2014 and 2018**: secondary dips, possibly linked to mild winters.

### Installation

```bash
pip install pandas matplotlib
```

### Usage

1. Download the dataset from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/consommation-annuelle-delectricite-et-gaz-par-region/)
2. Place `energie.csv` on the Desktop
3. Run:

```bash
python analyse_energie.py
```

The chart is automatically saved to the Desktop as `conso_paca.png`.

### Skills Demonstrated

- **Python**: pandas, matplotlib
- **Data**: CSV loading, cleaning, missing value handling, aggregation
- **Visualization**: annotated bar chart, automatic PNG export
- **Analysis**: critical reading of trends on time series
- **Robustness**: error handling, automatic column and path detection

---

*Projet personnel — Personal project | Ikram AYAD © 2025*
