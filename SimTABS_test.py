import PerteEtGain
import SimTABS
from SimTABS import odefunction
from PerteEtGain import interpG
import numpy as np

with open("PerteEtGain.txt") as f_valeurs: 
    valeurs = np.loadtxt(f_valeurs)

# Séparation des donnée du fichier.txt
heure = valeurs[0, :]  #première ligne qui contient les heures de la journée 
flux_chaleur = valeurs[1, :] #deuxième ligne qui contient G(t)

t, G = interpG(heure, flux_chaleur)

T = np.array([50, 50, 50, 50, 50])
dT = odefunction(t, T, G)