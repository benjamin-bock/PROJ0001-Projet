import numpy as np
import scipy as sp
import PerteEtGain as pg
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp as ode45 # Defining the solver (ode45)

'''Signification des constantes
C = Capacité thermique spécifique (J/m²K)
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
    dT[0] = (-(T[0]-T[4]) / (R[3]+R[4]) + G(t)) / C[3]
    
    # Dernier terme annulé quand sys à l'arrêt
    if T[5] != 0 :
        dT[1] = (-(T[1] - T[2])/R[1] - (T[1]-T[5])/R[5]) / C[4]
    else : 
        dT[1] = (-(T[1] - T[2])/R[1]) / C[4]

    dT[2] = (-(T[2]-T[3])/R[0] - (T[2]-T[1])/R[1] - (T[4]-T[2])/R[2])/C[0]           
    dT[3] = (-(T[3]-T[2])/R[0]) / C[1]
    dT[4] = (-(T[4]-T[2])/R[2] + (T[0]-T[4])/(R[3]+R[4]))/C[2]
    
    # seconde -> heure
    dT = dT*3600
    
    return dT

# Question 2 #########################################################################################################

# Définition de la fonction
def calculTemperaturesEuler(t, T0, h, G):
    
    # Initialisation
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
T0 = np.array([15, 15, 15, 15, 15])
T0 = T0 + 273.15
heure, flux_chaleur = pg.PerteEtGain()
t, G = pg.interpG(heure, flux_chaleur)
h = 0.01

Euler = calculTemperaturesEuler(t, T0, h, G)

# Question 3 ##########################################################################################################

# Définition de la fonction
def calculTemperaturesIVP(t, T0, rtol, G):
    
    def system(t, T):
        return odefunction(t, T, G)
    solution = ode45(system, tspan, T0, method='RK45', rtol=rtol)
    return [solution.t, solution.y]

# Résolution numérique
tspan = [t[0], t[-1]]
rtol = 1e-10
IVP = calculTemperaturesIVP(t, T0, rtol, G)
    
# Question 4 #############################################################################################################

# Solution de référence IVP avec rtol = 1e-10
# Ceci va servir de base de comparaison pour Euler
t_ref, T_ref = calculTemperaturesIVP(tspan, T0, rtol, G)

# Valeurs candidates de h

h_test = [0.1, 0.05, 0.01, 0.005, 0.001]

# Stocker les erreurs pour chaque h
errors = []

for h in h_test:
    # Résolution avec Euler
    t_euler, T_euler = calculTemperaturesEuler(tspan, T0, h, G)
    
    # Interpolation de la solution référence sur les temps d'Euler
    T_ref_interp = np.array([np.interp(t_euler, t_ref, T_ref[i, :]) for i in range(5)])   
    
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
plt.ylabel("Erreur absolue moyenne")
plt.title("Détermination du pas de temps h optimal dans la méthode d'Euler")
plt.legend()
plt.grid()
plt.show()

'''Le graphique montre un décroissance d'erreur plus h diminue, ce qui est logique
car l'approximation devient de plus en plus précise. Cependant, le graphe esr représenté
en échelle logarithmique et on remarque que même pour des valeurs de h très petite
l'erreur ne décroît pas aussi signiicativement. Il vient alors de faire un compromis
et choisir h=1e-2 qui est plus précis que 1e-1 et plus rapide que 1e-3'''


# Question 5 #############################################################################################

# Initialisation des constantes
max_jours = 100
jour = 1
h = 0.01

def simulation_etat_stationnaire(tspan, T0, G, h, max_jours) :
    

    # Initialisation des tableaux
    t_tot = np.array([])
    T_tot = np.zeros((5, 0))
    
    # Listes pour stocker t et T à chaque jour
    t_list = []  # Liste pour stocker les temps t de chaque jour
    T_list = []  # Liste pour stocker les températures T de chaque jour
   
    # Simulation sur plusieurs jours consécutifs
    for jour in range(max_jours):
        
        # On résout l'EDO pour un jour
        Euler = calculTemperaturesEuler(tspan, T0, h, G)
        t = np.array(Euler[0])
        T = np.array(Euler[1])
        
        # Stocker t et T dans les listes
        t_list.append(t)
        T_list.append(T)
        
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
        
        
        # Les dernières valeurs de T deviennent les conditions initales pour la prochaine itération
        # Euler[1]= on accède à la deuxième liste d'Euler; 
        # Euler[1][:, -1]= dans la 2eme liste, on sélectionne tous les éléments de la dernière colonne'''
        T0 = T[:, -1]
        
        # Vérifier les conditions d'état stationnaire
        if jour >= 1:
            # t va de 0 à 24 mais possède n éléments 
            # -> On utilise len(t) en toute généralité
            diff_T = T_tot[0, -1] - T_tot[0, -len(t) - 1]
            
            # Condition de stationnarité
            if abs(diff_T) < 0.01 + 273.15 :
                print("État stationnaire atteint après ",jour + 1, "jours.")
                break
    return t_tot, T_tot, t_list, T_list

t_tot, T_tot, t_list, T_list = simulation_etat_stationnaire(tspan, T0, G, h, max_jours)
    
        
        
        
        
    
    
    
    
    








