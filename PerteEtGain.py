import numpy as np
import matplotlib.pyplot as plt 
from scipy.interpolate import CubicSpline

# QUESTION 1 ################################################################################################################

''' Fichier qui contient: première ligne(heure de la journée ), Deuxième ligne(flux de chaleur)
 ouvrir un fichier en lecture (par défaut) et à gérer automatiquement la fermeture 
 du fichier lorsque le bloc de code est terminé. C'est une façon pratique et sécurisée
 de manipuler les fichiers en Python.'''
 
def PerteEtGain():
    with open("PerteEtGain.txt") as f_valeurs: 
        valeurs = np.loadtxt(f_valeurs)

    # Séparation des donnée du fichier.txt
    heure = valeurs[0, :]  #première ligne qui contient les heures de la journée 
    flux_chaleur = valeurs[1, :] #deuxième ligne qui contient G(t)
    return heure, flux_chaleur

heure, flux_chaleur = PerteEtGain()

# QUESTION 2 ################################################################################################################

'''On interpole les données à l'aide d'une spline
 cubique car les données sont successivement 
 décroissantes, croissantes et de nouveau décroissantes'''

# La fonction prend en argument un liste 
# heure et flux_chaleur 

def interpG(heure, flux_chaleur):
    
    ''' On crée une liste t de 400 éléments pour
    avoir une pseudo-continuité entre le 
    début et la fin de heure'''
    t = np.linspace(heure[0], heure[-1], 400) #[-1] indexation négative : permet de pointer le dernier élément sans connaître la taille de la liste
    g = CubicSpline(heure, flux_chaleur, bc_type='not-a-knot')
    return t, g

# QUESTION 3 ################################################################################################################

# On appelle interpG pour stocker les valeurs dans t et G
t, g = interpG(heure, flux_chaleur)

plt.figure(figsize=(10, 6))  # Définit une taille pour éviter les problèmes d'affichage
plt.xticks(np.linspace(t[0], t[-1], 9))  # Divise la grille en 8 parts verticales égales
plt.plot(heure, flux_chaleur, 'o', label = "Données initiales" )
plt.plot(t, g(t), label = "Interpolation par spline cublique"  )
plt.title("Évolution du flux de chaleur, G(t), en fonction du moment de la journée", fontsize=22)
plt.grid(True)
plt.xlabel("Heure (h)", fontsize=22)
plt.ylabel("Flux de chaleur (W/m²)", fontsize=22)
plt.legend(fontsize=22)
plt.show()

def G(t):
    return g(t)
