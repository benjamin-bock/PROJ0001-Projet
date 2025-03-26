import numpy as np
import matplotlib.pyplot as plt
import SimTABS as tabs

# QUESTION 1 ################################################################################################################

T0 = np.array([15.0, 15.0, 15.0, 15.0, 15.0]) #T0 en °C


def scenario2(tspan, T0, h, jour) :
        
        def odefunction2(t, T):
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
    plt.plot(t_f2, T_f2[:, j], 'o-',  markersize=5, label="Scénario 2"