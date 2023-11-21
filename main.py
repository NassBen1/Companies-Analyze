import pandas as pd
import numpy as np
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






if __name__ == "__main__" :

    #Ouverture des fichiers et concaténation de tous les dataframes du dossier Data
    df = OpenDocsAndTagging("data")
