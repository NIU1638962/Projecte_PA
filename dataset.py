# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:39:22 2022

@author: marcs
"""
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, datetime, timedelta
from abc import ABCMeta, abstractmethod
from typing import Tuple, Dict
import numpy as np
import csv
from scipy.sparse import lil_matrix
from data import Data, Pelicula
from usuario import Usuari


# Matriu que guarda de forma efectiva molts zeros, basada en numpy, una vegada
# creada es s'utilitza com numpy.

a = lil_matrix(1000, 1000)


@dataclass
class Dataset(metaclass=ABCMeta):
    _elementos: Tuple[Dict[int, Data]] = field(init=False, default=({}, {}, {}))
    _usuarios: Tuple[Dict[int, Usuari]] = field(init=False, default=({}, {}))
    _valoraciones: lil_matrix = field(init=False, default=None)
    _columnas: int = field(init=False, default=0)
    _filas: int = field(init=False, default=0)

    @property
    def usuarios(self):
        return self._usuarios

    @property
    def valoraciones(self):
        return self._valoraciones

    @property
    def elementos(self):
        return self._elementos
    def score_other_users_also(self, k, usuario):
        valoraciones_usuario=self._valoraciones[usuario,:]
        dict_similitudes={}
        for fila in range(self._filas):
            if fila!=usuario:
                valoraciones_else=(self._valoraciones[fila,:])
                suma=0
                den1=[]
                den2=[]
                for i in range(self._columnas):
                    usu1=valoraciones_usuario[0, i]
                    usu2=valoraciones_else[0,i]
                    if not np.array_equal(usu1,0) and  not np.array_equal(usu2,0) :
                        suma+=(valoraciones_usuario[0, i])*valoraciones_else[0,i]
                        den1.append(valoraciones_usuario[0, i])
                        den2.append(valoraciones_else[0,i])
                den1=[n**2 for n in den1]                
                den2=[n**2 for n in den2]
                den1=(sum(den1))
                den2=sum(den2)
                if den1!=0 or den2!=0:                    
                    similitud=suma/((((den1))**(1/2))*((den2))**(1/2))
                    dict_similitudes[fila]=similitud
        dict_similitudes = sorted(dict_similitudes.items(), key=lambda x: x[1], reverse=True)
        lista_similitudes=dict_similitudes
        usuarios_mas_parecidos=lista_similitudes[:k]
        return usuarios_mas_parecidos
    def other_users_also(self, k, usuario):
       score_dict={}
       usuarios_parecidos=self.score_other_users_also(k, usuario)
       medias=[]
       for columna in range(self._columnas):
           recuento=0
           suma=0
           for fila in usuarios_parecidos:
               if self._valoraciones[fila[0], columna]!=0:
                   recuento+=1
                   suma+=self._valoraciones[fila[0], columna]
           if recuento==0:
               media=0
           else:               
               media=suma/recuento
               medias.append(medias)
       for media, index in zip(medias, range(self._columnas)):       
          titulo=(self._elementos[0][index]._titol)
          score_dict[titulo]=media
       indices=[]
       for i in range(self._columnas):
           print(self._valoraciones[usuario, i])
           if self._valoraciones[usuario, i]==0:
              
              indices.append(i)
       print(indices)
       recomendadas=list(score_dict.items())
       peliculas_recomendadas=[]
       for indice in indices:
           peliculas_recomendadas.append(recomendadas[indice])
       peliculas_recomendadas.sort(key = lambda x: x[1], reverse=True)
       return peliculas_recomendadas
              
              
         
    
           
        
    
    
    def top_popular_items (self, min_votos, usuario):
        score_dict={}
        medias=[]
        votos=[]
        valoraciones=[]
        print(self._columnas)
        size=self._valoraciones.shape
        for columna in range(size[1]):
            recuento=0
            suma=0
            for i in range(size[0]):
                if self._valoraciones[i, columna]!=0:
                    recuento+=1
                    suma+=self._valoraciones[i, columna]
                    
            votos.append(recuento)
            if recuento<min_votos:
                media=0
                medias.append(media)
            else:
                media=suma/recuento
                medias.append(media)
                    
            media_global=(sum(medias))/len(medias)
            
        for recuento, media in zip(votos, medias):
            if media==0:
                 score=0
            else:
                score=(recuento/(recuento+min_votos)*media)+(min_votos/(recuento+min_votos)*media_global)
            valoraciones.append(score)

        for score, index in zip(valoraciones, range(self._columnas)):       
            titulo=(self._elementos[0][index]._titol)
            score_dict[titulo]=score
            print(index)
        # score_dict = sorted(score_dict.items(), key=lambda x: x[1])
        print(len(score_dict))
        valoraciones_usuario=self._valoraciones.getrow(usuario)
        indices=[]
        rec_usuario={}
        indices=[i for i in range(self._columnas + 1) if i not in list(valoraciones_usuario.nonzero()[1])]
        # indices=np.nonzero(valoraciones_usuario == 0) 
        print(len(indices))
        for index in indices:
            titol=list(score_dict.keys())
            titol=titol[index]
            rec_usuario[titol]=score_dict[titol]

        rec_usuario = sorted(rec_usuario.items(), key=lambda x: x[1], reverse=True)
        return rec_usuario
    @abstractmethod
    def read_data(self, directory: str, names_files: List[str]):
        raise NotImplementedError()


NAMES_FILES = ["movies.csv", "ratings.csv"]
DIRECTORY = "ml-latest-small"


@dataclass
class Pelicules(Dataset):
    def read_data(self, directory: str, names_files: List[str]):
        with open(directory + "/" + names_files[0], "r", encoding="utf8") as csv_file:
            csvreader = csv.reader(csv_file)
            fields = next(csvreader)
            for row in csvreader:
                self._elementos[0][self._columnas] = Pelicula(
                    row[1], row[0], self._columnas
                )
                self._elementos[1][row[1]] = self._elementos[0][self._columnas]
                self._elementos[2][row[0]] = self._elementos[0][self._columnas]
                row[2] = row[2].split("|")
                self._elementos[0][self._columnas].caracteristicas = {fields[2]: row[2]}
                self._columnas += 1
        with open(directory + "/" + names_files[1], "r", encoding="utf8") as csv_file:
            csvreader = csv.reader(csv_file)
            fields = next(csvreader)
            zero_array = np.zeros((self._columnas + 1))
            prev_usuari_nom = None
            prev_usuari_fila = None
            prev_elem_colum = None
            prev_elem_iden = None
            for row in csvreader:
                if row[0] not in [usuari.nom for usuari in self._usuarios[0].values()]:
                    self._usuarios[0][self._filas] = Usuari(row[0], self._filas)
                    self._usuarios[1][row[0]] = self._usuarios[0][self._filas]
                    self._filas += 1
                    if self._valoraciones is None:
                        self._valoraciones = zero_array
                    else:
                        self._valoraciones = np.vstack([self._valoraciones, zero_array])
                if len(self._valoraciones.shape) == 1:
                    self._valoraciones[self._elementos[2][row[1]].columna] = float(
                        row[2]
                    )
                else:
                    if prev_usuari_nom == row[0]:
                        fila = prev_usuari_fila
                    else:
                        prev_usuari_nom = row[0]
                        fila = self._usuarios[1][row[0]].fila
                        prev_usuari_fila = fila
                    if prev_elem_iden == row[1]:
                        columna = prev_elem_colum
                    else:
                        prev_elem_iden == row[1]
                        columna = self._elementos[2][row[1]].columna
                        prev_elem_colum = columna
                    self._valoraciones[fila, columna] = float(row[2])
