#!/usr/bin/env python3
from random import randint
from random import sample
from statistics import mean
import argparse
import ant_animate


# TODO tourner jusqu'à ce que toutes fourmis mortes plutôt que tours
# TODO grille commence à 1 ?

# définit les options qu'on peut passer au programme
parser = argparse.ArgumentParser()
# nombre de foumis
parser.add_argument('-f', '--nb-fourmis', default=20, type=int,
                    help='Le nombre de fourmis (20 par défaut).')
# nombre de points de nourriture
parser.add_argument('-n', '--nb-nourriture', default=10, type=int,
                    help='Le nombre de points de nourriture (10 par défaut).')
# points de vie max des fourmis
parser.add_argument('-v', '--pv-max', default=20, type=int,
                    help='Les points des vie des fourmis au début de la simulation (20 par défaut).')
# nombre de tours de simulation
parser.add_argument('-t', '--tours', default=20, type=int,
                    help='Le nombre de tours de simulation (20 par défaut).')
# trophallaxie (partage de nourriture entre fourmis) ou non
parser.add_argument('-p', '--trophallaxie', action='store_true',
                    help='Active le partage de nourriture.')
# affichage graphique ou non
parser.add_argument('-g', '--graphique', action='store_false',
                    help="Désactive l'affichage graphique.")
# et stocke toutes les valeurs dans un objet
args = parser.parse_args()

mincoord = 0
maxcoord = 20

# fonction pour initialiser food (la liste de tous les points de nourriture)
# et d_foumis (un dictionnaire qui contient les coordonées et le nombre de
# points de vie de chaque fourmis à chaque tour) en tirant au hasard des
# coordonées parmi toutes les coordonées possibles
def init(nb_fourmis, nb_nourriture, pv_max, mincoord, maxcoord):
    # génère une liste de toutes les coordonées possibles
    all_coords = [(x, y) for x in range(mincoord, maxcoord)
                         for y in range(mincoord, maxcoord)]
    ant_dict = {i: {'coords': sample(all_coords, 1),
                    'life': [pv_max]}
                for i in range(nb_fourmis)}
    food = sample(all_coords, nb_nourriture)
    return food, ant_dict

food, d_fourmis = init(args.nb_fourmis, args.nb_nourriture, args.pv_max, mincoord, maxcoord)


for tour in range(args.tours):
    # déplacement et dépense énergie
    for i in d_fourmis:
        # si la fourmi a plus de la moitié de ses pv
        # OU qu'elle a plus de 0 pv
        # ET une chance sur deux
        if (d_fourmis[i]['life'][tour] > (args.pv_max / 2)
                or d_fourmis[i]['life'][tour] > 0
                and randint(0, 1) == 1):
            # alors elle bouge
            # si elle dépasse une limite, elle se déplace sur le bord opposé
            direction = randint(0, 3)
            if direction == 0:
                # déplacement vers le haut
                d_fourmis[i]['coords'].append((((d_fourmis[i]['coords'][tour][0] + 1) % maxcoord),
                                              (d_fourmis[i]['coords'][tour][1])))
            elif direction == 1:
                # déplacement vers le bas
                d_fourmis[i]['coords'].append((((d_fourmis[i]['coords'][tour][0] - 1) % maxcoord),
                                              (d_fourmis[i]['coords'][tour][1])))
            elif direction == 2:
                # déplacement vers la droite
                d_fourmis[i]['coords'].append(((d_fourmis[i]['coords'][tour][0]),
                                              ((d_fourmis[i]['coords'][tour][1] + 1) % maxcoord)))
            else:
                # déplacement vers la gauche
                d_fourmis[i]['coords'].append(((d_fourmis[i]['coords'][tour][0]),
                                              ((d_fourmis[i]['coords'][tour][1] - 1) % maxcoord)))
            d_fourmis[i]['life'].append(d_fourmis[i]['life'][tour] - 2)

        elif d_fourmis[i]['life'][tour] > 0:
            # la fourmi reste immobile
            d_fourmis[i]['coords'].append(d_fourmis[i]['coords'][tour])
            d_fourmis[i]['life'].append(d_fourmis[i]['life'][tour] - 1)

        else:
            # la fourmi est morte
            d_fourmis[i]['coords'].append(d_fourmis[i]['coords'][tour])
            d_fourmis[i]['life'].append(0)

        # recharge énergie quand fourmie est sur un point de nourriture nomnom
        if (d_fourmis[i]['coords'][tour+1] in food
                and d_fourmis[i]['life'][tour] > 0):
            d_fourmis[i]['life'][tour+1] = args.pv_max

    # partage de nourriture
    if args.trophallaxie is True:
        # coors des fourmis à ce tour:
        coors_tour = [d_fourmis[f]['coords'][tour+1] for f in d_fourmis.keys()]
        # récupère toutes les valeurs en double
        # (càd les cases où il y a plusieurs fourmies):
        coors_tropha = list(set([dup for dup in coors_tour if coors_tour.count(dup) > 1]))
        # si il y a des valeurs en double:
        if coors_tropha:
            # pour chaque valeur en double:
            for coor in coors_tropha:
                # créé une liste des noms des fourmies sur cette case
                fourm_coor_tropha = [f for f in d_fourmis.keys()
                                       if d_fourmis[f]['coords'][tour+1] == coor]
                # créé une liste des pvs des fourmies sur cette case
                pvs = [d_fourmis[f]['life'][tour+1] for f in fourm_coor_tropha]
                # calcule les pvs après partage
                partage = int(mean(pvs))
                # assigne les pvs après partage aux fourmies sur la case
                for f in fourm_coor_tropha:
                    d_fourmis[f]['life'][tour+1] = partage


if args.graphique is True:
    # utilise le module d'affichage graphique
    # TODO interface graphique maison ? -> pygames
    ant_app = ant_animate.Visual_App(d_fourmis, food, args.pv_max)
    ant_app.run()
else:
    # affiche d_fourmis
    print(d_fourmis)
