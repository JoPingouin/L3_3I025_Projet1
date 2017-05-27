# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 14:35:31 2017

@author: 3412470
"""

import numpy as np
import heapq

class Noeud():
    def __init__(self, x, y, cout):
        self.x = x
        self.y = y
        self.cout = cout
    
    def equals(self,N):
        if(self.x==N.x and self.y==N.y):
            return True
        return False

    def isWall(self,liste):
        for i in liste:
            if(self.x==i[0] and self.y==i[1]):
                return True
        return False
        
        
    def isIn(self,liste):
        for i in liste :
            if (self.equals(i)):
                return True
        return False
        
        
        
        
    def expand(self,WallStates,reserve,taille):
        toRet=[]
        g=Noeud(N.x-1,N.y,N.cout+1)
        if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
            toRet.append(g)
            

        g=Noeud(N.x,N.y-1,N.cout+1)
        if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
            toRet.append(g)
            
        g=Noeud(N.x+1,N.y,N.cout+1)
        if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
            toRet.append(g)

        g=Noeud(N.x,N.y+1,N.cout+1)
        if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
            toRet.append(g)
        
        return toRet


"""
"""

def compareNoeuds(n1, n2):
    if n1.h < n2.h :
        return 1
    elif n1.h == n2.h :
        return 0
    else :
        return -1
        
def calculh(goal, taille):
    list = np.zeros((taille,taille))
    print list
    print " "
    for i in range(taille):
        for j in range(taille):
            list[i][j] = abs(goal[0][0]-i)+abs(goal[0][1]-j)
    return list
    

    
def calculheur(N,goal):
    x=N.x
    y=N.y
    return abs(goal[0][0]-x)+abs(goal[0][1]-y)

#def updateFrontiere(File , N):
#    x=N.x
#    y=N.y
#    dansFile=[0,0,0,0]
#    for i in File:
#        if(x-1==i.x and y==i.y):
#            dansFile[0]=1
#        if(x==i.x and y-1==i.y):
#            dansFile[1]=1
#        if(x+1==i.x and y== i.y):
#            dansFile[2]=1
#        if(x==i.x and y+1==i.y):
#            dansFile[3]=1
#        
#        if dansFile[0]==0:
#            print 1
#            heapq.heappush(File,Noeud(x-1,y,0))
#        if dansFile[1]==0:
#            print 2
#            heapq.heappush(File,Noeud(x,y-1,0))
#        if dansFile[2]==0:            
#            print 3
#            heapq.heappush(File,Noeud(x+1,y,0))
#        if dansFile[3]==0:            
#            print 4
#            heapq.heappush(File,Noeud(x,y+1,0))
#            
#    print(File)
        
def recupchemin(liste):
    for i in liste:
        a,b,c=i
        

def astar(objectif, depart, taille,wall):
    pere={}
    nodeGoal = Noeud(objectif[0][0],objectif[0][1],0)
    nodeInit = Noeud(depart[0][0], depart[0][1], 0)
    print nodeInit
    pere[nodeInit]=None
    frontiere = [(nodeInit.cout+calculheur(nodeInit,objectif),nodeInit,None)] 
    reserve = []       
    bestNoeud = nodeInit
    while frontiere != [] and not bestNoeud.equals(nodeGoal):  
        print frontiere

        (min_f,bestNoeud,pere) = heapq.heappop(frontiere)    
        print frontiere
        
    # Suppose qu'un noeud en réserve n'est jamais ré-étendu 
    # Hypothèse de consistence de l'heuristique
    # ne gère pas les duplicatas dans la frontière
    
        if not bestNoeud.isIn(reserve):
            reserve.append(bestNoeud) #maj de reserve
            nouveauxNoeuds = bestNoeud.expand(wall,reserve,taille)
            print nouveauxNoeuds
            for n in nouveauxNoeuds:
                pere[n]=bestNoeud
                f = n.cout+calculheur(n,objectif)
                heapq.heappush(frontiere, (f,n,bestNoeud))
                print "test" ,frontiere

                
    chemin=[]
    #print frontiere
    while(bestNoeud != None):
        print bestNoeud
        chemin.append(bestNoeud)
        print "test"
        bestNoeud = reserve[reserve.index(bestNoeud)]
    return chemin
    
    
    
    
if __name__=="__main__":
    N=Noeud(1,0,0)
#    print calculh([(1,2)], 4)
#    print calculheur(N,[(1,2)])
#    test = [Noeud(1,0,0)]
#    print (Noeud(1,0,0) in test)
#    chemin =[]
#    print N
#    chemin.append(N)
#    print chemin
    #astar([(2,3)],[(0,0)],4,[])
    a=dict()
    a["test"]=3
    print a
