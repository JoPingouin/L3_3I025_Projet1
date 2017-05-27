# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 23:00:43 2017

@author: julie_000
"""

def prise(couleur,nbfiole_prise,j):#[R,B,J]
    if couleur=='r':
        nbfiole_prise[j][0]+=1
    if couleur=='b':
        nbfiole_prise[j][1]+=1
    if couleur=='j':
        nbfiole_prise[j][2]+=1
    return nbfiole_prise
    
    
def point(guesspref,couleur,j):
    tmp=guesspref[j].index(couleur)
    if tmp==0:
        return 10
    if tmp==1:
        return 7
    if tmp==2:
        return 2