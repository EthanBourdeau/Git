import time

def simul_tuple(nbr_iter=1000):
    t = tuple(range(1000))
    tps_exec = []
    for u in range(nbr_iter):
        for i in range(len(t)):
            t_i = time.time()
            recupe_val = t[i]
            t_f = time.time()
            tps_exec.append(float(t_f - t_i))
    return tps_exec

def calc_tps_exec(bdd_tps_exec):
    somme = 0
    for i in bdd_tps_exec:
        somme += i
    moy = somme / len(bdd_tps_exec)
    return moy

def simul_liste(nbr_iter=1000):
    t = list(range(1000))
    tps_exec = []
    for u in range(nbr_iter):
        for i in range(len(t)):
            t_i = time.time()
            recupe_val = t[i]
            t_f = time.time()
            tps_exec.append(float(t_f - t_i))
    return tps_exec

res_tuples = calc_tps_exec(simul_tuple())
print(res_tuples)

res_liste = calc_tps_exec(simul_liste())
print(res_liste)

if res_tuples < res_liste:
    print("Les tuples sont plus rapides")   
else:
    print("Les listes sont plus rapides")






