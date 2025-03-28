import RechercheRacine as rr

def f(x):
    return x**3 - 2*x - 4



print(rr.bissection(f,-5,10,1e-6))
print(rr.secante(f,-5,10,1e-6))
