import pandas as pd
import numpy as np
import plotly.express as px
import os
import re


def OpenDocsAndTagging(link):

    pattern = r"(.+)Products - Sheet1.csv"

    list_df = []

    for filename in os.listdir(link):
        if filename.endswith('.csv'):
            path = os.path.join(link,filename)
            df = pd.read_csv(path)
            match = re.match(pattern, filename)
            if match:
                # Ajouter le nom de l'entreprise extrait à la liste
                nom_entreprise = match.group(1)
                df["Brand"] = nom_entreprise
            list_df.append(df)
    merged_df = pd.concat(list_df, ignore_index=True)

    return merged_df

#Fonction qui pour chaque année de création, le nombre de produits encore actif
def CountActivePerYear(df) :
    # Filtrer les produits encore actifs
    active_products = df[df["Status"] == "Active"]

    # Compter le nombre de produits actifs pour chaque année
    active_products_count = active_products.groupby("Launch Year").size()
    active_products_count = active_products_count.reset_index(name='Number of Active Products')

    return active_products_count

#Affichage En barre d'active_products
def VisualisationEnBarre(data):

    fig = px.bar(data, x='Launch Year', y='Number of Active Products', labels={'Launch Year': 'Année de Lancement', 'Number of Active Products': 'Nombre de Produits Actifs'})
    fig.show()

#Fonction qui permet de trouver le produit avec la plus longue durée depuis son lancement
def LongestDurationProduct(df) :


    current_year = 2023  # Mise à jour avec l'année actuelle
    df = df[df['Launch Year'].astype(str).str.match(r'^\d{4}$')]
    df['Launch Year'] = df['Launch Year'].astype(int)
    df['Years Since Launch'] = current_year - df['Launch Year']
    longest_duration_product = df[df['Years Since Launch'] == df['Years Since Launch'].max()]
    print("\n\n Voici le produit le plus ancien :\n")
    print(longest_duration_product[['Product Name', 'Launch Year', 'Years Since Launch']])

#Fonction permettant la visualistaion des question posées à l'exercice 3
def Visualize(df) :

    #First Question
    df_brand_count = df.groupby('Brand')['Status'].count().reset_index()
    fig_bar = px.bar(df_brand_count, x='Brand', y='Status', title='Nombre de produits actifs par Marque')
    fig_bar.show()

    #Second Question
    df_brand_distribution = df['Brand'].value_counts().reset_index()
    df_brand_distribution.columns = ['Brand', 'Count']
    fig_pie = px.pie(df_brand_distribution, values='Count', names='Brand', title='Répartition des produits par Marque')
    fig_pie.show()

    #Last Question
    pivot_table = df.pivot_table(index='Launch Year', columns='Brand', values='Status', aggfunc='count').fillna(0)
    pivot_table_reset = pivot_table.reset_index()
    fig_bar_line = px.bar(pivot_table_reset, x='Launch Year', y=pivot_table_reset.columns[1:],
                          title='Répartition des produits actifs par année de lancement et par Marque')
    fig_bar_line.update_layout(barmode='stack')  # Mettre les barres en mode 'stack' pour les empiler
    fig_bar_line.show()


if __name__ == "__main__" :

    #Ouverture des fichiers et concaténation de tous les dataframes du dossier Data (Exercice 1)
    df = OpenDocsAndTagging("data")

    #Exercice 2
    #Afficher les premières lignes du dataframe
    print("Voici les premières lignes du nouveau Dataframe:\n")
    print(df.head())
    # Afficher le type des valeurs des colonnes
    print("Voici le type des valeurs des colonnes:\n")
    print(df.dtypes)

    #Compter le nombre de produits actifs pour chaque année de lancement. (Le mieux ici serait une visualisation que je vais effectuer en utilisant la librairie Plotly)
    active_products = CountActivePerYear(df)
    VisualisationEnBarre(active_products)

    #Appel de la fonction qui cherche le produit le plus vieux
    LongestDurationProduct(df)

    #Exercice 3
    Visualize(df)








