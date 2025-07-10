import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import time
import re
import plotly.express as px
import streamlit.components.v1 as components
import os

# --- Cleaning functions ---
def clean_price(price_str):
    try:
        cleaned = re.sub(r'[^\d,\.]', '', price_str)
        cleaned = cleaned.replace(',', '.')
        return float(cleaned) if cleaned else None
    except:
        return None

def clean_address(address_str):
    try:
        return ' '.join(address_str.strip().split())
    except:
        return 'N/A'

def clean_cloth_type(cloth_str):
    try:
        return ' '.join(cloth_str.strip().split()).capitalize()
    except:
        return 'N/A'

# --- Scraping function ---
def scrape_data(link, number_page=50):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = []

    progress_text = f"Scraping en cours pour {link.split('/')[-1].replace('-', ' ')}..."
    my_bar = st.progress(0, text=progress_text)

    for p in range(1, number_page + 1):
        try:
            url = f'{link}?page={p}'
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = bs(response.text, "html.parser")
            containers = soup.find_all("div", class_="col s6 m4 l3")

            if not containers:
                st.info(f"Page {p} de {link.split('/')[-1].replace('-', ' ')} ne contient plus d'éléments. Arrêt du scraping pour cette catégorie.")
                break

            for container in containers:
                try:
                    cloth_type_elem = container.find('p', class_='ad__card-description')
                    cloth_type = clean_cloth_type(cloth_type_elem.a.text) if cloth_type_elem and cloth_type_elem.a else 'N/A'

                    price_elem = container.find('p', class_='ad__card-price')
                    price = clean_price(price_elem.a.text) if price_elem and price_elem.a else None

                    address_elem = container.find('p', class_='ad__card-location')
                    address = clean_address(address_elem.span.text) if address_elem and address_elem.span else 'N/A'

                    img_elem = container.find('a', class_='card-image ad__card-image waves-block waves-light')
                    image_link = urljoin(url, img_elem.img['src']) if img_elem and img_elem.img and 'src' in img_elem.img.attrs else 'N/A'

                    data.append({
                        "Type Habits": cloth_type,
                        "Prix": price,
                        "Adresse": address,
                        "Lien Image": image_link
                    })

                except AttributeError:
                    continue
                except Exception as e:
                    st.warning(f"Erreur lors du traitement d'un élément sur la page {p}: {e}")
                    continue

            time.sleep(1)
            my_bar.progress(p / number_page, text=f"Scraping en cours pour {link.split('/')[-1].replace('-', ' ')}... Page {p}/{number_page}")

        except requests.RequestException as e:
            st.error(f"Erreur de requête sur la page {p} pour {link}: {e}")
            break
        except Exception as e:
            st.error(f"Une erreur inattendue est survenue lors du scraping de la page {p} pour {link}: {e}")
            break
    my_bar.empty()

    df = pd.DataFrame(data)
    return df

# --- Application setup ---
LINKS_TO_SCRAPE = {
    "Vêtements Homme": "https://sn.coinafrique.com/categorie/vetements-homme",
    "Chaussures Homme": "https://sn.coinafrique.com/categorie/chaussures-homme",
    "Vêtements Enfants": "https://sn.coinafrique.com/categorie/vetements-enfants",
    "Chaussures Enfants": "https://sn.coinafrique.com/categorie/chaussures-enfants"
}

# Mapping for pre-scraped files to their display labels (for "Télécharger des données..." page)
PRE_SCRAPED_FILES_RAW = {
    "Vêtements Homme": "./data/vetements-homme.csv",
    "Chaussures Homme": "./data/chaussures-homme.csv",
    "Vêtements Enfants": "./data/vetements-enfant.csv",
    "Chaussures Enfants": "./data/chaussure-enfant.csv",
}

# Mapping for CLEANED files for the Dashboard
CLEANED_DASHBOARD_FILES = {
    "Vêtements Homme": "./data_cleaned/vetements-homme_cleaned.csv",
    "Chaussures Homme": "./data_cleaned/chaussures-homme_cleaned.csv",
    "Vêtements Enfants": "./data_cleaned/vetements-enfant_cleaned.csv",
    "Chaussures Enfants": "./data_cleaned/chaussure-enfant_cleaned.csv",
}

# Sidebar menu
page = st.sidebar.selectbox("Choisir une option", [
    "Scraper avec Beautiful Soup",
    "Télécharger des données déjà scrapées à travers Web Scraper",
    "Voir le Tableau de Bord", # This page will now load from data_cleaned
    "Remplir formulaire d'évaluation de l'app"
])

