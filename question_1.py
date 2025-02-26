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


def bissection(f, x0, x1, tol):
   
    f_x0 = f(x0)
    f_x1 = f(x1)
    if abs(f_x0) < tol:
        return x0, 0  # a est proche d'une racine
    elif abs(f_x1) < tol:
        return x1, 0  # b est proche d'une racine
    elif f_x0 * f_x1 > 0:
        print('Selon le TVI, il n y a pas de racines entre ces 2 valeurs')
        return np.nan, 1
    else:
        d = abs(x1 - x0)
        iterations = 0  # Compte les itérations
        max_iterations = np.log2(np.abs((x1 - x0)) / (2 * tol)) # limite sinon boucles infinies

        while d > tol and iterations < max_iterations and f_x0 * f_x1 != 0:
            m = (x0 + x1) / 2
            f_m = f(m)
            if f_m == 0:
                return [m, 0]  # La racine a été trouvée
            elif f_x0 * f_m > 0:
                x0 = m
            else:
                x1 = m
            d = abs(x1 - x0)
            iterations += 1

        if iterations == max_iterations:
            return [m, 1]  # La méthode n'a pas convergé dans le nombre maximum d'itérations
        else:
            return [m, 0]  # La méthode a convergé dans la tolérance demandée
