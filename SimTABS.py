import numpy as np
from PerteEtGain import G
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp as ode45 # Defining the solver (ode45)
from scipy.interpolate import interp1d
from RechercheRacine import secante


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

C =          [ 0,    1,     2,      3,    4 ]
C =          [cc,   c1,    c2,    room,   w]'''  
C = np.array([50.0, 50.0, 10.0,  12.0  , 30.0])
C = C*1000.00 # kJ/m²K -> J/m²K
''' 
R =         [  0,    1    , 2,      3,     4,    5]
R =         [cc-c1,  x,   c2-cc,   r-s,  s-c2,   w]'''
R = np.array([0.05, 0.025 , 0.02  , 0.1, 0.183, 0.15]) 

nom_T = ["la pièce, T_room", "l'eau dans les tubes, T_t", "la partie centrale du béton, T_cc", "la partie supérieure du béton, T_c1", "la partie inférieure du béton, T_c2",] 

# Question 3.1 ##############################################################################################################

def odefunction(t, T):
    
    # Convertir T en float64 pour éviter les problèmes de type
    T = T.astype(np.float64)
    
    '''T = [  0,  1 , 2,  3,  4, 5]'''
    '''T = [room, t, cc, c1, c2, w]'''
    # Celsius -> Kelvin
    T += 273.15 
    
    '''Valeur de T_w'''
    if t <= 4 :
        T_w = 18.0 + 273.15
    else :
        T_w = 0.0
        
    # On place T_W en T[5]
    T = np.concatenate((T, np.array([T_w],dtype=np.float64)), axis=None)
    
    # Résolution du système ED
    dT = np.zeros(5, dtype=np.float64)
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
    dT *= 3600.0
    
    return dT

# Question 3.2 #########################################################################################################

# Définition de la fonction
def calculTemperaturesEuler(tspan, T0, h):
    t = np.linspace(tspan[0], tspan[-1], int((tspan[-1]-tspan[0])/h +1))
    T = np.zeros((5, len(t)), dtype=np.float64)  # Correction ici
    T[:, 0] = T0
    
    for i in range(1, len(t)):
        dT = odefunction(t[i-1], T[:, i-1])  # Utilisation correcte des indices
        T[:, i] = T[:, i-1] + h * dT  # Utilisation correcte des indices
    
    return [t, T]
 
# Résolution numérique

# Données   
T0 = np.array([15.0, 15.0, 15.0, 15.0, 15.0]) #T0 en °C
h = 0.01
t0 = 0.0
tf = 24.0
tspan = [t0, tf]

Euler = calculTemperaturesEuler(tspan, T0, h)

plt.figure(figsize=(10, 6))
for k in range(len(T0)):
    plt.plot(Euler[0], Euler[1][k, :], 'o-', markersize=5, label="Euler") # Tracer Euler
plt.xlabel("Temps (h)", fontsize=13)
plt.ylabel("Température finale de la pièce (°C)", fontsize=13)
plt.title("Comparaison des résultats entre Euler et Runge-Kutta 45", fontsize=13)


# Question 3.3 ##########################################################################################################

# Définition de la fonction
def calculTemperaturesIVP(tspan, T0, rtol):
    
    
    solution = ode45(lambda t, T: odefunction(t, T), tspan, T0, method='RK45', rtol=rtol)
    return [solution.t, solution.y]

# Résolution numérique
tspan = [t0, tf]
rtol = 1e-15
IVP = calculTemperaturesIVP(tspan, T0, rtol)

for k in range(len(T0)):
    plt.plot(IVP[0], IVP[1][k, :], 'o-', markersize=5, label="RK45")
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(80/plt.gcf().dpi, 70/plt.gcf().dpi))
plt.show()
    
# Question 3.4 #############################################################################################################

def comparaisonEulerIVP(t_ref, T_ref, h_test) :
    
    # Stocker les erreurs pour chaque h
    errors = []
    
    for h in h_test:
        # Résolution avec Euler
        t_euler, T_euler = calculTemperaturesEuler(tspan, T0, h)
        
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
    plt.xlabel("Pas de temps h (heures)", fontsize=13)
    plt.ylabel("Erreur absolue moyenne (°C)", fontsize=13)
    plt.title("Détermination du pas de temps h optimal dans la méthode d'Euler", fontsize=13)
    plt.legend(fontsize=13)
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
t_ref, T_ref = calculTemperaturesIVP(tspan, T0, rtol)

# Valeurs candidates de h

h_test = [0.05, 0.01, 0.005, 0.001, 0.0005]

comparaisonEulerIVP(t_ref, T_ref, h_test)

# Question 3.5 #############################################################################################

# Initialisation des constantes
max_jours = 100
jour = 0
h = 0.01

def simulation_etat_stationnaire(tspan, T0, h, max_jours) :
    

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
        Euler = calculTemperaturesEuler(tspan, T0, h)
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
                print("\nQuestion 3.5\nÉtat stationnaire atteint après",jour + 1,"jours.\n")
                break
        
        # Mettre à jour la température de référence pour le prochain jour
        T_room_jour_prec = T_room_jour
            
    return t_f, T_f, jour+1

t_f, T_f, jour = simulation_etat_stationnaire(tspan, T0, h, max_jours)
    
        
# Visualisation
t_f = np.array(t_f)/(tf-t0)
T_f = np.array(T_f)
plt.figure(figsize=(10, 6))
plt.xticks(np.linspace(t_f[0], t_f[-1], 10))  # Divise la grille en 8 parts verticales égales

plt.plot(t_f, T_f[:, 0], 'o-', markersize=5, label="T_room") # Tracer 
plt.plot(t_f, T_f[:, 4], 'o-', markersize=5, label="T_c2") # Tracer T_c2
plt.xlabel("Temps (jours)", fontsize=13)
plt.ylabel("Température finale de la pièce (°C)", fontsize=13)
plt.title("Convergence vers l'état stationnaire", fontsize=13)
plt.grid(True)
plt.legend(fontsize=13)
plt.show()
    
# Question 3.6 #########################################################################################################

# Stocke les variables
t_f1 = t_f
T_f1 = T_f 

'''Comparons les 3 scénarios'''

for j in range(len(T0)): #On affiche chaque T[:]
    
    # Scénario 1 (voir question 5) ##############################################
    plt.figure(figsize=(8, 6))
    plt.rc('xtick', labelsize=18)  # Taille police graduations x
    plt.rc('ytick', labelsize=18)  # Taille police graduations y
    plt.xticks(np.linspace(t_f1[0], t_f1[-1], 10))  # Divise la grille en 8 parts verticales égales
    plt.plot(t_f1, T_f1[:, j], 'o-', markersize=7, label="Scénario 1")
    plt.xlabel("Temps (jours)",fontsize=18)
    plt.ylabel(f"Température finale de \n {nom_T[j]} (°C)\n",fontsize=18)
    plt.grid(True)
    plt.title(f"Évolution de la température \n de {nom_T[j]},\n en fonction des différents scénarios", fontsize=18)
    
    # Scnéario 2 ##############################################################
    
    def scenario2(tspan, T0, h, jour) :
        
        def odefunction2(t, T):
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
        
        def calculTemperaturesEuler2(tspan, T0, h):
            
            # Initialisation
            
            t = np.arange(tspan[0], tspan[-1] + h, h)
            n = len(t)
            T = np.zeros((5, n))
            T[:, 0] = T0
            
            # Méthode d'Euler
            for i in range(n-1):
                dT = odefunction2(t[i], T[:, i])
                T[:, i+1] = T[: , i] + h * dT
            
            return [t, T]
        
        def simulation_scenario2(tspan, T0, h, jour) :
            
            # Listes pour stocker t et T à chaque jour
            t_f = []  # Liste pour stocker les temps t de chaque jour
            T_f = []  # Liste pour stocker les températures T de chaque jour
            
            # Conditions initiales
            t_f.append(tspan[0])
            T_f.append(T0)
            
            # Simulation sur plusieurs jours consécutifs
            for day in range(jour):
                
                # On résout l'EDO pour un jour
                Euler = calculTemperaturesEuler2(tspan, T0, h)
                t = np.array(Euler[0]) # Temps
                T = np.array(Euler[1]) # Température
                
                # Stocker t et T dans les listes
                t_f.append(t[-1] + day * 24) # On stocke tf à chaque fin de journée
                T_f.append(T[:, -1])         # On stocke T à chaque fin de journée
                  
                #Les dernières valeurs de T deviennent les conditions initales pour la prochaine itération
                T0 = T[:, -1]
                    
            return t_f, T_f
    
        t_f, T_f = simulation_scenario2(tspan, T0, h, jour)
    
        return t_f, T_f
    
    # Simulation
    t_f, T_f = scenario2(tspan, T0, h, jour)
    
    # Représenation graphique
    t_f2 = np.array(t_f)/(tf-t0)
    T_f2 = np.array(T_f)
    plt.plot(t_f2, T_f2[:, j], 'o-',  markersize=5, label="Scénario 2")
    
    
    # Scnéario 3 ################################################################
    
    def scenario3(tspan, T0, h, jour) :
        
        def odefunction3(t, T):
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
        
        def calculTemperaturesEuler3(tspan, T0, h):
            
            # Initialisation
            
            t = np.arange(tspan[0], tspan[-1] + h, h)
            n = len(t)
            T = np.zeros((5, n))
            T[:, 0] = T0
            
            # Méthode d'Euler
            for i in range(n-1):
                dT = odefunction3(t[i], T[:, i])
                T[:, i+1] = T[: , i] + h * dT
            
            return [t, T]
        
        def simulation_scenario3(tspan, T0, h, jour) :
            
            # Listes pour stocker t et T à chaque jour
            t_f = []  # Liste pour stocker les temps t de chaque jour
            T_f = []  # Liste pour stocker les températures T de chaque jour
            
            # Conditions initiales
            t_f.append(tspan[0])
            T_f.append(T0)
            
            # Simulation sur plusieurs jours consécutifs
            for day in range(jour):
                
                # On résout l'EDO pour un jour
                Euler = calculTemperaturesEuler3(tspan, T0, h)
                t = np.array(Euler[0]) # Temps
                T = np.array(Euler[1]) # Température
                
                # Stocker t et T dans les listes
                t_f.append(t[-1] + day * 24) # On stocke tf à chaque fin de journée
                T_f.append(T[:, -1])         # On stocke T à chaque fin de journée
                  
                #Les dernières valeurs de T deviennent les conditions initales pour la prochaine itération
                T0 = T[:, -1]
                    
            return t_f, T_f
    
        t_f, T_f = simulation_scenario3(tspan, T0, h, jour)
    
        return t_f, T_f
    
    # Simulation
    t_f, T_f = scenario3(tspan, T0, h, jour)
    
    # Représenation graphique
    t_f3 = np.array(t_f)/(tf-t0)
    T_f3 = np.array(T_f)
    plt.plot(t_f3, T_f3[:, j], 'o-',  markersize=5, label="Scénario 3")
    
    # On affiche les graphes
    plt.legend(loc='upper left', bbox_to_anchor=(90/plt.gcf().dpi, 130/plt.gcf().dpi), fontsize=16)
    plt.show()


##################################################################################################################   
# QUESTION 4 ##############################################################################################################
##################################################################################################################

# QUESTION 4.1 ##############################################################################################################

def scenario4(tspan, T0, h, delta_t) :
        
        
        def odefunction4(t, T):
            '''T = [  0,  1 , 2,  3,  4, 5]'''
            '''T = [room, t, cc, c1, c2, w]'''
            # Celsius -> Kelvin
            T = T + 273.15 
            
            '''Valeur de T_w'''
            if t <= 4 :
                T_w = 18 + 273.15
            elif 4 < t <= 4 + delta_t :
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
        
        # Méthode d'Euler
        def calculTemperaturesEuler4(tspan, T0, h):
            
            # Initialisation
            
            t = np.arange(tspan[0], tspan[-1] + h, h)
            n = len(t)
            T = np.zeros((5, n))
            T[:, 0] = T0
            
            # Méthode d'Euler
            for i in range(n-1):
                dT = odefunction4(t[i], T[:, i])
                T[:, i+1] = T[: , i] + h * dT
            
            return [t, T]
        

        def simulation_scenario4(tspan, T0, h) :
                        
            # On résout l'EDO pour un jour
            Euler = calculTemperaturesEuler4(tspan, T0, h)
            t_4 = np.array(Euler[0]) # Temps
            T_4 = np.array(Euler[1]) # Température
                    
            return t_4, T_4
    
        t_4, T_4 = simulation_scenario4(tspan, T0, h)
    
        return t_4, T_4

def findTmax(tspan, T0, h, delta_t) :
    
    t_4, T_4 = scenario4(tspan, T0, h, delta_t)
    
    T_confort = (T_4[0, :] + T_4[4, :])/2  # Moyenne entre T_room (indice 0) et T_c2 (indice 4)
    T_max = np.max(T_confort)
    t_max = np.argmax(T_confort)
    return T_max , t_max , T_confort , t_4, T_4

# Simulation
delta_t = 1
T_max, t_max, T_confort, t_4, T_4 = findTmax(tspan, T0, h, delta_t)

# Représentation graphique
t_4 = np.array(t_4)
T_confort = np.array(T_confort)
t_max_plot = (np.float64(t_max))/100

plt.figure(figsize=(10, 6))
plt.xticks(np.linspace(t_4[0], t_4[-1], 9))  # Divise la grille en 8 parts verticales égales
plt.plot(t_4, T_confort, 'o-', markersize=3, label="Température de confort")
plt.plot(t_max_plot, T_max,'ro', markersize=8)
plt.axhline(y=T_max, color='r', linestyle='--', label=f"T_max = {T_max:.2f}°C")
plt.xlabel("Temps (heures)", fontsize=13)
plt.ylabel("Température de confort (°C)", fontsize=13)
plt.title(f"Évolution de la température de confort pour ∆t = {delta_t}", fontsize=13)
plt.grid(True)
plt.legend(fontsize=13)
plt.show()


# QUESTION 4.2 ##############################################################################################################

def f(delta_t):
    """
    Fonction dont on cherche la racine : f(delta_t) = T_max(delta_t) - T_max_d
    """
    if delta_t < 0:  # Protection contre les valeurs négatives
        return float('inf')
    T_max, _, _, _, _ = findTmax(tspan, T0, h, delta_t)
    return T_max - T_max_d

# Test de la fonction
T_max_d = 24.0  # Température maximale souhaitée

# Points initiaux pour la méthode de la sécante
delta_t_min = 0.1  # Premier point initial
delta_t_max = 8.0  # Deuxième point initial
tol = 1e-2  # Tolérance moins stricte

resultat_sec = secante(f, delta_t_min, delta_t_max, tol)

delta_t_optimal = resultat_sec[0]


print(f"Question 4.2\nPour atteindre une température maximale de {T_max_d}°C, il faut un ∆t de {delta_t_optimal:.2f} heures \n")

# Vérification du résultat
T_max_final, t_max, T_confort, t_4, T_4 = findTmax(tspan, T0, h, delta_t_optimal)
print(f"Température maximale atteinte : {T_max_final:.2f}°C \n")

# Représentation graphique avec le delta_t optimal
t_4 = np.array(t_4)
T_confort = np.array(T_confort)
t_max_plot = (np.float64(t_max))/100

plt.figure(figsize=(12, 6))
plt.xticks(np.linspace(t_4[0], t_4[-1], 9))  # Divise la grille en 8 parts verticales égales
plt.plot(t_4, T_confort, 'o-', markersize=3, label="Température de confort")
plt.plot(t_max_plot, T_max_final, 'ro', markersize=8, label="T_max atteint")
plt.axhline(y=T_max_d, color='g', linestyle='--', label=f"T_max désirée = {T_max_d}°C")
plt.axhline(y=T_max_final, color='r', linestyle='--', label=f"T_max atteinte = {T_max_final:.2f}°C")
plt.xlabel("Temps (heures)", fontsize=13)
plt.ylabel("Température de confort (°C)", fontsize=13)
plt.title(f"Évolution de la température de confort pour ∆t optimal = {delta_t_optimal:.2f} heures", fontsize=13)
plt.grid(True)
plt.legend(fontsize=13)
plt.show()   

# QUESTION 4.3 ##############################################################################################################
# Simulation avec le delta_t optimal pour obtenir toutes les températures

def simulation_complete(tspan, T0, h, delta_t, nb_jours):
    """
    Simule le système sur plusieurs jours en gardant toutes les données temporelles
    """
    # Initialisation des tableaux pour stocker toutes les données
    t_tot = np.array([])
    T_tot = np.zeros((5, 0))
    
    # Simulation jour par jour
    for jour in range(nb_jours):
        # Simulation d'une journée
        t_jour, T_jour = scenario4(tspan, T0, h, delta_t)
        
        # Ajout du décalage temporel pour ce jour
        t_jour = t_jour + jour * 24
        
        # Concaténation avec les résultats précédents
        t_tot = np.concatenate((t_tot, t_jour))
        T_tot = np.concatenate((T_tot, T_jour), axis=1)
        
        # Mise à jour des conditions initiales pour le jour suivant
        T0 = T_jour[:, -1]
    
    return t_tot, T_tot

def simulation_etat_stationnaire4(tspan, T0, h, delta_t, max_jours):
    """
    Simule le système jusqu'à l'état stationnaire avec un delta_t constant
    """
    
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
        # On résout l'EDO pour un jour avec le même delta_t
        t_4, T_4 = scenario4(tspan, T0, h, delta_t)
        
        # Stocker t et T dans les listes
        t_f.append(t_4[-1] + jour * (tspan[-1]-tspan[0]))
        T_f.append(T_4[:, -1])
        
        # Mettre à jour T_room_jour_actuel
        T_room_jour = T_4[0, -1]
        
        # Vérifier les conditions d'état stationnaire
        if jour >= 1:
            diff_T = abs(T_room_jour - T_room_jour_prec)
            if diff_T < 0.01:
                print(f"État stationnaire atteint après {jour + 1} jours.\n")
                break
        
        # Mettre à jour pour le prochain jour
        T0 = T_4[:, -1]
        T_room_jour_prec = T_room_jour
            
    return t_f, T_f, jour+1

def f_stationnaire(delta_t):
    """
    Fonction dont on cherche la racine : f(delta_t) = max(T_confort) - T_max_d 
    Vérifie que la température de confort ne dépasse jamais T_max_d à tout instant
    """
    if delta_t < 0:  # Protection contre les valeurs négatives
        return float('inf')
        
    # Simulation sur plusieurs jours jusqu'à l'état stationnaire
    nb_jours = 5  # On simule sur 5 jours pour atteindre l'état stationnaire
    t_complet, T_complet = simulation_complete(tspan, T0, h, delta_t, nb_jours)
    
    # Calcul de la température de confort pour tous les points
    T_confort = (T_complet[0, :] + T_complet[4, :])/2
    
    # On regarde le dernier jour (état stationnaire)
    debut_dernier_jour = (nb_jours - 1) * 24
    indices_dernier_jour = t_complet >= debut_dernier_jour
    T_confort_dernier = T_confort[indices_dernier_jour]
    
    # On vérifie le maximum sur toute la journée
    T_max = np.max(T_confort_dernier)
    
    return T_max - T_max_d

# Test de la fonction pour T_max_d = 24°C
T_max_d = 24.0  # Température maximale à ne jamais dépasser
max_jours = 100

# Points initiaux pour la méthode de la sécante
delta_t_min = 0.1  # Premier point initial
delta_t_max = 8.0  # Deuxième point initial
tol = 1e-2  # Tolérance


# Utilisation de la méthode de la sécante
resultat_sec = secante(f_stationnaire, delta_t_min, delta_t_max, tol)
delta_t_optimal = resultat_sec[0]

print(f"Question 4.3\nPour atteindre une température maximale de {T_max_d}°C à l'état stationnaire: ∆t optimal = {delta_t_optimal:.2f} heures \n")

# Vérification du résultat avec le delta_t optimal trouvé
t_stat, T_stat, jour_stat = simulation_etat_stationnaire4(tspan, T0, h, delta_t_optimal, max_jours)
T_stat = np.array(T_stat)
T_confort_final = (T_stat[-1, 0] + T_stat[-1, 4])/2
print(f"Température maximale atteinte à l'état stationnaire : {T_confort_final:.2f}°C\n")

# Représentation graphique
t_stat = np.array(t_stat)/(tf-t0)  # Conversion en jours
T_stat = np.array(T_stat)

# Calcul de la température de confort pour tous les points
T_confort = (T_stat[:, 0] + T_stat[:, 4])/2

plt.figure(figsize=(12, 6))
plt.plot(t_stat, T_confort, 'b-', label='Température de confort')
plt.axhline(y=T_max_d, color='g', linestyle='--', label=f'T_max désirée = {T_max_d}°C')
plt.axhline(y=T_confort[-1], color='r', linestyle='--', label=f'T_max atteinte = {T_confort[-1]:.2f}°C')
plt.xlabel("Temps (jours)", fontsize=13)
plt.ylabel("Température de confort (°C)", fontsize=13)
plt.title(f"Évolution de la température de confort à l'état stationnaire (∆t = {delta_t_optimal:.2f}h)", fontsize=13)
plt.grid(True)
plt.legend(fontsize=13)
plt.show()



# Simulation sur plusieurs jours
nb_jours = jour_stat  # On simule sur 5 jours pour voir la stabilisation
t_complet, T_complet = simulation_complete(tspan, T0, h, delta_t_optimal, nb_jours)

# Calcul de la température de confort pour tous les points
T_confort = (T_complet[0, :] + T_complet[4, :])/2

# Vérification de la norme EN (19.5°C - 24°C entre 8h et 19h)
# On ne regarde que le dernier jour
debut_dernier_jour = (nb_jours - 1) * 24
indices_dernier_jour = t_complet >= debut_dernier_jour

t_dernier = t_complet[indices_dernier_jour] - debut_dernier_jour
T_confort_dernier = T_confort[indices_dernier_jour]

# Période 8h-19h du dernier jour
masque_periode = (t_dernier >= 8) & (t_dernier <= 19)
T_confort_periode = T_confort_dernier[masque_periode]
t_periode = t_dernier[masque_periode]

# Vérification des limites
conforme = np.all((T_confort_periode >= 19.5) & (T_confort_periode <= 24))
T_min_periode = np.min(T_confort_periode)
T_max_periode = np.max(T_confort_periode)

print("Vérification de la norme EN15251 (période 8h-19h du dernier jour):")
print(f"Température minimale: {T_min_periode:.2f}°C")
print(f"Température maximale: {T_max_periode:.2f}°C")
print(f"La norme EN15251 est {'respectée' if conforme else 'non respectée'}.\n")

# Graphique de l'évolution complète
plt.figure(figsize=(12, 6))
plt.plot(t_complet/24, T_confort, 'b-', label='Température de confort')
plt.axhline(y=24, color='r', linestyle='--', label='Limite supérieure (24°C)')
plt.axhline(y=19.5, color='g', linestyle='--', label='Limite inférieure (19.5°C)')
plt.xlabel("Temps (jours)", fontsize=13)
plt.ylabel("Température de confort (°C)", fontsize=13)
plt.title(f"Évolution de la température de confort sur {nb_jours} jours (∆t = {delta_t_optimal:.2f}h)", fontsize=13)
plt.grid(True)
plt.legend(fontsize=13)
plt.show()

# Graphique détaillé du dernier jour
plt.figure(figsize=(12, 6))
plt.plot(t_dernier, T_confort_dernier, 'b-', label='Température de confort')
plt.xticks(np.linspace(t_4[0], t_4[-1], 9))  # Divise la grille en 8 parts verticales égales
plt.axhline(y=24, color='r', linestyle='--', label='Limite supérieure (24°C)')
plt.axhline(y=19.5, color='g', linestyle='--', label='Limite inférieure (19.5°C)')
plt.axvline(x=8, color='gray', linestyle=':', label='Période 8h-19h')
plt.axvline(x=19, color='gray', linestyle=':')
plt.xlabel("Heure de la journée", fontsize=13)
plt.ylabel("Température de confort (°C)", fontsize=13)
plt.title("Température de confort - Dernier jour", fontsize=13)
plt.grid(True)
plt.legend(loc='lower right', fontsize=13)
plt.show()


