# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:39:22 2022

@author: marcs
"""
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, datetime, timedelta
from abc import ABCMeta, abstractmethod
import numpy as np
@dataclass
class Dataset:
    def __init__(self):
        self._usuarios=0
        self._valoraciones=[]
        self._elementos={}
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
        media_global=suma/size[1]
        media=suma/recuento
        score=(recuento/(recuento+min_votos)*media)+(min_votos/(recuento+min_votos)*media_global)
        return score
    
    
    def top_popular_items (self, min_votos):
        score_dict={}
        repeticion="s"
        print("Elija una opción")
        print("Opción 1: listado de recomendaciones.")
        print("Opción 2: añadir valoraciones.")        
        opcion=input()
        if opcion==1:
            for elemento in self._elementos:
                size=self._valoraciones.size()
                for columna in range(size[0]):
                    score=self.score_top_popular_items(min_votos, columna)                
                    score_dict[elemento]=score
            score_dict = sorted(score_dict.items(), key=lambda x: x[1])
            return score_dict
        elif opcion==2:
            dict_valoracion={}
            repeticion="s"
            while repeticion=="s":
                pelicula=input("Introduzca el titulo de la película: ")
                if pelicula not in self._elementos.keys():
                    raise AssertionError("Película no disponible")
                else:
                    valoracion_usuario=float(input("Introduzca su valoración: "))
                    columna=self._elementos.keys().index(pelicula)
                    dict_valoracion[pelicula]=valoracion_usuario
                    repeticion=input("¿Quiere valorar otra película?(s/n):")
            nuevo_usuario=np.zeros(size[1])  
            for columna, valoracion in dict_valoracion.values():
                nuevo_usuario[1,columna]=valoracion
                score=self.score_top_popular_items(min_votos, columna)
                score_dict[pelicula]=score
            score_dict = sorted(score_dict.items(), key=lambda x: x[1])
            return score_dict
        
