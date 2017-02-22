︠10ca3a23-1d2d-4344-90a3-5afb1655218d︠
import random
n=10
sl={}
for k in range(1,n+1):
    sl.update({k:[]})
names= set(sl.keys())
for name, choices in sl.items():
    left = set(names).difference([name]).difference(choices)
    if len(left)>0:
        left = list(left)
        random.shuffle(left)
        choices.extend(left)
## sl = slovar, ključi so številke od 1 do n, items so rangirani preostali člani

p.set_objective() ## Ne znava tvoriti objecitve-a (Morda bi lahko vseeno definirala ciljno funkcijo, npr. da želita minimizirati vsoto rangiranj izbranih sostanovalcev. Zanimivo bi bilo primerjati čas, porabljen za reševanje variante s ciljno funkcijo in brez, pa tudi, v kolikšnem deležu primerov se rešitvi ujemata (morda bi bilo smiselno poiskati še najslabšo dopustno rešitev).), oz ne veva, kako program deluje brez njega

for i in sl.keys():
    p.add_constraint(x[i,i]==0)

for i in sl.keys():
    for j in sl.keys():
        if i!=j:
            p.add_constraint(x[i,j] + sum(x[i,k] + sum(x[j,k]) for k in ??? <= 1) ## Ne veva kako omejiti k


p.solve()
︡dcc5545f-bac4-4a20-b598-97b4e65819d9︡{"stderr":"Error in lines 13-13\nTraceback (most recent call last):\n  File \"/projects/sage/sage-7.5/local/lib/python2.7/site-packages/smc_sagews/sage_server.py\", line 982, in execute\n    exec compile(block+'\\n', '', 'single') in namespace, locals\n  File \"\", line 1, in <module>\nNameError: name 'p' is not defined\n"}︡{"stderr":"*** WARNING: Code contains non-ascii characters ***\n"}︡{"done":true}︡









