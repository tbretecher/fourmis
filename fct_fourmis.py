#!/usr/bin/env python3

import random


# defini les coord de depart des points de nourriture
#
# args: mini = coord min de la grille (par ex, 1)
#       maxi = coord max de la grille (par ex, 10)
#       nbcouples = nb de points de nourriture
#
# sortie de la fonction : deux listes contenant respectivement les coord x et y de chaque point de nourriture
#   foodx = liste contenant les coord x de chaque pt
#   foody = liste contenant les coord y de chaque pt
def setFood(mini, maxi, nbcouples):

    x = []
    y = []
    for i in range(mini,(maxi+1)) :
        for j in range(mini, (maxi+1)) :
            x.append(i)
            y.append(j)

    couple_indexes = random.sample(range(maxi*maxi), nbcouples)

    foodx =  [x[ci] for ci in couple_indexes]
    foody =  [y[ci] for ci in couple_indexes]

    return foodx, foody
