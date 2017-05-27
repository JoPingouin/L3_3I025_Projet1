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
import copy
import tools




    
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
    no_bypass=False
    for i in range(len(players)):
        preferences.append({})
    for i in range(len(preferences)):
        pref=[10,7,2]
        random.shuffle(pref)
        preferences[i]['r'] =pref[0]
        preferences[i]['b'] =pref[1]
        preferences[i]['j'] =pref[2]
    nbfioleprise=[[0,0,0],[0,0,0]] #[R,B,J]
    #print (preferences)
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

            
        #print (iteration)
        
        guesspref=[[-1,-1,-1],[-1,-1,-1]]    
        cpt=0 #Pour mettre a jour les préférebce que au début de chaque manche
        while len(fioles)> 0 :
            cpt+=1
            for j in range(nbPlayers):
                #print (j)
                if iteration==0 or j==1:
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
                        posPlayers[j]=(row,col)
                        players[j].ramasse(game.layers)
                        tools.prise(fioles[(row,col)],nbfioleprise,j)#A METTRE DANS TOUTES LES IA
                        score[j]+=(preferences[j][fioles[(row,col)]])
                        fioles.pop((row,col))
                        if len(fioles)==0:
                            break
                        continue
        
        
                    for i in fioles :
                        tmp=preferences[j][fioles[i]]
                        chemin=astar.astar([i],[posPlayers[j]],20,wallStates)
                        for l in {-2,-1,0,1,2}: #carré de 5 x 5
                            for c in {-2,-1,0,1,2}:
                                ligne,colone=i
                                ligne+=l
                                colone+=c
                                if ((ligne,colone) in fioles):
                                    if (len(astar.astar([(ligne,colone)],[i],20,wallStates)) <=9 ):
                                        tmp+=preferences[j][fioles[(ligne,colone)]]
                                        
                                
                        ratio=(1.0* tmp)/(1.0*len(chemin))
                        tabfiole[ratio]=i
                    best=max(tabfiole.keys())
                    chemin=astar.astar([tabfiole[best]],[posPlayers[j]],20,wallStates)
                    if (len(chemin) == 1 and chemin[0]==posPlayers[j]):
                        players[j].ramasse(game.layers)
                        tools.prise(fioles[(row,col)],nbfioleprise,j)#A METTRE DANS TOUTES LES IA
                        game.mainiteration()
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
                        tools.prise(fioles[(row,col)],nbfioleprise,j)#A METTRE DANS TOUTES LES IA
                        game.mainiteration()                
                        #print ("Objet de couleur ", fioles[(row,col)], " trouvé par le joueur ", j, "a l emplacement",(row,col))
                        score[j]+=(preferences[j][fioles[(row,col)]])
                        fioles.pop((row,col))   # on enlève cette fiole de la liste
                        if len(fioles)==0:
                            break
    
                    
                    
                    
                else:
                    #print("test")
                    if cpt==1:
                        print(nbfioleprise)
                        
                        #print("3 fois en une partie")
                        nbfioleprisetmp=copy.deepcopy(nbfioleprise)
                        for a in range(0,3):
                            tmp=nbfioleprisetmp[(j+1)%2].index(max(nbfioleprisetmp[(j+1)%2]))
                            if tmp==0:
                                guesspref[j][a]='r'
                            if tmp==1:
                                guesspref[j][a]='b'
                            if tmp==2:
                                guesspref[j][a]='j'
                            nbfioleprisetmp[(j+1)%2][tmp]=-1
                    print(guesspref)                       
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
        
                    if(bypass==True and no_bypass==False):
                        players[j].set_rowcol(row,col)
                        game.mainiteration()
                        posPlayers[j]=(row,col)
                        players[j].ramasse(game.layers)
                        tools.prise(fioles[(row,col)],nbfioleprise,j)#A METTRE DANS TOUTES LES IA
#                        print("#######################")
#                        print("BYPASS")
#                        print ("Objet de couleur ", fioles[(row,col)], " trouve par le joueur ", j, "a l emplacement",(row,col))
#                        print("donne : ",(preferences[j][fioles[(row,col)]])," points ")                        
#                        print("#######################")
                        score[j]+=(preferences[j][fioles[(row,col)]])
                        fioles.pop((row,col))

                        if len(fioles)==0:
                            break
                        continue
                    no_bypass=False
                    test_pref_dix=False
                    test_pref_sept=False
                    test_default=False
