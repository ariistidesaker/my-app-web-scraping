# Application de Scraping et d'Analyse de Données de Coinafrique

Bienvenue dans l'application de scraping et d'analyse de données de Coinafrique ! Cette application Streamlit vous permet de récupérer des données en temps réel depuis le site Coinafrique.sn, de consulter des données pré-scrapées et nettoyées, de visualiser des tableaux de bord interactifs pour chaque catégorie de vêtements et chaussures, et même de fournir des retours via un formulaire d'évaluation.

## Fonctionnalités Clés

- **Scraping en Temps Réel avec Beautiful Soup** : Récupérez des données fraîches pour diverses catégories (vêtements homme, chaussures homme, vêtements enfants, chaussures enfants) directement depuis Coinafrique.sn. Vous pouvez spécifier le nombre de pages à scraper pour chaque catégorie.
- **Téléchargement de Données Pré-scrapées** : Accédez à des jeux de données bruts, déjà collectés via Web Scraper, pour les mêmes catégories. Ces données peuvent être visualisées sous forme de tableaux et téléchargées individuellement.
- **Tableaux de Bord Interactifs (Données Nettoyées)** : Explorez des visualisations complètes (histogrammes de prix, diagrammes circulaires de types d'habits, diagrammes en bandes d'adresses) pour chaque catégorie, basées sur des données pré-nettoyées. Chaque ensemble de données est présenté séparément pour une analyse détaillée.
- **Formulaire d'Évaluation de l'Application** : Partagez vos commentaires et suggestions via un formulaire intégré pour nous aider à améliorer l'application.

## Comment Utiliser l'Application

### Prérequis

- Assurez-vous d'avoir Python installé (version 3.7 ou supérieure recommandée).
- Installez les bibliothèques Python nécessaires en exécutant :

```bash
pip install streamlit pandas requests beautifulsoup4 plotly
```

### Structure des Dossiers

- Créez un dossier nommé `data` dans le même répertoire que votre script `app.py` (ou quel que soit le nom de votre fichier Streamlit). Ce dossier accueillera les fichiers CSV bruts pré-scrapés.
- Créez un autre dossier nommé `data_cleaned` dans le même répertoire. Ce dossier contiendra les fichiers CSV nettoyés utilisés pour les tableaux de bord.
- Vos fichiers doivent être nommés comme suit dans le dossier `data` :
  - `chaussure-enfant.csv`
  - `chaussures-homme.csv`
  - `vetements-enfant.csv`
  - `vetements-homme.csv`
- Vos fichiers nettoyés doivent être nommés comme suit dans le dossier `data_cleaned` :
  - `chaussure-enfant_cleaned.csv`
  - `chaussures-homme_cleaned.csv`
  - `vetements-enfant_cleaned.csv`
  - `vetements-homme_cleaned.csv`

### Lancer l'Application

1. Naviguez vers le répertoire de votre projet dans votre terminal ou invite de commandes.
2. Exécutez la commande :

```bash
streamlit run app.py
```

(Remplacez `app.py` par le nom réel de votre fichier Python.)

### Navigation dans l'Application

- Une fois lancée, l'application s'ouvrira dans votre navigateur web.
- Utilisez le menu latéral (barre latérale gauche) pour naviguer entre les différentes sections :
  - **Scraper avec Beautiful Soup** : Lancez de nouvelles sessions de scraping.
  - **Télécharger des données déjà scrapées à travers Web Scraper** : Visualisez et téléchargez les données brutes pré-existantes.
  - **Voir le Tableau de Bord** : Explorez les analyses visuelles des données nettoyées, présentées par catégorie.
  - **Remplir formulaire d'évaluation de l'app** : Accédez au formulaire de feedback.

## Structure du Projet (Exemple)

```
.
├── app.py
├── data/
│   ├── chaussure-enfant.csv
│   ├── chaussures-homme.csv
│   ├── vetements-enfant.csv
│   └── vetements-homme.csv
└── data_cleaned/
    ├── chaussure-enfant_cleaned.csv
    ├── chaussures-homme_cleaned.csv
    ├── vetements-enfant_cleaned.csv
    └── vetements-homme_cleaned.csv
```

## Lien de l'application
[text](https://coin-afrique-scraper.streamlit.app/)