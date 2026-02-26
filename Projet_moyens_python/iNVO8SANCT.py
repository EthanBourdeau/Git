import random

def simul_invoq(nbr_inv):
    t = 0
    for u in range (nbr_inv):
        nbr = random.random()
   
        if 0 < nbr <= 0.49:
            t += 5
        if 0.49< nbr <= 0.77:
            t += 2
        if 0.77< nbr <= 0.87:
            t += 10
        if 0.87< nbr <= 0.884:
            t += 25
        if 0.884< nbr <= 0.889:
            t += 50
        if 0.889< nbr <= 0.891:
            t += 100
    return t

def calc (gen, it):
    tot_gen = 0

    for i in range (gen):
        tot_un = simul_invoq(it) 

        if tot_un >= 40:
            tot_gen+= 1
    return tot_gen / gen * 100
        
    
print(calc(10000, 14))