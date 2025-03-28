import numpy as np

def bissection(f,x0,x1,tol):

    fx0 = f(x0)
    fx1 = f(x1)
    k = 0
    k_max = 1000
    
    if(np.abs(fx0)<=tol): # si x0 est déja une racine
        statut = 0
        return [x0,statut]
    if(np.abs(fx1)<=tol): # si x1 est déja une racine
        statut = 0
        return [x1,statut]

    if(fx0*fx1<0): # => Deux valeurs de signe opposé => hyp. verifiée
        

        while (np.abs(x1-x0) > tol): #Tant que l'intervalle est + grand que tol
            x2 = (x0+x1)/2
            fx2 = f(x2)

            if (np.abs(fx2)<=tol):
                statut = 0
                print(k)
                return [x2,statut]

            if (fx2*fx0>0):
                x0 = x2
                fx0 = fx2

            else:
                x1 = x2
                fx1 = fx2
            k += 1

            if(k >= k_max):
                statut = -1
                print("Erreur, la bissection ne converge pas vers une racine.")
                print("Veuillez entrer des autres valeurs qui définissent un intervalle différent de celui des précédentes valeurs.")
                print("Ou il est possible que la fonction n'est pas continue dans cette intervalle.")
                return [1,statut]

        statut = 0
        print(k)
        return [x0,statut]

    else:
        statut = 1
        print("Erreur, la fonction ne change pas de signe dans cette intervalle-là.")
        print("Dans le cas où vous avez essayer plusieurs valeurs, il est possible que la fonction possède une racine multiple.")
        print(k)
        return [1,statut]
        
def secante(f,x0,x1,tol):

    statut = 0
    k_max = int(np.log2(np.abs(x1-x0)/(2*tol)))
    fx0 = f(x0)
    fx1 = f(x1)
    k = 0
    
    if(fx0*fx1>0):
        statut = 1
        print("Erreur, les valeurs introduites partagent le même signe.")
        return [1,statut]
    
    if(np.abs(fx0-fx1)<=tol):
        statut = 1
        print("Erreur, les valeurs introduites partagent la même ordonnée.")
        return [1,statut]

    if(np.abs(fx0)<=tol):
        return [x0,statut]

    if(np.abs(fx1)<=tol):
        return [x1,statut]

    for i in range(k_max):  # Maximum 50 itérations
        if abs(fx1 - fx0) < 1e-10:  # Éviter division par zéro
            break
            
        x2 = x1 - fx1 * (x1 - x0)/(fx1 - fx0)
        
        if abs(x2 - x1) < tol:  # Convergence atteinte
            return [x2,statut]
            
        x0, x1 = x1, x2
        fx0, fx1 = fx1, f(x2)
        
        k += 1
    else:
        # Si on sort de la boucle sans break, on utilise la bissection
        print("La méthode de la sécante n'a pas convergé.")
        print(k)
        statut = 1
        return [x1,statut]
    










