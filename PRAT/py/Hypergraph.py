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
    def noise_detection(_img, _hyper):
        ISO = []
        IS  = []
        NH  = []
        # Determination of isolated hyperedges of _hyper
        for i in range(_hyper.hyper.shape[0]):
            for j in range(_hyper.hyper.shape[1]):
                ng = set(_hyper.neighboors(i, j)[:, 0])
                ex = ng.intersection(_hyper.hyper[i,j])
                if ex == ng: # ex is an isolated hyperedge
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
            if False:
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
    def segmentation():
        pass
img = Tools.read_image('../images/Iobservee.png')
img.show()
h = Hypergraph(img)
h.construct()
denoise = HyperTools.denoising(img, h)
denoise.show()