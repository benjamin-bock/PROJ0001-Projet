import numpy as np

def bissection(f,x0,x1,tol):
    f0 = f(x0)
    f1 = f(x1)
    i = 0
    x = 0

    if f0f1 > 0 : 
        print("Erreur, l'hypothèse n'est pas vérifiée, f(x0) et f(x1) ont le même signe")
        statut = 1
        return [0, statut]

    if f0f1 == 0 : 
        return [x0, 0] if f0 == 0 else [x1,0]
 
    while abs(x1-x0) > tol :
        x = (x0 + x1)/2
        fx = f(x)

        if fxf0 > 0:
                x0 = x
                f0 = fx
        else :
                x1 = x
        i += 1
        if i > 50:
            break
    if np.log2((abs(x1-x0))/2 tol) > i : 
        print("La fonction diverge")
        return [0, -1]

    return [x, 0]

###############################################################################################################################################################################

def secante(f,x0,x1,tol):
    
    statut = 0
    k = 0
    k_max = np.log2(np.abs(x1-x0)/(2*tol))
    fx0 = f(x0)
    fx1 = f(x1)
    
    if(np.abs(fx0-fx1)<=tol):
        statut = 1
        print("Erreur, les valeurs introduites partagent la même ordonnée.")
        return [1,statut]
    
    if(np.abs(fx0)<=tol):
        return [x0,statut]
    
    if(np.abs(fx1)<=tol):
        return [x1,statut]
    
    while (np.abs(fx1) > tol):
        x2 = x1 - fx1*(x1-x0)/(fx1-fx0)
        a = x1
        x1 = x2
        x0 = a
        fx0 = fx1
        fx1 = f(x1)
        
        k += 1 
        if(k >= k_max):
           statut = -1
           print("Elle ne converge pas vers une racine")
           return [-1,statut]
      
    return [x1,statut]





















