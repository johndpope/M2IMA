# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 00:04:07 2015

@author_id: 3410735
@author_name: BIRGUI SEKOU Taibou
"""

import numpy as np
import Image
import time

class Hypergraph:
    def __init__(self, _img):
        self.img  = _img
        self.size = _img.size # size(img);
    
    def construct(self):
        E = []
        t = time.time()
        print 'Hypergraph building ...'
        for i in range(self.size[0]):
            E.append([])
            for j in range( self.size[1]):
                E[i].append([])
                neighboors = self.neighboors(i,j)
                alpha = np.std(neighboors[:, 1])
                gamma = set()
                for k in range(neighboors.shape[0]):
                    if self.distance(neighboors[k, 1], self.img.getpixel((i,j))) <= alpha:
                        gamma.add(neighboors[k, 0])
                E[i][j] = gamma
        self.hyper = np.array(E)
        self.runtime = time.time() -t
        print 'Building runtime : ', self.runtime 
    
    def neighboors(self, _i, _j):
        # 8 connexité
        neighboors = []
        for k in range(-1,2):
            for l in range(-1,2):
                a = mod(_i -k, self.size[0]) 
                b = mod(_j -l, self.size[1]) 
                #print a, '  ', b
                neighboors.append([(a, b), self.img.getpixel((a, b))])
        return np.array(neighboors)  
    
    def distance(self, _a, _b):
        return abs(_a-_b)

class Tools:
    @staticmethod
    def read_image(_filename ='../images/image_0005.jpg'):
        img = Image.open(_filename) # read(_filename)
        return img


class HyperTools:
    @staticmethod
    def open_neighborhood(H, IS, ISO, x):
        print 'enter : s(IS) = ',IS.shape, ' , s(ISO) = ', ISO.shape 
        # initialisation : gathering elements of IS and ISO
        isos = ISO[:,1] if len(ISO) else []
        iss  = IS[:,1]
        sets = set()
        if isos != []:
            for iso in isos:
                sets = sets.union(set(iso))
        for i in iss:
            sets = sets.union(set(i))
        print 'init'
        # building open neighborhood 
        Ex  = set(IS[x,1])
        print 'neighbors'
        open_ng = set()
        while Ex != set([]):
            el      = Ex.pop()
            open_ng = open_ng.union(H[el[0], el[1]])
            open_ng.discard(el)
        print 'open'
        # for each element in open neighborhood, check if its neighbors in IS or ISO
        stock = open_ng.copy()
        while stock != set([]):
            y  = stock.pop()
            Ey = H[y[0], y[1]]
            print 'stock : ', stock
            print 'y : ',y, ' ::: Ey ',  Ey 
            if sets.issuperset(Ey):
                return True
        return False
    
    @staticmethod    
    def noise_detection(_img, _hyper):
        ISO = []
        IS  = []
        NH  = []
        # Determination of isolated hyperedges of _hyper
        for i in range(_hyper.hyper.shape[0]):
            for j in range(_hyper.hyper.shape[1]):
                ng = set(_hyper.neighboors(i, j)[:, 0])
                ex = ng.intersection(_hyper.hyper[i,j])
                #print 'ng : ', ng
                #print 'ex : ', ex
                #if ex == ng: # ex is an isolated hyperedge
                if len(ng) == 1:
                    ISO.append([(i,j), ng])
                else:
                    IS.append([(i,j), ng])
        ISO = np.array(ISO)
        IS  = np.array(IS)
        # Detection of noise hyperedges of _hyper
        for x in range(ISO.shape[0]):
            ngx = set(_hyper.neighboors(ISO[x, 0][0], ISO[x, 0][1])[:, 0])
            for y in range(x, ISO.shape[0]):
                py = set([ISO[y, 0]])
                for z in range(y, ISO.shape[0]):        
                    pz = set([ISO[z, 0][0]])
                    if py.isdisjoint(ngx) and pz.isdisjoint(ngx):
                        NH.append(ISO[x])
        for x in range(IS.shape[0]):
            if HyperTools.open_neighborhood(_hyper.hyper, IS, ISO, x):
                NH.append(IS[x])
        NH = np.array(NH)
        return ISO, IS, NH
    
    @staticmethod
    def denoising(_img, _hyper):
        ISO, IS, NH = HyperTools.noise_detection(_img, _hyper)
        res = _img.copy()
        for i in range(NH.shape[0]):
            res.putpixel(NH[i, 0], 0)
        return res #, ISO, IS, NH
    
    @staticmethod
    def star_intersection(_star1, star2):
        for star1 in _star1:
            for star2 in _star2:
                if not star1.isdisjoint(star2):
                    return True
        return False
    
    @staticmethod
    def segmentation(_img, _hyper):
        # Choosing a cover of the image by a minimal set of stars 
        E = []
        for i in range(_hyper.hyper.shape[0]):
            E.append([])
            for j in range(_hyper.hyper.shape[1]):
                E[i].append([])
                ng = _hyper.neighboors(i, j)[:, 0]
                ex = set([(i,j)])
                for k in range(len(ng)):
                    if not ex.isdisjoint(_hyper.hyper[ng[k][0], ng[k][1]]):
                        E[i][j].append(_hyper.hyper[ng[k][0], ng[k][1]])
        # Building aggregate areas
        Agg = []
        for i in range(_hyper.hyper.shape[0]):
            Agg.append([])
            for j in range(_hyper.hyper.shape[1]):
                I   = _img.getpixel((i,j))
                Agg([i]).append([]) # Initialization on a new aggregation area
                ng  = _hyper.neighboors(i, j)
                Agg[i][j].append((i, j))
                for k in range(len(ng)):
                    if  HyperTools.star_intersection(E[i][j], E[ng[k, 0][0]][ng[k, 0][1]]):
                        alpha = np.std(ng[:, 1])
                        if _img.getpixel((ng[k, 0][0], ng[k, 0][1])) >= I - alpha and _img.getpixel((ng[k, 0][0], ng[k, 0][1])) <= I + alpha   :
                            Agg[i][j].append((ng[k, 0][0], ng[k, 0][1]))
        # Reducing the number of areas
        #for i in range(_hyper.hyper.shape[0]):
        #    for j in range(_hyper.hyper.shape[1]):
                #g = 


img = Tools.read_image('../images/test.jpg')
img.show()
h = Hypergraph(img)
h.construct()
denoise = HyperTools.denoising(img, h)
denoise.show()