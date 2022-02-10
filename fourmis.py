#!/usr/bin/env python3
from random import randint
from statistics import mean
import argparse
import ant_animate
import fct_fourmis


# TODO tourner jusqu'à ce que toutes fourmis mortes plutôt que tours

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--nb-fourmis', default=20, type=int,
                    help='Le nombre de fourmis (20 par défaut).')
parser.add_argument('-n', '--nb-nourriture', default=10, type=int,
                    help='Le nombre de points de nourriture (10 par défaut).')
parser.add_argument('-v', '--pv-max', default=20, type=int,
                    help='Les points des vie des fourmis au début de la simulation (20 par défaut).')
parser.add_argument('-t', '--tours', default=20, type=int,
                    help='Le nombre de tours de simulation (20 par défaut).')
parser.add_argument('-p', '--trophallaxie', action='store_true',
                    help='Active le partage de nourriture.')
parser.add_argument('-g', '--graphique', action='store_true',
                    help="Active l'affichage graphique.")
args = parser.parse_args()

mincoord = 0
maxcoord = 20

# TODO fonctions pour initialiser d_fourmis et food
d_fourmis = {}
for i in range(args.nb_fourmis):
    d_fourmis[i] = {'x': [randint(mincoord, maxcoord)],
                    'y': [randint(mincoord, maxcoord)],
                    'pv': [args.pv_max]}
foodx, foody = fct_fourmis.setFood(mincoord, maxcoord, args.nb_nourriture)


for tour in range(args.tours):
    # déplacement et dépense énergie
    for i in d_fourmis.keys():
        # si la fourmi a plus de la moitié de ses pv
        # OU qu'elle a plus de 0 pv
        # ET une chance sur deux
        if (d_fourmis[i]['pv'][tour] > (args.pv_max / 2)
                or d_fourmis[i]['pv'][tour] > 0
                and randint(0, 1) == 1):
            # alors elle bouge
            # si elle dépasse une limite, elle se déplace sur le bord opposé
            direction = randint(0, 3)
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
            # la fourmi est mort
            d_fourmis[i]['x'].append(d_fourmis[i]['x'][tour])
            d_fourmis[i]['y'].append(d_fourmis[i]['y'][tour])
            d_fourmis[i]['pv'].append(0)

        # recharge énergie quand fourmie est sur un point de nourriture nomnom
        for j in range(args.nb_nourriture):
            if (d_fourmis[i]['x'][tour+1] == foodx[j]
                    and d_fourmis[i]['y'][tour+1] == foody[j]
                    and d_fourmis[i]['pv'][tour] > 0):
                d_fourmis[i]['pv'][tour+1] = args.pv_max

    # partage de nourriture
    # TODO nettoyer ce bordel
    if args.trophallaxie is True:
        # coors des fourmis à ce tour:
        xcoor = [d_fourmis[k]['x'][tour+1] for k in d_fourmis.keys()]
        ycoor = [d_fourmis[k]['y'][tour+1] for k in d_fourmis.keys()]
        # transforme deux listes en liste de tuples (x,y):
        coors = list(zip(xcoor, ycoor))
        # récupère toutes les valeurs en double
        # (càd les cases où il y a plusieurs fourmies):
        coor_dupli = [dup for dup in coors if coors.count(dup) > 1]
        # créé une liste des valeurs en double sans duplicats:
        coor_uni_dupli = list(set(coor_dupli))
        print(coor_uni_dupli)
        # si il y a des valeurs en double:
        if coor_uni_dupli:
            # pour chaque valeur en double:
            for x, y in coor_uni_dupli:
                # créé une liste des noms des fourmies sur cette case
                k_coor = [k for k in d_fourmis.keys()
                          if d_fourmis[k]['x'][tour+1] == x
                          and d_fourmis[k]['y'][tour+1] == y]
                print(k_coor)
                # créé une liste des pvs des fourmies sur cette case
                pvs = [d_fourmis[k]['pv'][tour+1] for k in k_coor]
                print(pvs)
                # calcule les pvs après partage
                partage = int(mean(pvs))
                print(partage)
                # assigne les pvs après partage aux fourmies sur la case
                for k in k_coor:
                    d_fourmis[k]['pv'][tour+1] = partage
                    print('Trophallaxie !', tour)


if args.graphique is True:
    # utilise le module d'affichage graphique
    # TODO interface graphique maison ? -> pygames
    ant_app = ant_animate.Visual_App(d_fourmis, foodx, foody, args.pv_max)
    ant_app.run()
else:
    # affiche d_fourmis
    print(d_fourmis)
