# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys
import astar




    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----


game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'match2'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps =  300 # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():
    
    #for arg in sys.argv:
#    iterations = 200 # default
#    if len(sys.argv) == 2:
#        iterations = int(sys.argv[1])
    init()

    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    fioles = {} # dictionnaire (x,y)->couleur pour les fioles
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    #print ("Init states:", initStates)
    
    
    # on localise tous les objets ramassables
    #goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    #print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    #-------------------------------
    # Placement aleatoire des fioles de couleur 
    #-------------------------------
                   

    #print("Les fioles ont été placées aux endroits suivants: \n\n", fioles)
    preferences=[]
    fiole_prise=-1 #A METTRE DANS TOUTES LES IA
    for i in range(len(players)):
        preferences.append({})
    for i in range(len(preferences)):
        pref=[10,7,2]
        random.shuffle(pref)
        preferences[i]['r'] =pref[0]
        preferences[i]['b'] =pref[1]
        preferences[i]['j'] =pref[2]
    #print (preferences)
    posPlayers = initStates
    
    for iteration in range(0,4):
        if iteration!=0:
            init()
            players = [o for o in game.layers['joueur']]
            initStates = [o.get_rowcol() for o in game.layers['joueur']]
            wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
            nbPlayers = len(players)
            fioles = {}
        posPlayers = initStates
        posPlayers = [(18, 1), (1, 18)]
        for o in game.layers['ramassable']: # on considère chaque fiole
            if o.tileid == (19,0): # tileid donne la coordonnee dans la fiche de sprites
                couleur = 'r'
            elif o.tileid == (19,1):
                couleur = 'j'
            else:
                couleur = 'b'
    
            # et on met la fiole qqpart au hasard
    
            x = random.randint(1,19)
            y = random.randint(1,19)
    
            while (x,y) in wallStates: # ... mais pas sur un mur
                x = random.randint(1,19)
                y = random.randint(1,19)
            o.set_rowcol(x,y)
            # on ajoute cette fiole 
            fioles[(x,y)]=couleur
    
            game.layers['ramassable'].add(o)
            game.mainiteration()
    
    
    
    
        while len(fioles)> 0 :
            for j in range(nbPlayers):
                row,col=posPlayers[j]
                tabfiole={}
                bypass=False
                if (row+1,col) in fioles:
                    row=row+1
                    bypass=True
                if (row-1,col) in fioles:
                    row=row-1
                    bypass=True
                if (row,col+1) in fioles:
                    col=col+1
                    bypass=True
                if (row,col-1) in fioles:
                    col=col-1
                    bypass=True
    
                if(bypass==True):
                    players[j].set_rowcol(row,col)
                    game.mainiteration()
                    fiole_prise=fioles[(row,col)] #A METTRE DANS TOUTES LES IA
                    posPlayers[j]=(row,col)
                    players[j].ramasse(game.layers)
#                    print ("Objet de couleur ", fioles[(row,col)], " trouve par le joueur ", j, "a l emplacement",(row,col))
#                    print("points gagne : ",(preferences[j][fioles[(row,col)]]))
#                    print("score actuel : ",score[j])
                    score[j]+=(preferences[j][fioles[(row,col)]])
                    fioles.pop((row,col))
                    if len(fioles)==0:
                        break
                    continue
    
    
                for i in fioles :
                    chemin=astar.astar([i],[posPlayers[j]],20,wallStates)
                    ratio=(1.0*preferences[j][fioles[i]])/(1.0*len(chemin))
                    tabfiole[ratio]=i
                best=max(tabfiole.keys())
                chemin=astar.astar([tabfiole[best]],[posPlayers[j]],20,wallStates)
                if (len(chemin) == 1 and chemin[0]==posPlayers[j]):
                    players[j].ramasse(game.layers)
                    game.mainiteration()
#                    print ("Objet de couleur ", fioles[(row,col)], " trouve par le joueur ", j, "a l emplacement",(row,col))
#                    print("points gagne : ",(preferences[j][fioles[(row,col)]]))
#                    print("score actuel : ",score[j])
                    score[j]+=(preferences[j][fioles[(row,col)]])
                    fioles.pop((row,col))
                    del tabfiole[best]
                    best=max(tabfiole.keys())
                    chemin=astar.astar([tabfiole[best]],[posPlayers[j]],20,wallStates)
                    
                row,col=chemin[-2]
                players[j].set_rowcol(row,col)
                game.mainiteration()
                posPlayers[j]=(row,col)
        
                if (row,col) in fioles:
                    o = players[j].ramasse(game.layers)
                    game.mainiteration()                
                    fiole_prise=fioles[(row,col)] #A METTRE DANS TOUTES LES IA
#                    print ("Objet de couleur ", fioles[(row,col)], " trouve par le joueur ", j, "a l emplacement",(row,col))
#                    print("points gagne : ",(preferences[j][fioles[(row,col)]]))
#                    print("score actuel : ",score[j])
                    score[j]+=(preferences[j][fioles[(row,col)]])
                    fioles.pop((row,col))   # on enlève cette fiole de la liste
                    if len(fioles)==0:
                        break
    
    print ("scores:", score)
    #print (fioles)
    if(score[0]>score[1]):
        pygame.quit()
        return 0
    else :
        pygame.quit()
        return 1
        

if __name__ == '__main__':
    resultat=[0,0]
    
    while(True):
        ret=main()
        resultat[ret]+=1
        print ("player 0 : ",resultat[0]," player 1 : ",resultat[1])
    


