import numpy as np

def secante(f, x0, x1, tol):
    def isreal(num):
        return isinstance(num, (int, float))

    #constantes
    statut = 0
    x = 0
    valeur_fx = f(x1)
    valeur_fy = f(x0)
    iter_count = 0
    iter_max = 30

    # verifier les bornes
    if not (isreal(x0) and isreal(x1)):
        x = 0
        statut = 1
        print('Les valeurs de la fonction ne sont pas réelles.')
        return x, statut

    if not (isreal(valeur_fx) and isreal(valeur_fy)):
        x = 0
        statut = 1
        print('Les valeurs de la fonction ne sont pas réelles.')
        return x, statut

    if abs(valeur_fy) <= tol:
        x = x0
        statut = 0
        return x, statut

    if abs(valeur_fx) <= tol:
        x = x1
        statut = 0
        return x, statut

    if valeur_fy == valeur_fx:
        x = 0
        statut = 1
        print('En prenant ces valeurs, la méthode de la sécante ne fonctionne pas.')
        return x, statut

    # Boucle principale - Méthode de la sécante
    while tol < abs(valeur_fx):
        try:
            z = x1 - (valeur_fx * (x1 - x0) / (valeur_fx - valeur_fy))
        except ZeroDivisionError:
            print('La division par zéro est survenue. Essayez de changer de bornes')
            x = 0
            statut = 1
            return x, statut

        x0 = x1
        x1 = z

        valeur_fy = valeur_fx
        valeur_fx = f(x1)

        iter_count += 1

        if iter_count > iter_max:
            x = 0
            statut = -1
            print('La fonction ne converge pas vers une racine.')
            return x, statut

    # Fin de la méthode
    x = x1

    return [x, statut]


 def bissection(f,x0,x1,tol):
    f0 = f(x0)
    f1 = f(x1)
    i = 0
    x = 0

    if f0*f1 > 0 : 
        print("Erreur, l'hypothèse n'est pas vérifiée, f(x0) et f(x1) ont le même signe")
        return [0, 1]   

    if f0*f1 == 0 : 
        return [x0, 0] if f0 == 0 else [x1,0]
 
    while abs(x1-x0) > tol :
        x = (x0 + x1)/2
        fx = f(x)

        if fx*f0 > 0:
                x0 = x
                f0 = fx
        else :          
                x1 = x
        i += 1
        if i > 50:
            break
    if np.log2((abs(x1-x0))/2 * tol) > i : 
        print("La fonction diverge")
        return [0, -1]
        
    return [x, 0]