# --- Page: Scraper avec Beautiful Soup ---
if page == "Scraper avec Beautiful Soup":
    st.header("Scraper des données avec Beautiful Soup")
    st.info("Cette section vous permet de scraper des données en direct de Coinafrique. Cliquez sur un bouton pour scraper une catégorie spécifique.")

    number_pages = st.number_input(
        "Nombre de pages à scraper pour chaque catégorie (max 50, pour éviter de surcharger le serveur)",
        min_value=1,
        max_value=50,
        value=5
    )

    for label, link in LINKS_TO_SCRAPE.items():
        st.markdown(f"### Scraper les données pour : {label}")
        if st.button(f"Lancer le Scraping de {label}", key=f"scrape_button_{label.replace(' ', '_')}"):
            with st.spinner(f"Scraping en cours pour les {label.lower()}..."):
                scraped_df = scrape_data(link, number_pages)

                if not scraped_df.empty:
                    st.success(f"Scraping des {label.lower()} terminé avec succès. {len(scraped_df)} éléments trouvés.")
                    st.dataframe(scraped_df, use_container_width=True)

                    csv = scraped_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"Télécharger les données des {label.lower()} (CSV)",
                        data=csv,
                        file_name=f'donnees_{label.lower().replace(" ", "_")}.csv',
                        mime='text/csv',
                        key=f'download_scraped_{label.replace(" ", "_")}'
                    )
                else:
                    st.warning(f"Aucune donnée trouvée pour les {label.lower()} ou erreur de scraping.")
        st.markdown("---")

# --- Page: Télécharger des données déjà scrapées à travers Web Scraper (Raw Data) ---
elif page == "Télécharger des données déjà scrapées à travers Web Scraper":
    st.header("Télécharger des données déjà scrapées à travers Web Scraper")
    st.info("Ces données ont été préalablement scrapées et sont affichées ici pour visualisation et téléchargement.")

    if not os.path.exists('data'):
        st.error("Le dossier './data' est introuvable. Veuillez créer ce dossier et y placer les fichiers CSV bruts.")
        st.stop()

    for label, file_path in PRE_SCRAPED_FILES_RAW.items():
        st.markdown(f"### Données pour : {label}")
        if os.path.exists(file_path):
            try:
                df_raw = pd.read_csv(file_path)
                # Apply basic cleaning/renaming for display consistency if needed, but not full dashboard cleaning
                df_raw.columns = df_raw.columns.str.replace('_', ' ').str.title()
                column_mapping = {
                    'Price': 'Prix',
                    'Address': 'Adresse',
                    'Type': 'Type Habits',
                    'Image Link': 'Lien Image',
                }
                df_raw.rename(columns=column_mapping, inplace=True)

                st.dataframe(df_raw, use_container_width=True)

                csv_data = df_raw.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"Télécharger les données de {label} (CSV)",
                    data=csv_data,
                    file_name=f"{label.lower().replace(' ', '_')}_raw.csv",
                    mime='text/csv',
                    key=f"download_raw_{label.replace(' ', '_')}"
                )
            except pd.errors.EmptyDataError:
                st.warning(f"Le fichier '{file_path}' est vide. Aucune donnée à afficher.")
            except Exception as e:
                st.error(f"Erreur lors de la lecture ou du traitement du fichier '{file_path}': {e}")
        else:
            st.warning(f"Fichier brut non trouvé : '{file_path}'.")
        st.markdown("---")

