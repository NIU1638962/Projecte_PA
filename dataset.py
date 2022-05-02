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

    def top_popular_items (self, min_votos, usuario):
        score_dict={}
        # print("Elija una opción")
        # print("Opción 1: listado de recomendaciones.")
        # print("Opción 2: añadir valoraciones.")        
        # opcion=input()
        medias=[]
        votos=[]
        valoraciones=[]
        size=self._valoraciones.size()
        print(size)
        for columna in range(size[0]):
            print(1)
            recuento=0
            suma=0
            for i in range(size[1]):
                if self._valoraciones[columna, i]!=0:
                    recuento+=1
                    suma+=self._valoraciones[columna, i]
                    print(2)
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
            for elemento, score in zip(self._elementos, valoraciones):
                score_dict[elemento]=score
            score_dict = sorted(score_dict.items(), key=lambda x: x[1])
            return score_dict
            
        # elif opcion==2:
        #     dict_valoracion={}
        #     repeticion="s"
        #     while repeticion=="s":
        #         pelicula=input("Introduzca el titulo de la película: ")
        #         if pelicula not in self._elementos.keys():
        #             raise AssertionError("Película no disponible")
        #         else:
        #             valoracion_usuario=float(input("Introduzca su valoración: "))
        #             columna=self._elementos.keys().index(pelicula)
        #             dict_valoracion[pelicula]=valoracion_usuario
        #             repeticion=input("¿Quiere valorar otra película?(s/n):")
        #     nuevo_usuario=np.zeros(size[1])  
        #     for columna, valoracion in dict_valoracion.values():
        #         nuevo_usuario[1,columna]=valoracion
        #         score=self.score_top_popular_items(min_votos, columna)
        #         score_dict[pelicula]=score
        #     score_dict = sorted(score_dict.items(), key=lambda x: x[1])

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
