# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:49:18 2023

@author: marie
"""
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import geopandas as gpd


####################################
#      EVOLUTION SUR 50 ANS        #
####################################

# on va lire dans les 11 fichiers 
# On commence par créer trois DataFrame avec les années en index et en colonnes
# - le nombre d'exploitations pour chaque pôle (dataframe evol_n_exploit)
# - la sau totale pour chaque pôle (dataframe evol_sau_tot)
# - la sau moyenne pour chaque pôle (dataframe evol_sau_moy) : attention, la moyenne
# des sau n'est pas 
evol = pd.DataFrame(index = [1970, 1979, 1988, 2000, 2010, 2020])
evol_n_exploit = pd.DataFrame(index = [1970, 1979, 1988, 2000, 2010, 2020])
evol_sau_tot = pd.DataFrame(index = [1970, 1979, 1988, 2000, 2010, 2020])
evol_sau_moy = pd.DataFrame(index = [1970, 1979, 1988, 2000, 2010, 2020])

# Création d'une liste qui sera utilisée pour récupérer les noms des poles
# et les affecter aux noms des variables, à la fin dans chaque dataframe

listepole = []

# on lit dans chaque fichier du répertoire pour récupérer les informations
# sur le nombre d'exploitation, la sau tot et la sau moy 
# Le programme n'est pas trop commenté, mais à l'arrivée il y a un DataFrame evol
# qui contient tout, et des fichiers evol_n_exploit, evol_sau_tot et evol_sau_moy
# qui ne contiennent qu'une partie des info
# j'ai choisi de garder les infos sur ca_du_pays_basque, on peut aussi ne pas traiter
# cette modalité

listeDossiers = os.listdir('fichiersParPole')
for fichier in listeDossiers:
    pole = fichier[11:-1]
    df = pd.read_csv('fichiersParPole/' + fichier + '/evolution_n_exploit_sau-Tableau 1.csv',index_col = 0)
    # Mise à jour des noms de colonnes dans le dataframe df
    listepole.append(pole)
    listenom =[]
    for nom in df.columns : 
        listenom.append(f'{nom}_{pole}')
    df.columns = listenom
        
    df_n_exploit = df[listenom[0]]
    df_sau_tot = df[listenom[1]]
    df_sau_moy = df[listenom[2]]
    
    evol = pd.merge(evol, df, right_index=True, left_index=True)
    evol['n_exploit'] = df[listenom[0]]
    evol['sau_tot'] = df[listenom[1]]
    evol['sau_moy'] = df[listenom[1]]/df[listenom[0]]
    
    evol_n_exploit =  pd.merge(evol_n_exploit, df_n_exploit, right_index=True, left_index=True)
    evol_sau_tot = pd.merge(evol_sau_tot, df_sau_tot, right_index=True, left_index=True)
    evol_sau_moy = pd.merge(evol_sau_moy, df_sau_moy, right_index=True, left_index=True)
    

evol_n_exploit.columns = listepole
evol_sau_tot.columns = listepole
evol_sau_moy.columns = listepole

# Calcul des taux d'évolution sur la période 
# dans le DataFrame taux (attention il y a toujours ca_du_pays_basque)
taux = pd.DataFrame(index = listepole)
for ind in taux.index :
    max = evol_n_exploit.index[-1]
    min = evol_n_exploit.index[0]
    taux.loc[ind,'tx_n_exploit'] = (evol_n_exploit.loc[max,ind]-evol_n_exploit.loc[min,ind])/evol_n_exploit.loc[min,ind]
    max = evol_sau_tot.index[-1]
    min = evol_sau_tot.index[0]
    taux.loc[ind,'tx_sau_tot'] = (evol_sau_tot.loc[max,ind]-evol_sau_tot.loc[min,ind])/evol_sau_tot.loc[min,ind]
    max = evol_sau_moy.index[-1]
    min = evol_sau_moy.index[0]
    taux.loc[ind,'tx_sau_moy'] = (evol_sau_moy.loc[max,ind]-evol_sau_moy.loc[min,ind])/evol_sau_moy.loc[min,ind]


# Export
evol.to_csv('evol.csv', sep=";",encoding = 'utf-8', decimal = ",")
evol_n_exploit.to_csv('evol_n_exploit.csv', sep=";",encoding = 'utf-8', decimal = ",")
evol_sau_moy.to_csv('evol_sau_moy.csv', sep=";",encoding = 'utf-8', decimal = ",")
evol_sau_tot.to_csv('evol_sau_tot.csv', sep=";",encoding = 'utf-8', decimal = ",")
taux.to_csv('taux.csv', sep=";",encoding = 'utf-8', decimal = ",")

##############################
# Représentations graphiques #
##############################

# Nombre d'exploitations
evol_n_exploit[listepole].plot()

# Nombre d'exploitations - echelle logarithmique
evol_n_exploit[listepole].plot()
plt.yscale('log')
plt.grid(True,which="both", linestyle='--',axis = 'y')

# sau totale
evol_n_exploit[listepole].plot()

# Nombre d'exploitations - echelle logarithmique
evol_sau_tot[listepole].plot()
plt.yscale('log')
plt.grid(True,which="both", linestyle='--',axis = 'y')
