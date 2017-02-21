import time
import csv
import random


# branje_preferenc(dat):
# Funkcija, ki prebere preference posameznikov, zapisane v csv datoteki.
# Prva številka v posamezni vrstici ponazarja posameznika, ostale pa njegove preference od najbolj zaželjene,
# do najmanj zaželjene osebe.
    
def branje_preferenc(dat):   
    prefs = {} # Slovar, kamor bomo shranili preference.
    with open(dat, "r") as fin:
        for line in fin:
            line = line.split(",") # Ker so podatki v csv datoteki ločeni z vejico, razdelimo vsako vrstico glede na ",".
            line=[s.strip() for s in line] # Odstranimo bele znake(prazen znak).
            prefs[line[0]] = line[1:] # Preference prvega v vrstici, so vse osebe od vključno druge osebe v vrstici.
    return prefs



# zapolni(prefs):
# Funkcija naključno zapolni preference, ki jih dobi iz slovarja prefs, prejšnje funkcije branje_preferenc(dat).
# To je še posebej uporabno za naključno generiranje večjih vzorcev ljudi, da nam ni potrebno ročno vpisovati njihovih preferenc.
# To funkcijo sva uporabila tudi zaradi tega, ker pri analizi algoritma točno določene preference niso pomembne, potrebujemo samo veliko podatkov.

def zapolni(prefs): #Če katera izmed oseb ni rangirala vseh ostalih ljudi, to naredimo po naključnem vrstnem redu
    names= set(prefs.keys()) # Množica oseb, ki iščejo sostanovalca. 
    for name, choices in prefs.items():
        left = set(names).difference([name]).difference(choices) # Za vsako osebo pogledamo, koga od ostalih oseb ni rangirala in jih shranimo v množico left.

        if len(left)>0: 
            left = list(left) # Iz množice naredimo seznam, zaradi lepših pythonskih operacij.
            random.shuffle(left) 
            choices.extend(left) # Dopolnimo preference.

# zavrni(prefs, ranks, holds):
# Ta funkcija naredi redukcijo naših preferenc. Argumenti, ki jih sprejme so:
# prefs= slovar preferenc iz funkcije branje_preferenc(dat),
# ranks= slovar, ki za vsako osebo pove kako rangira ostale osebe, podrobneje opisan v funkciji stableroomate.
# holds= kdo drži koga v vsakem koraku prve faze, podrobneje opisano v funkciji faza1. 

            
def zavrni(prefs, ranks, holds):

    for y in holds:

        i = 0
        x = holds[y] # oseba x 'drži' povabilo od osebe y.
        
        while i < len(prefs[y]):
            yi = prefs[y][i] # Oseba, iz preferenc osebe y, seveda začnemo z najvišjo, torej prvo(i=0).

            if yi == x: # Če se zgodi da je yi kar x, potem vse slabše izbire izbrišemo iz preferenc y.
                prefs[y] = prefs[y][:i+1]

            if ranks[yi][holds[yi]] < ranks[yi][y]: # Nižje kot je, bolje je. yi zavrne osebo y, če je y rangirana višje od 
                prefs[y].pop(i)                     # osebe, ki jo trenutno drži.
                continue
            i += 1

# zig_zag:
# Naredi naslednji korak naše metode, po temu ko redukcija po prvi fazi že narjena. Naredi zig-zag redukcijo po pravilu:
# začnemo s poljubno osebo, ki ima več kot eno osebo v njihovem reduciranem seznamu preferenc, naj bo to oseba $p_i$.
# Potem je oseba $q_i$ druga preferenca $p_i$ in $p_{i+1}$ zadnja preferenca $q_i$.
# To rekurzivno zaporedje ponavljamo dokler se nek $p_i$ ne ponovi. Ko se to zgodi lahko iz seznamov preferenc izbrišemo osebe $p_{i+1}$ in $q_i$

def zig_zag(prefs, ranks, holds):

    p = []
    q = []

    # Najprej najdemo osebo, ki ima več kot eno preferenco še. 
    for x in sorted(prefs):
        if len(prefs[x]) > 1:
            cur = x # Določimo trenutno osebo.
            break
    else:
        return None


    while cur not in p:
        # q_i = Druga oseba v seznamu preferenc p_i
        q.append( prefs[cur][1] )

        # p_{i+1}= zadnja oseba v seznamu preferenc q_i
        p.append(cur)
        cur = prefs[q[-1]][-1]

    a = p[p.index(cur):] # reduciran seznam po zig-zag redukciji.
    b = [prefs[n][0] for n in a]

    return a

# faza1(prefs,ranks) opravi prvo fazo našega algoritma. Sprejme seznam preferenc posameznikov ter
# ranks, ki za vsako osebo povejo kako je rangirala ostale. Trenutna preferenca curpref je na začetku None.


