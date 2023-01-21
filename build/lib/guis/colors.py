import math
import pygame
from pygame.locals import *
import json as jsonmod
import random
import glob
import importlib
import sys
import os
import pathlib
import difflib
import zipfile
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pylab

white = (255,255,255)
black = (0,0,0)
grey = (128, 128, 128)
lgrey = (200, 200, 200)
dgrey = (28, 28, 28)

red = (155,0,0)
lred = (255,0,0)
dred = (55,0,0)

green = (0,155,0)
ygreen = (55,155,0)
lgreen = (0,255,0)
dgreen = (0,55,0)

blue = (0,0,155)
lblue = (0,0,255)
dblue = (0,0,55)

purple = (75,0,155)
dpurple = (25,0,55)
drpurple = (55,0,25)
lpurple = (170,0,255)

lyellow = (255, 255, 0)
yellow = (155, 155, 0)
dyellow = (55, 55, 0)

drawalpha = (0,0,0,0)

def gradientizecolor(
surface,color=(255,255,255),gradient=(255,255,255),togradient=(0,0,0),rect=None,
vertical=True,forward=True,flip=True):
    a1 = pygame.surfarray.pixels3d(surface)
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    h = y2-y1
    w = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    if forward:
        inv = 1
    else:
        inv = -1
    if togradient == None or togradient=="None": togradient=(0,0,0)
    cr,cg,cb = togradient
    #print(cr,cg,cb)
    if vertical:
        rate = (
            float(b[0]-a[0])/h,
            float(b[1]-a[1])/h,
            float(b[2]-a[2])/h
        )
    else:
        if forward:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
        else:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
    i = -1
    i1 = -1
    for a2 in a1:
        i+=1
        i1=-1
        for p in a2:
                i1+=1
                if p[0]==cr and p[1]==cg and p[2]==cb:
                    if vertical:
                        color = (
                            min(max((a[0]+rate[0]*(i)),0),255),
                            min(max((a[1]+rate[1]*(i)),0),255),
                            min(max((a[2]+rate[2]*(i)),0),255)
                        )
                    else:
                        if flip:
                            color = (
                                min(max((a[0]+rate[0]*(i1)),0),255),
                                min(max((a[1]+rate[1]*(i)),0),255),
                                min(max((a[2]+rate[2]*(i)),0),255)
                            )
                        else:
                            color = (
                                min(max((a[0]+rate[0]*((i+i1)/2 )),0),255),
                                min(max((a[1]+rate[1]*((i+i1)/2)),0),255),
                                min(max((a[2]+rate[2]*((i+i1)/2)),0),255)
                            )
                    #print(p)
                    a1[i,i1] = color
            #print(p)
    return surface

def gradientizewhite(
    surface,color,gradient,rect=None,
    vertical=True,forward=True,flip=True):

    if rect is None: rect = surface.get_rect()
    a1 = pygame.surfarray.pixels3d(surface)
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    h = y2-y1
    w = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    if forward:
        inv = 1
    else:
        inv = -1
    if vertical:
        rate = (
            float(b[0]-a[0])/h,
            float(b[1]-a[1])/h,
            float(b[2]-a[2])/h
        )
    else:
        if forward:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
        else:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
    i = -1
    i1 = -1
    for a2 in a1:
        i+=1
        i1=-1
        for p in a2:
            i1+=1
            if p[0]!=0 and p[1]!=0 and p[2]!=0:
                if vertical:
                    color = (
                        min(max((a[0]+rate[0]*(i)),0),255),
                        min(max((a[1]+rate[1]*(i)),0),255),
                        min(max((a[2]+rate[2]*(i)),0),255)
                    )
                else:
                    if flip:
                        color = (
                            min(max((a[0]+rate[0]*(i1)),0),255),
                            min(max((a[1]+rate[1]*(i)),0),255),
                            min(max((a[2]+rate[2]*(i)),0),255)
                        )
                    else:
                        color = (
                            min(max((a[0]+rate[0]*((i+i1)/2)),0),255),
                            min(max((a[1]+rate[1]*((i+i1)/2)),0),255),
                            min(max((a[2]+rate[2]*((i+i1)/2)),0),255)
                        )
                #print(p)
                a1[i,i1] = color
            #print(p)
    return surface

def gradientizeblack(
    surface,color,gradient,rect=None,
    vertical=True,forward=True,flip=True):
    a1 = pygame.surfarray.pixels3d(surface)
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    h = y2-y1
    w = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    if forward:
        inv = 1
    else:
        inv = -1
    if vertical:
        rate = (
            float(b[0]-a[0])/h,
            float(b[1]-a[1])/h,
            float(b[2]-a[2])/h
        )
    else:
        if forward:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
        else:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
    i = -1
    i1 = -1
    for a2 in a1:
        i+=1
        i1=-1
        for p in a2:
            i1+=1
            if p[0]==0 and p[1]==0 and p[2]==0:
                if vertical:
                    color = (
                        min(max((a[0]+rate[0]*(i)),0),255),
                        min(max((a[1]+rate[1]*(i)),0),255),
                        min(max((a[2]+rate[2]*(i)),0),255)
                    )
                else:
                    if flip:
                        color = (
                            min(max((a[0]+rate[0]*(i1)),0),255),
                            min(max((a[1]+rate[1]*(i)),0),255),
                            min(max((a[2]+rate[2]*(i)),0),255)
                        )
                    else:
                        color = (
                            min(max((a[0]+rate[0]*((i+i1)/2)),0),255),
                            min(max((a[1]+rate[1]*((i+i1)/2)),0),255),
                            min(max((a[2]+rate[2]*((i+i1)/2)),0),255)
                        )
                #print(p)
                a1[i,i1] = color
            #print(p)
    return surface

def gradientizeall(
surface,color,gradient,rect=None,
vertical=True,forward=True,flip=True):
    a1 = pygame.surfarray.pixels3d(surface)
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    h = y2-y1
    w = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    if forward:
        inv = 1
    else:
        inv = -1
    if vertical:
        rate = (
            float(b[0]-a[0])/h,
            float(b[1]-a[1])/h,
            float(b[2]-a[2])/h
        )
    else:
        if forward:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
        else:
            rate = (
                float(b[0]-a[0])/w,
                float(b[1]-a[1])/w,
                float(b[2]-a[2])/w
            )
    i = -1
    i1 = -1
    for a2 in a1:
        i+=1
        i1=-1
        for p in a2:
                i1+=1
            #if p[0]!=0 and p[1]!=0 and p[2]!=0:
                if vertical:
                    color = (
                        min(max((a[0]+rate[0]*(i)),0),255),
                        min(max((a[1]+rate[1]*(i)),0),255),
                        min(max((a[2]+rate[2]*(i)),0),255)
                    )
                else:
                    if flip:
                        color = (
                            min(max((a[0]+rate[0]*(i1)),0),255),
                            min(max((a[1]+rate[1]*(i)),0),255),
                            min(max((a[2]+rate[2]*(i)),0),255)
                        )
                    else:
                        color = (
                            min(max((a[0]+rate[0]*((i+i1)/2 )),0),255),
                            min(max((a[1]+rate[1]*((i+i1)/2)),0),255),
                            min(max((a[2]+rate[2]*((i+i1)/2)),0),255)
                        )
                #print(p)
                a1[i,i1] = color
            #print(p)
    return surface