#                    print("------------------------------------")
#                    print("Joueur",j)
#                    print(guesspref[j])
#                    print(preferences[j])
#                    print("------------------------------------")
#                    print (" ")
                    
                    for i in fioles :
                        if fioles[i]==guesspref[j][0] and preferences[j][guesspref[j][0]] != 2:
                            notre_len=len(astar.astar([i],[posPlayers[j]],20,wallStates))
                            son_len=len(astar.astar([i],[posPlayers[(j+1)%2]],20,wallStates))
                            #print("++++++++++++++++")
                            #print ("entre attaque sur 10 points")
                            #print ("notre_len : ",notre_len," son_len : ",son_len)
                            if notre_len<son_len or (notre_len==son_len and j<((j+1)%2)) :#2eme partie : si la longueur est égale mais il joue en premier, il arrivera avant 
                                #print("attaque prevu")
                                tabfiole[notre_len]=i
                                test_pref_dix=True
                                if son_len-notre_len <=1:
                                    #print("pas de bypass attauqe 10")
                                    no_bypass=True                                    
                                    
                                    
                        if fioles[i]==guesspref[j][1] and test_pref_dix!=True and preferences[j][guesspref[j][1]]!=2:
                            notre_len=len(astar.astar([i],[posPlayers[j]],20,wallStates))
                            son_len=len(astar.astar([i],[posPlayers[(j+1)%2]],20,wallStates))
                            #print("++++++++++++++++")
                            #print ("entre attaque sur 7 points")
                            #print ("notre_len : ",notre_len," son_len : ",son_len)
                            if (notre_len<son_len) or (notre_len==son_len and j<((j+1)%2)):#2eme partie : si la longueur est égale mais il joue en premier, il arrivera avant 
                                #print("attaque prevu")
                                tabfiole[notre_len]=i
                                test_pref_sept=True
                                if son_len-notre_len <=1:
                                    #print("pas de bypass attaque 7")
                                    no_bypass=True
                        
                        
                        
                        
                    if test_pref_dix==False and test_pref_sept==False :
                        #print("attaque n ont pas marche : default ")
                        for i in fioles :
                            tmp=preferences[j][fioles[i]]
                            chemin=astar.astar([i],[posPlayers[j]],20,wallStates)
                            for l in {-2,-1,0,1,2}: #carré de 5 x 5
                                for c in {-2,-1,0,1,2}:
                                    ligne,colone=i
                                    ligne+=l
                                    colone+=c
                                    if ((ligne,colone) in fioles):
                                        if (len(astar.astar([(ligne,colone)],[i],20,wallStates)) <=9 ):
                                            tmp+=preferences[j][fioles[(ligne,colone)]]
                                            
                                    
                            ratio=(1.0* tmp)/(1.0*len(chemin))
                            tabfiole[ratio]=i
                        test_default=True


                    if (test_default==True):
                        #print("default")
                        best=max(tabfiole.keys())
                    else :
                        #print("attaque")
                        best=min(tabfiole.keys())
			#print(best)
                        
                    chemin=astar.astar([tabfiole[best]],[posPlayers[j]],20,wallStates)
                    if (len(chemin) == 1 and chemin[0]==posPlayers[j]):
                        players[j].ramasse(game.layers)
                        tools.prise(fioles[(row,col)],nbfioleprise,j)#A METTRE DANS TOUTES LES IA
                        game.mainiteration()
                        score[j]+=(preferences[j][fioles[(row,col)]])
                        fioles.pop((row,col))
                        del tabfiole[best]
                              
                        if (len(tabfiole)==0):
                            for i in fioles:                #regle bug : si il y a une fiole au spawn et
                                tabfiole[1]=i               #que cette fioles est la seule a avoir été mise dans tabfiole
                                break                       #i.e. c est une des meilleurs préférence de l autre et que c est la seule qu il a décidé d attaquer 
                                                            #(les autres sont plus proches de l adversaire que de lui)
                            
                        
                        
                        if (test_default==True):
                            best=max(tabfiole.keys())
                        else :
                            best=min(tabfiole.keys())
                        chemin=astar.astar([tabfiole[best]],[posPlayers[j]],20,wallStates)
                        
                    row,col=chemin[-2]
                    players[j].set_rowcol(row,col)
                    game.mainiteration()
                    posPlayers[j]=(row,col)
            
                    if (row,col) in fioles:
                        o = players[j].ramasse(game.layers)
                        tools.prise(fioles[(row,col)],nbfioleprise,j)#A METTRE DANS TOUTES LES IA
                        game.mainiteration()                
                        #print ("Objet de couleur ", fioles[(row,col)], " trouve par le joueur ", j, "a l emplacement",(row,col))
                        #print("donne : ",(preferences[j][fioles[(row,col)]])," points ")                                                
                        score[j]+=(preferences[j][fioles[(row,col)]])
                        fioles.pop((row,col))   # on enlève cette fiole de la liste
                        if len(fioles)==0:
                            break
            
            
            
            
            
            
                    
                    
                    
                    
        #print("ceci doit etre vide : ",fioles)
        #print (" ")
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
        print("\n====================================================")
        print ("player 0 : ",resultat[0]," player 1 : ",resultat[1])
        print("\n====================================================")
        
    


