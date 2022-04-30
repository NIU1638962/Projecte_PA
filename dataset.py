# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:34 2022

@author: Joel Tapia Salvador
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:39:22 2022

@author: marcs
"""
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, datetime, timedelta
from abc import ABCMeta, abstractmethod

@dataclass
class Dataset:
    def __init__(self):
        self._usuarios=0
        self._valoraciones=[]
        self._elementos=[]
    @property
    def usuarios(self):
        return self._usuarios
    @property
    def valoraciones(self):
        return self._valoraciones
    @property
    def elementos(self):
        return self._elementos
    def score_top_popular_items(self, min_votos, columna):
        size=self._valoraciones.size()
        recuento=0
        suma=0
        for i in range(size[1]):
                if self._valoraciones[columna, i]!=0:
                    recuento+=1
                    suma+=self._valoraciones[columna, i]
        media=suma/recuento
        score=(recuento/(recuento+min_votos))
        return score
    
    def menu(self):
        print("Elija una opción")
        print("Opción 1: listado de valoraciones.")
        print("Opción 2: añadir valoración.")
    
    def top_popular_items (self, min_votos):
        score_dict={}
        opcion=input()
        if opcion==1:
            for elemento in self._elementos:
                size=self._valoraciones.size()
                for columna in range(size[0]):
                    score=self.score_top_popular_items(min_votos, columna)                
                    score_dict[elemento]=score
        elif opcion==2:
            pelicula=input()
