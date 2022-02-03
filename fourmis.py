from random import randint
from pprint import pprint
from statistics import mean
import ant_animate
import fct_fourmis

# TODO interface ligne de commande propre

nb_fourmis = 20
nb_nourriture = 10
pv_max = 20
tours = 20
trophallaxie = True
gfourmis = False
mincoord = 0
maxcoord = 20

# TODO fonctions pour initialiser d_fourmis et food
d_fourmis = {}
for i in range(nb_fourmis):
    d_fourmis[i] = {'x': [randint(mincoord,maxcoord)],
                    'y': [randint(mincoord,maxcoord)],
                    'pv': [pv_max]}
foodx, foody = fct_fourmis.setFood(mincoord, maxcoord, nb_nourriture)


for tour in range(tours):
    #déplacement et dépense énergie
    for i in d_fourmis.keys():
        # si la fourmi a plus de la moitié de ses pv
        # OU qu'elle a plus de 0 pv
        # ET une chance sur deux
        if (d_fourmis[i]['pv'][tour] > (pv_max / 2)
                or d_fourmis[i]['pv'][tour] > 0
                and randint(0,1) == 1):
            # alors elle bouge
            # si elle dépasse une limite, elle se déplace sur le bord opposé
            direction = randint(0,3)
            if direction == 0:
                # déplacement vers le haut
                d_fourmis[i]['y'].append((d_fourmis[i]['y'][tour] + 1) % maxcoord)
                d_fourmis[i]['x'].append(d_fourmis[i]['x'][tour])
            elif direction == 1:
                # déplacement vers le bas
                d_fourmis[i]['y'].append((d_fourmis[i]['y'][tour] - 1) % maxcoord)
                d_fourmis[i]['x'].append(d_fourmis[i]['x'][tour])
            elif direction == 2:
                # déplacement vers la droite
                d_fourmis[i]['x'].append((d_fourmis[i]['x'][tour] + 1) % maxcoord)
                d_fourmis[i]['y'].append(d_fourmis[i]['y'][tour])
            else:
                # déplacement vers la gauche
                d_fourmis[i]['x'].append((d_fourmis[i]['x'][tour] - 1) % maxcoord)
                d_fourmis[i]['y'].append(d_fourmis[i]['y'][tour])
            d_fourmis[i]['pv'].append(d_fourmis[i]['pv'][tour] - 2)

        elif d_fourmis[i]['pv'][tour] > 0:
            # la fourmi reste immobile
            d_fourmis[i]['x'].append(d_fourmis[i]['x'][tour])
            d_fourmis[i]['y'].append(d_fourmis[i]['y'][tour])
            d_fourmis[i]['pv'].append(d_fourmis[i]['pv'][tour] - 1)

        else:
            # la fourmi est morte
            d_fourmis[i]['x'].append(d_fourmis[i]['x'][tour])
            d_fourmis[i]['y'].append(d_fourmis[i]['y'][tour])
            d_fourmis[i]['pv'].append(0)

        # recharge énergie quand la fourmie est sur un point de nourriture nomnom
        for j in range(nb_nourriture):
            if (d_fourmis[i]['x'][tour+1] == foodx[j]
                    and d_fourmis[i]['y'][tour+1] == foody[j]
                    and d_fourmis[i]['pv'][tour] > 0):
                d_fourmis[i]['pv'][tour+1] = pv_max

    # partage de nourriture
    # TODO
    if trophallaxie == True:
        xcoor = [d_fourmis[k]['x'][tour+1] for k in d_fourmis.keys()]
        ycoor = [d_fourmis[k]['y'][tour+1] for k in d_fourmis.keys()]
        coors = list(zip(xcoor, ycoor))
        coor_dupli = [dup for dup in coors if coors.count(dup) > 1]
        coor_uni_dupli = list(set(coor_dupli))
        print(coor_uni_dupli)
        if coor_uni_dupli != []:
            for x, y in coor_uni_dupli:
                k_coor = [k for k in d_fourmis.keys() if d_fourmis[k]['x'][tour+1] == x and d_fourmis[k]['y'][tour+1] == y]
                print(k_coor)
                pvs = [d_fourmis[k]['pv'][tour+1] for k in k_coor]
                print(pvs)
                partage = int(mean(pvs))
                print(partage)
                for k in k_coor:
                    d_fourmis[k]['pv'][tour+1] = partage
                    print('Trophallaxie !', tour)
                


if gfourmis is True:
    # utilise le module d'affichage graphique
    # TODO interface graphique maison ? -> pygames
    ant_app = ant_animate.Visual_App(d_fourmis, foodx, foody, pv_max)
    ant_app.run()
else:
    # affiche d_fourmis
    # TODO affichage texte plus propre
    print(d_fourmis)