# --- Page: Voir le Tableau de Bord (Displays Cleaned Data Separately) ---
elif page == "Voir le Tableau de Bord":
    st.header("Tableau de Bord des Données Nettoyées")
    st.info("Ce tableau de bord affiche les données nettoyées de chaque catégorie séparément, avec leurs analyses visuelles.")

    # Ensure the 'data_cleaned' directory exists
    if not os.path.exists('data_cleaned'):
        st.error("Le dossier './data_cleaned' est introuvable. Veuillez créer ce dossier et y placer les fichiers CSV nettoyés.")
        st.stop() # Stop execution if directory not found

    for label, file_path in CLEANED_DASHBOARD_FILES.items():
        st.markdown(f"## Analyse pour : {label}")
        if os.path.exists(file_path):
            try:
                df_cleaned = pd.read_csv(file_path)

                # Apply cleaning functions to ensure consistency
                df_cleaned.columns = df_cleaned.columns.str.replace('_', ' ').str.title()
                column_mapping = {
                    'Price': 'Prix',
                    'Address': 'Adresse',
                    'Type': 'Type Habits',
                    'Image Link': 'Lien Image',
                }
                df_cleaned.rename(columns=column_mapping, inplace=True)

                if 'Prix' in df_cleaned.columns:
                    df_cleaned['Prix'] = df_cleaned['Prix'].apply(clean_price)
                if 'Adresse' in df_cleaned.columns:
                    df_cleaned['Adresse'] = df_cleaned['Adresse'].apply(clean_address)
                if 'Type Habits' in df_cleaned.columns:
                    df_cleaned['Type Habits'] = df_cleaned['Type Habits'].apply(clean_cloth_type)

                if not df_cleaned.empty:
                    st.subheader("Aperçu des Données")
                    st.dataframe(df_cleaned, use_container_width=True)

                    st.subheader("Analyses Visuelles")

                    # Price Distribution (Histogram)
                    if 'Prix' in df_cleaned.columns and not df_cleaned['Prix'].isnull().all():
                        fig_hist = px.histogram(df_cleaned.dropna(subset=['Prix']), x="Prix", nbins=20, title=f"Distribution des Prix pour {label}")
                        st.plotly_chart(fig_hist)
                    else:
                        st.warning(f"Impossible de tracer la distribution des prix pour {label} : la colonne 'Prix' est manquante ou ne contient pas de données valides.")

                    # Type Habits Distribution (Pie Chart)
                    if 'Type Habits' in df_cleaned.columns and not df_cleaned['Type Habits'].isnull().all():
                        fig_pie = px.pie(df_cleaned, names="Type Habits", title=f"Répartition des Types d'Habits pour {label}", hole=0.3)
                        st.plotly_chart(fig_pie)
                    else:
                        st.warning(f"Impossible de tracer la répartition des types d'habits pour {label} : la colonne 'Type Habits' est manquante ou ne contient pas de données valides.")

                    # Address/Location Distribution (Bar Chart)
                    if 'Adresse' in df_cleaned.columns and not df_cleaned['Adresse'].isnull().all():
                        address_counts = df_cleaned['Adresse'].value_counts().reset_index()
                        address_counts.columns = ['Adresse', 'Nombre d\'annonces']
                        fig_bar = px.bar(address_counts, x='Adresse', y='Nombre d\'annonces', title=f"Nombre d'annonces par Adresse pour {label}",
                                         labels={'Adresse': 'Adresse', 'Nombre d\'annonces': 'Nombre d\'annonces'})
                        st.plotly_chart(fig_bar)
                    else:
                        st.warning(f"Impossible de tracer la répartition par adresse pour {label} : la colonne 'Adresse' est manquante ou ne contient pas de données valides.")


                    st.subheader("Télécharger les Données")
                    csv_data = df_cleaned.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"Télécharger les données nettoyées de {label} (CSV)",
                        data=csv_data,
                        file_name=f'{label.lower().replace(" ", "_")}_cleaned_dashboard.csv',
                        mime='text/csv',
                        key=f'download_dashboard_{label.replace(" ", "_")}'
                    )
                else:
                    st.warning(f"Le fichier nettoyé '{file_path}' est vide ou ne contient pas de données valides pour {label}.")

            except pd.errors.EmptyDataError:
                st.warning(f"Le fichier nettoyé '{file_path}' est vide. Aucune donnée à afficher pour {label}.")
            except Exception as e:
                st.error(f"Erreur lors du chargement ou du traitement du fichier nettoyé '{file_path}' : {e}")
        else:
            st.warning(f"Fichier nettoyé non trouvé : '{file_path}'. Impossible d'afficher le tableau de bord pour {label}.")
        st.markdown("---") # Separator between categories in dashboard

# --- Page: Remplir formulaire d'évaluation de l'app ---
elif page == "Remplir formulaire d'évaluation de l'app":
    st.header("Formulaire d'évaluation de l'application")
    st.write("Nous apprécions vos commentaires ! Veuillez remplir le formulaire ci-dessous pour nous aider à améliorer l'application.")

    components.html(
        """
        <iframe src="https://ee.kobotoolbox.org/i/lfXWSYVo" width="800" height="600"></iframe>
        """,
        height=620,
        width=820,
        scrolling=True
    )