def faza1(prefs, ranks, curpref=None):

    # Slovar, ki nam pove od koga oseba drži snubitev. Na začetku so vse snubitve None, kar potem spreminjamo.
    holds = dict( (name,None) for name in prefs.keys() )

    if curpref is None:
        curpref = dict( (name, 0) for name in prefs.keys() ) # Slovar, z osebami. Na začetku
                                                             # damo ničle zato, ker vedno najprej zasnubijo prvo osebo
                                                             # s svojega seznama preferenc.
    people = list(prefs.keys()) # Seznam vseh oseb.
    random.shuffle(people)

    ze_zasnubili = set() # Ljudi, ki smo jih že zasnubili.
   


    for person in people:
        poser = person # Najdemo osebo, ki snubi.

        while (1):
            
            while curpref[poser] < len(prefs[poser]):
                nchoice = prefs[poser][curpref[poser]] # Oseba, katero naš poser snubi
                curpref[poser] += 1 # Povečamo za eno.

                # person poser is holding
                cchoice = holds[nchoice] # Oseba, katere snubitev naš poser trenutno drži.
                
                if cchoice is None or \
                        ranks[nchoice][poser] < ranks[nchoice][cchoice]: # Če je nižje rangirana je boljše zato prekinemo zanko.
                    break
                elif curpref[poser]==len(prefs[poser]): # Preverimo, če so koga vsi zavrnili. Če se to zgodi, ne obstaja stabilno prirejanje.
                    return(None)
            
            holds[nchoice] = poser # Oseba, katero je naš poser zasnubil sprejme snubitev od poserja.

            if nchoice not in ze_zasnubili: # V primeru, če je še ni zasnubil prekinemo zanko.
                
                assert cchoice is None
                break

            
            poser = cchoice # Nastavimo novo osebo, ki snubi.
            if curpref[poser]==len(prefs[poser]): # Ta pogoj je nujen, saj se v primeru, ko neka oseba x sprejme snubitev osebe y
                return(None)                      # ki ima x zadnjega v seznamu, a ga kasneje zavrne. Pogoj za notranjo zanko while več
                                                  # ne velja, ampak preostanek zanke while pa se ne spremeni. S tem pogojem odpravimo ta problem.


        ze_zasnubili.add(nchoice) # Dodamo v množico.

    return holds # Vrnemo kdo drži čigavo snubitev po prvi fazi.

# Funkcija stableroomate je glavna funkcija našega algoritma, saj vključuje vse zgoraj naštete funkcije. Njen argument je preprosta csv datoteka, v kateri
# so določene preference posameznikov, ki so ločene z vejicami, poleg tega pa prva številka ali niz v vsaki vrstici predstavlja osebo in ne preference. 

def stableroomate(dat):
    
    # Preberemo vse preference iz naše datoteke dat.
    prefs = branje_preferenc(dat)

    # Dopolnemo preference posameznikov,
    # v primeru da je katera izmed oseb navedla premalo preferenc(lahko tudi nobene).
    # To naredimo naključno.
    zapolni(prefs)

    # Za vsako ime generiramo slovar, ki nam za vsakega posameznika pokaže kako rangira posamezne osebe, to predstavimo s številko.
    ranks = dict( (idx, dict(zip(val,range(len(val)) )))
                 for idx,val in prefs.items() )

    # Naredimo prvo fazo in dobimo kdo koga snubi in kdo drži snubitev od koga.
    holds = faza1(prefs, ranks)

    if holds==None: # Preveriti moramo, če se kdaj zgodi, da funkcija, ki izvede prvo fazo vrne None. V tem primeru  stabilno prirejanje ne obstaja.
        print("no solution exists")
        return    
    
    zavrni(prefs, ranks, holds) # Naredimo redukcijo naših preferenc.

    if [] in prefs.values(): # Če se zgodi, da katera oseba nima več preferenc,
        print("no solution exists") # Spet ne obstaja stabilno prirejanje.
        return
    
    
    cikel = zig_zag(prefs, ranks, holds) # Izvedemo zig-zag redukcijo.

    # Sedaj to redukcijo izvajamo dokler obstajajo osebe, ki imajo več kot eno osebo v
    # svojem seznamu preferenc. Ko take osebe ne obstajajo več se zadnja faza zaključi.
    while cikel is not None:

        curpref = {}
        for x in prefs:
            if x in cikel:
                curpref[x] = 1
            else:
                curpref[x] = 0

        holds = faza1(prefs, ranks, curpref) 


        zavrni(prefs, ranks, holds) # Spet naredimo redukcijo in preverimo
                                    # ali se kdaj zgodi, da kakšno osebo vse ostale zavrnejo.
        if [] in prefs.values():
            print("no solution exists")
            return

        cikel = zig_zag(prefs, ranks, holds)

    return(holds)


# Spodnji zakomentiran del kode, je koda katero sva uporabila za izračun časovne zahtevnosti
# algoritma. Pri tem sva s pomočjo funkcije generator(n) spreminjala velikost vhodnih podatkov.

##start = time.time()
##stableroomate("sostanovalci.csv")
##
##end = time.time()
##
##elapsed = end - start
##print(elapsed)


def verjetnostobstoja(dat):
    i=0
    obstoj_rešitve=0
    l=0
    while i<100:
        a=stableroomate(dat)
        if type(a)==dict:
            obstoj_rešitve+=1
        if a==None:
            l+=1
        i+=1
    return(obstoj_rešitve)



