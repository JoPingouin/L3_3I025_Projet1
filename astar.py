
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
        
        
        
        
    def expand(self, WallStates, reserve, taille, frontiere, objectif):
        toRet=[]
        g=Noeud(self.x-1,self.y,self.cout+1)
        #print (self.x, self.y)
        test=False
        for x in frontiere:
            a,b,c=x
            if g.equals(b):
                test=True
                if a > (g.cout + calculheur(g,objectif)):
                    if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
                        toRet.append(g)
        if test==False:
            if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
                toRet.append(g)
            
    
        g=Noeud(self.x,self.y-1,self.cout+1)
        test=False
        for x in frontiere:
            a,b,c=x
            if g.equals(b):
                test=True
                if a > (g.cout + calculheur(g,objectif)):
                    if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
                        toRet.append(g)
        if test==False:
            if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
                toRet.append(g)
            
                
        g=Noeud(self.x+1,self.y,self.cout+1)
        test=False
        for x in frontiere:
            a,b,c=x
            if g.equals(b):
                test=True
                if a > (g.cout + calculheur(g,objectif)):
                    if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
                        toRet.append(g)
        if test==False:
            if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
                toRet.append(g)
        
    
        g=Noeud(self.x,self.y+1,self.cout+1)
        test=False
        for x in frontiere:
            a,b,c=x
            if g.equals(b):
                test=True
                if a > (g.cout + calculheur(g,objectif)):
                    if(not g.isWall(WallStates) and not g.isIn(reserve) and g.x<taille and g.x>=0 and g.y<taille and g.y>=0):
                        toRet.append(g)
        if test==False :
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




def astar(objectif, depart, taille,wall):
    papa=dict()
    nodeGoal = Noeud(objectif[0][0],objectif[0][1],0)
    nodeInit = Noeud(depart[0][0], depart[0][1], 0)
    papa[(nodeInit.x,nodeInit.y)]=None
    frontiere = [(nodeInit.cout+calculheur(nodeInit,objectif),nodeInit,None)] 
    reserve = []       
    bestNoeud = nodeInit
    pere=None
    while frontiere != [] and not bestNoeud.equals(nodeGoal):  
        (min_f,bestNoeud,pere) = heapq.heappop(frontiere)
        if pere!=None:
            papa[(bestNoeud.x,bestNoeud.y)]=(pere.x,pere.y)
        else:
            papa[(bestNoeud.x,bestNoeud.y)]=None

    # Suppose qu'un noeud en réserve n'est jamais ré-étendu 
    # Hypothèse de consistence de l'heuristique
    # ne gère pas les duplicatas dans la frontière
        #print min_f
    
        if not bestNoeud.isIn(reserve):
            reserve.append(bestNoeud) #maj de reserve
            nouveauxNoeuds = bestNoeud.expand(wall,reserve,taille,frontiere,objectif)
            for n in nouveauxNoeuds:
                #print n.x,n.y,bestNoeud.x,bestNoeud.x
                #papa[(n.x,n.y)]=(bestNoeud.x,bestNoeud.y)
                f = n.cout+calculheur(n,objectif)
                heapq.heappush(frontiere, (f,n,bestNoeud))
                #print papa 
        #print "test" ,frontiere

    chemin=[]
    #print frontiere
    bestNoeud=(bestNoeud.x,bestNoeud.y)
    while(bestNoeud != None):
        chemin.append((bestNoeud[0],bestNoeud[1]))
        bestNoeud = papa[(bestNoeud[0],bestNoeud[1])]
    return chemin
    
    
    
    
if __name__=="__main__":
    N=Noeud(1,0,0)
    print calculh([(2,3)], 4)
#    print calculheur(N,[(1,2)])
#    test = [Noeud(1,0,0)]
#    print (Noeud(1,0,0) in test)
#    chemin =[]
#    print N
#    chemin.append(N)
#    print chemin
    print astar([(2,3)],[(0,0)],4,[])
#    a=dict()
#    a[(1,2)]=(1,2)
#    print a

