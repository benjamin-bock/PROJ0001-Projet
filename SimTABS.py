import numpy as np
import scipy as sp
import PerteEtGain as pg
from scipy.integrate import solve_ivp as ode45 # Defining the solver (ode45)


'''Encodage des constantes

C =          [ 0,  1,  2,  3,    4 ]
C =          [cc, c1, c2, room,  w]'''  
C = np.array([50, 50, 10,  12  , 30])
C = C*1000 # kJ/m²K -> J/m²K
''' 
R =         [  0,    1    , 2,      3,     4,    5]
R =         [cc-c1,  x,   c2-cc,   r-s,  s-c2,   w]'''
R = np.array([0.05, 0.025 , 0.02  , 0.1, 0.183, 0.15])

# Question 1

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

# Question 2

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
    
    return t, T
 
# Résolution numérique

# Données   
T0 = np.array([15, 15, 15, 15, 15])
heure, flux_chaleur = pg.PerteEtGain()
t, G = pg.interpG(heure, flux_chaleur)
h = 0.01

Euler = calculTemperaturesEuler(t, T0, h, G)

# Question 3

def calculTemperaturesIVP(t, T0, rtol):
    
    tspan = [t[0], t[-1]]
    solution = ode45(odefunction(tspan, T0, G), t, T0, method='RK45', rtol=rtol)
    return solution.t, solution.y

IVP = calculTemperaturesIVP(t, T0, 1e-10)
    


























