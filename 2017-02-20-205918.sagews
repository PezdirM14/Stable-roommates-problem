︠10ca3a23-1d2d-4344-90a3-5afb1655218dsr︠
import random
import time
p = MixedIntegerLinearProgram(maximization = False)
x = p.new_variable(binary = True)

start = time.time()
n=100
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

## Na koncu dobimo:
## sl = slovar, kljuci so stevilke od 1 do n, items so rangirani preostali clani

ranks = {i: {j: k for k, j in enumerate(l)} for i, l in sl.items()} ## Slovar, kjer za vsako osebo napise njegovo rangiranje ostalih oseb po vrsti

for i in names: ## Pogoj, ki pravi, da i-ta oseba ne more izbrati sama sebe
    p.add_constraint(x[i,i]==0)

for i in names: ## Simetricnost
    for j in names:
        p.add_constraint(x[i,j]==x[j,i])

for i in names: ## Vsaka oseba ima natanko enega sostanovalca
    p.add_constraint(sum(x[i,j] for j in names) == 1)

for i in names:
    for j in names:
        if i!=j:
            p.add_constraint(x[i,j] +
                 sum(x[i,k] for k in sl[i][ranks[i][j]+1:]) +
                 sum(x[j,k] for k in sl[j][ranks[j][i]+1:]) <= 1)

p.solve()
end = time.time()
elapsed = end - start
print(elapsed)
︡f255f2ad-fffe-4c35-b445-2ba61d57cda4︡










