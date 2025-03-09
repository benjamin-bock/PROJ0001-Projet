# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 02:17:17 2025

@author: b3nja
"""

import numpy as np
import scipy as sp
import PerteEtGain as pg
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp as ode45 # Defining the solver (ode45)
from scipy.interpolate import interp1d


'''Signification des constantes
C = Capacité thermique spécifique (kJ/m²K)
    Ccc = de la partie centrale du béton
    Cc1 = de la partie supérieure du béton
    Cc2 = de la partie inférieure du béton
    Croom = de la pièce régulée
    Cw = de l'eau au sein des tubes

R = Résistance thermique (m²K/W)
    Rcc−c1 = entre la partie centrale et supérieure du béton
    Rx = entre les tubes et la partie centrale du béton
    Rc2−cc = entre la partie inférieure et centrale du béton
    Rr−s = entre la pièce régulée et la surface de contact
    Rs−c2 = entre la surface de contact et la partie inférieure du béton
    Rw = entre les tubes et l'eau circulant dans les tubes

Encodage des constantes

C =          [ 0,  1,  2,  3,    4 ]
C =          [cc, c1, c2, room,  w]'''  
C = np.array([50, 50, 10,  12  , 30])
C = C*1000 # kJ/m²K -> J/m²K
''' 
R =         [  0,    1    , 2,      3,     4,    5]
R =         [cc-c1,  x,   c2-cc,   r-s,  s-c2,   w]'''
R = np.array([0.05, 0.025 , 0.02  , 0.1, 0.183, 0.15]) 

nom_T = ["la pièce, T_room", "l'eau dans les tubes, T_t", "la partie centrale du béton, T_cc", "la partie supérieure du béton, T_c1", "la partie inférieure du béton, T_c2",] 

# Question 1 ##############################################################################################################

def odefunction(t, T, G):
    '''T = [  0,  1 , 2,  3,  4, 5]'''
    '''T = [room, t, cc, c1, c2, w]'''
    # Celsius -> Kelvin
    T = T + 273.15 
    
    '''Valeur de T_w'''
    if t <= 4 :
        T_w = 18 + 273.15
    else :
        T_w = 0
        
    # On place T_W en T[5]
    T = np.concatenate((T, T_w), axis=None)
    
    # Résolution du système ED
    dT = np.zeros(5)
    dT[0] = (-(T[0]-T[4]) / (R[3]+R[4]) + G(t)) / C[3] #(4)
    
    # Dernier terme annulé quand sys à l'arrêt
    if T[5] != 0 :
        dT[1] = (-(T[1] - T[2])/R[1] - (T[1]-T[5])/R[5]) / C[4] #(5)
    else : 
        dT[1] = (-(T[1] - T[2])/R[1]) / C[4] #(5)

    dT[2] = (-(T[2]-T[3])/R[0] - (T[2]-T[1])/R[1] + (T[4]-T[2])/R[2])/C[0] #(1)        
    dT[3] = (-(T[3]-T[2])/R[0]) / C[1] #(2)
    dT[4] = (-(T[4]-T[2])/R[2] + (T[0]-T[4])/(R[3]+R[4]))/C[2] #(3)
    
    # seconde -> heure
    dT = dT*3600
    
    return dT

# Question 2 #########################################################################################################

# Définition de la fonction
def calculTemperaturesEuler(tspan, T0, h, G):
    
    # Initialisation
    
    t = np.arange(tspan[0], tspan[-1] + h, h)
    n = len(t)
    T = np.zeros((5, n))
    T[:, 0] = T0
    
    # Méthode d'Euler
    for i in range(n-1):
        dT = odefunction(t[i], T[:, i], G)
        T[:, i+1] = T[: , i] + h * dT
    
    return [t, T]
 
# Résolution numérique

# Données   
T0 = np.array([15, 15, 15, 15, 15]) #T0 en °C
heure, flux_chaleur = pg.PerteEtGain()
t, G = pg.interpG(heure, flux_chaleur)
h = 0.01
t0 = 0 
tf = 24
tspan = [t0, tf]

Euler = calculTemperaturesEuler(tspan, T0, h, G)

plt.figure(figsize=(10, 6))
for k in range(len(T0)):
    plt.plot(Euler[0], Euler[1][k, :], 'o-', markersize=5, label="Euler") # Tracer Euler
plt.xlabel("Temps (h)")
plt.ylabel("Température finale de la pièce (°C)")
plt.title("Comparaison des résultats entre Euler et Runge-Kutta 45")


# Question 3 ##########################################################################################################

# Définition de la fonction
def calculTemperaturesIVP(tspan, T0, rtol, G):
    
    def system(t, T):
        return odefunction(t, T, G)
    
    solution = ode45(system, tspan, T0, method='RK45', rtol=rtol)
    return [solution.t, solution.y]

# Résolution numérique
tspan = [t[0], t[-1]]
rtol = 1e-10
IVP = calculTemperaturesIVP(tspan, T0, rtol, G)

for k in range(len(T0)):
    plt.plot(IVP[0], IVP[1][k, :], 'o-', markersize=5, label="RK45")
plt.grid(True)
plt.legend()
plt.show()
    
# Question 4 #############################################################################################################

def comparaisonEulerIVP(t_ref, T_ref, h_test) :
    
    # Stocker les erreurs pour chaque h
    errors = []
    
    for h in h_test:
        # Résolution avec Euler
        t_euler, T_euler = calculTemperaturesEuler(tspan, T0, h, G)
        
        # Interpolation de la solution référence sur les temps d'Euler
        T_ref_interp_func = interp1d(t_ref, T_ref, axis=1, kind='linear', fill_value="extrapolate")
        T_ref_interp = T_ref_interp_func(t_euler)   
        
        # Calcul de l'erreur
        error = np.mean(np.abs(T_euler - T_ref_interp))
        # On stocke chaque error dans errors
        errors.append(error)
    
    # Tracer l'erreur en fonction du pas de temps
    
    plt.figure(figsize=(10, 6))
    plt.plot(h_test, errors, 'o-', label="Erreur absolue moyenne")
    
    # Échelle logarithmique pour mieux visualiser la convergence
    plt.xscale('log')  
    plt.yscale('log')
    plt.xlabel("Pas de temps h (heures)")
    plt.ylabel("Erreur absolue moyenne (K)")
    plt.title("Détermination du pas de temps h optimal dans la méthode d'Euler")
    plt.legend()
    plt.grid()
    plt.show()
    
    '''Le graphique montre un décroissance d'erreur plus h diminue, ce qui est logique
    car l'approximation devient de plus en plus précise. Cependant, le graphe est représenté
    en échelle logarithmique et on remarque que la pente vaut environ 1. Ceci s'explique par
    le fait que la méthode d'Euler a un ordre de convergence de 1 {O(h)}. Il vient alors 
    de faire un compromis et choisir h=1e-2 qui est plus précis que 1e-1 et plus rapide que 1e-3'''

# Simulation

# Solution de référence IVP avec rtol = 1e-10
# Ceci va servir de base de comparaison pour Euler
t_ref, T_ref = calculTemperaturesIVP(tspan, T0, rtol, G)

# Valeurs candidates de h

h_test = [0.1, 0.05, 0.01, 0.005, 0.001]

comparaisonEulerIVP(t_ref, T_ref, h_test)

# Question 5 #############################################################################################

# Initialisation des constantes
max_jours = 100
jour = 0
h = 0.01

def simulation_etat_stationnaire(tspan, T0, G, h, max_jours) :
    

    # Initialisation des tableaux
    t_tot = np.array([])
    T_tot = np.zeros((5, 0))
    
    # Listes pour stocker t et T à chaque jour
    t_f = []  # Liste pour stocker les temps t de chaque jour
    T_f = []  # Liste pour stocker les températures T de chaque jour
    
    # Conditions initiales
    t_f.append(tspan[0])
    T_f.append(T0)
    
    # Stocke la température initiale de la pièce
    T_room_jour_prec = T0[0]
    
    # Simulation sur plusieurs jours consécutifs
    for jour in range(max_jours):
        
        # On résout l'EDO pour un jour
        Euler = calculTemperaturesEuler(tspan, T0, h, G)
        t = np.array(Euler[0]) # Temps
        T = np.array(Euler[1]) # Température
        
        # Mettre à jour T_room_jour_actuel
        T_room_jour = T[0, -1] 
        
        # Stocker t et T dans les listes
        t_f.append(t[-1] + jour * (tf-t0)) # On stocke tf à chaque fin de journée
        T_f.append(T[:, -1])          # On stocke T_room à chaque fin de journée
        
        # Ajouter les résultats à la simulation totale
        # Concatenate : t_tot[old] + t[new] = t_tot[old+new]
        t_tot = np.concatenate((t_tot, t + jour * 24), axis = None) # Ajouter le temps en heures
        T_tot = np.concatenate((T_tot, T), axis = 1)
        '''Pourquoi axis=1 ? Car la concaténation se fait horizontalement (axis=0 : verticalement)
        
        T_tot = ([T1, :]  on aimerait ajouter T à droite de la colonne T_tot
                 [T2, :]
                 [T3, :]
                 [T4, :]
                 [T5, :])
        
        
        Les dernières valeurs de T deviennent les conditions initales pour la prochaine itération'''
        T0 = T[:, -1]
        
        # Vérifier les conditions d'état stationnaire
        if jour >= 1:
            # t va de 0 à 24 mais possède n éléments 
            # -> On utilise len(t) en toute généralité
            diff_T = abs(T_room_jour - T_room_jour_prec) # Compare T_room en fin de journée vs T_room 24h auparavant
            
            # Condition de stationnarité
            if diff_T < 0.01 :
                print("État stationnaire atteint après",jour + 1,"jours.")
                break
        
        # Mettre à jour la température de référence pour le prochain jour
        T_room_jour_prec = T_room_jour
            
    return t_f, T_f, jour+1

t_f, T_f, jour = simulation_etat_stationnaire(tspan, T0, G, h, max_jours)
    
        
# Visualisation
t_f = np.array(t_f)/(tf-t0)
T_f = np.array(T_f)
plt.figure(figsize=(10, 6))
plt.plot(t_f, T_f[:, 0], 'o-', markersize=5, label="T_room") # Tracer 
plt.plot(t_f, T_f[:, 4], 'o-', markersize=5, label="T_c2") # Tracer T_c2
plt.xlabel("Temps (jours)")
plt.ylabel("Température finale de la pièce (°C)")
plt.title("Convergence vers l'état stationnaire")
plt.grid(True)
plt.legend()
plt.show()
    
# Question 6 #########################################################################################################

# Stocke les variables
t_f1 = t_f
T_f1 = T_f 

'''Comparons les 3 scénarios'''

for j in range(len(T0)): #On affiche chaque T[:]
    
    # Scénario 1 (voir question 5) ##############################################
    
    plt.figure(figsize=(10, 6))
    plt.plot(t_f1, T_f1[:, j], 'o-', markersize=5, label="Scénario 1")
    plt.xlabel("Temps (jours)")
    plt.ylabel(f"Température finale de {nom_T[j]} (°C)")
    plt.grid(True)
    
    # Scnéario 2 ##############################################################
    
    def scenario2(tspan, T0, G, h, jour) :
        
        def odefunction2(t, T, G):
            '''T = [  0,  1 , 2,  3,  4, 5]'''
            '''T = [room, t, cc, c1, c2, w]'''
            # Celsius -> Kelvin
            T = T + 273.15 
            
            '''Valeur de T_w'''
            if t <= 4 :
                T_w = 18 + 273.15
            elif 4 < t <= 13 :
                T_w = 28 + 273.15
            else :
                T_w = 0
                
            # On place T_w en T[5]
            T = np.concatenate((T, T_w), axis=None)
            
            # Résolution du système ED
            dT = np.zeros(5)
            dT[0] = (-(T[0]-T[4]) / (R[3]+R[4]) + G(t)) / C[3]
            
            # Dernier terme annulé quand sys à l'arrêt
            if T[5] != 0 :
                dT[1] = (-(T[1] - T[2])/R[1] - (T[1]-T[5])/R[5]) / C[4]
            else : 
                dT[1] = (-(T[1] - T[2])/R[1]) / C[4]
    
            dT[2] = (-(T[2]-T[3])/R[0] - (T[2]-T[1])/R[1] + (T[4]-T[2])/R[2])/C[0]           
            dT[3] = (-(T[3]-T[2])/R[0]) / C[1]
            dT[4] = (-(T[4]-T[2])/R[2] + (T[0]-T[4])/(R[3]+R[4]))/C[2]
            
            # seconde -> heure
            dT = dT*3600
            
            return dT
        
        def calculTemperaturesEuler2(tspan, T0, h, G):
            
            # Initialisation
            
            t = np.arange(tspan[0], tspan[-1] + h, h)
            n = len(t)
            T = np.zeros((5, n))
            T[:, 0] = T0
            
            # Méthode d'Euler
            for i in range(n-1):
                dT = odefunction2(t[i], T[:, i], G)
                T[:, i+1] = T[: , i] + h * dT
            
            return [t, T]
        
        def simulation_scenario2(tspan, T0, G, h, jour) :
            
            # Listes pour stocker t et T à chaque jour
            t_f = []  # Liste pour stocker les temps t de chaque jour
            T_f = []  # Liste pour stocker les températures T de chaque jour
            
            # Conditions initiales
            t_f.append(tspan[0])
            T_f.append(T0)
            
            # Simulation sur plusieurs jours consécutifs
            for day in range(jour):
                
                # On résout l'EDO pour un jour
                Euler = calculTemperaturesEuler2(tspan, T0, h, G)
                t = np.array(Euler[0]) # Temps
                T = np.array(Euler[1]) # Température
                
                # Stocker t et T dans les listes
                t_f.append(t[-1] + day * 24) # On stocke tf à chaque fin de journée
                T_f.append(T[:, -1])         # On stocke T à chaque fin de journée
                  
                #Les dernières valeurs de T deviennent les conditions initales pour la prochaine itération
                T0 = T[:, -1]
                    
            return t_f, T_f
    
        t_f, T_f = simulation_scenario2(tspan, T0, G, h, jour)
    
        return t_f, T_f
    
    # Simulation
    t_f, T_f = scenario2(tspan, T0, G, h, jour)
    
    # Représenation graphique
    t_f2 = np.array(t_f)/(tf-t0)
    T_f2 = np.array(T_f)
    plt.plot(t_f2, T_f2[:, j], 'o-',  markersize=5, label="Scénario 2")
    
    
    # Scnéario 3 ################################################################
    
    def scenario3(tspan, T0, G, h, jour) :
        
        def odefunction3(t, T, G):
            '''T = [  0,  1 , 2,  3,  4, 5]'''
            '''T = [room, t, cc, c1, c2, w]'''
            # Celsius -> Kelvin
            T = T + 273.15 
            
            '''Valeur de T_w'''
            if t <= 12 :
                T_w = 28 + 273.15
            else :
                T_w = 18 + 273.15
                
            # On place T_w en T[5]
            T = np.concatenate((T, T_w), axis=None)
            
            # Résolution du système ED
            dT = np.zeros(5)
            dT[0] = (-(T[0]-T[4]) / (R[3]+R[4]) + G(t)) / C[3]
            
            # Dernier terme annulé quand sys à l'arrêt
            if T[5] != 0 :
                dT[1] = (-(T[1] - T[2])/R[1] - (T[1]-T[5])/R[5]) / C[4]
            else : 
                dT[1] = (-(T[1] - T[2])/R[1]) / C[4]
    
            dT[2] = (-(T[2]-T[3])/R[0] - (T[2]-T[1])/R[1] + (T[4]-T[2])/R[2])/C[0]           
            dT[3] = (-(T[3]-T[2])/R[0]) / C[1]
            dT[4] = (-(T[4]-T[2])/R[2] + (T[0]-T[4])/(R[3]+R[4]))/C[2]
            
            # seconde -> heure
            dT = dT*3600
            
            return dT
        
        def calculTemperaturesEuler3(tspan, T0, h, G):
            
            # Initialisation
            
            t = np.arange(tspan[0], tspan[-1] + h, h)
            n = len(t)
            T = np.zeros((5, n))
            T[:, 0] = T0
            
            # Méthode d'Euler
            for i in range(n-1):
                dT = odefunction3(t[i], T[:, i], G)
                T[:, i+1] = T[: , i] + h * dT
            
            return [t, T]
        
        def simulation_scenario3(tspan, T0, G, h, jour) :
            
            # Listes pour stocker t et T à chaque jour
            t_f = []  # Liste pour stocker les temps t de chaque jour
            T_f = []  # Liste pour stocker les températures T de chaque jour
            
            # Conditions initiales
            t_f.append(tspan[0])
            T_f.append(T0)
            
            # Simulation sur plusieurs jours consécutifs
            for day in range(jour):
                
                # On résout l'EDO pour un jour
                Euler = calculTemperaturesEuler3(tspan, T0, h, G)
                t = np.array(Euler[0]) # Temps
                T = np.array(Euler[1]) # Température
                
                # Stocker t et T dans les listes
                t_f.append(t[-1] + day * 24) # On stocke tf à chaque fin de journée
                T_f.append(T[:, -1])         # On stocke T à chaque fin de journée
                  
                #Les dernières valeurs de T deviennent les conditions initales pour la prochaine itération
                T0 = T[:, -1]
                    
            return t_f, T_f
    
        t_f, T_f = simulation_scenario3(tspan, T0, G, h, jour)
    
        return t_f, T_f
    
    # Simulation
    t_f, T_f = scenario3(tspan, T0, G, h, jour)
    
    # Représenation graphique
    t_f3 = np.array(t_f)/(tf-t0)
    T_f3 = np.array(T_f)
    plt.plot(t_f3, T_f3[:, j], 'o-',  markersize=5, label="Scénario 3")
    
    # On affiche les graphes
    plt.legend()
    plt.show()
    
    
    






