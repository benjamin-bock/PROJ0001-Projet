import constante.py as cst

# Fonction pour le bilan énergétique de la partie centrale du béton
def dTcc_dt(T_cc, T_c1, T_t, T_c2):
    return (-1 / cst.R_cc_c1 * (T_cc - T_c1) - 1 / cst.R_x * (T_cc - T_t) + 1 / cst.R_c2_cc * (T_c2 - T_cc)) / cst.C_cc

# Fonction pour le bilan énergétique de la partie supérieure du béton
def dTc1_dt(T_c1, T_cc):
    return (-1 / cst.R_cc_c1 * (T_c1 - T_cc)) / cst.C_c1

# Fonction pour le bilan énergétique de la partie inférieure du béton
def dTc2_dt(T_c2, T_cc, T_room):
    return (-1 / cst.R_c2_cc * (T_c2 - T_cc) + 1 / (cst.R_r_s + cst.R_s_c2) * (T_room - T_c2)) / cst.C_c2

# Fonction pour le bilan énergétique de la pièce régulée
def dTroom_dt(T_room, T_c2, G_t):
    return (-1 / (cst.R_r_s + cst.R_s_c2) * (T_room - T_c2) + G_t) / cst.C_room

# Fonction pour le bilan énergétique des tubes
def dTt_dt(T_t, T_cc, T_w):
    return (-1 / cst.R_x * (T_t - T_cc) - 1 / cst.R_w * (T_t - T_w)) / cst.C_w
