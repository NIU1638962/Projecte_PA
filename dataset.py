# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:34 2022

@author: Joel Tapia Salvador
"""
from dataclasses import dataclass, field
from typing import Dict, Tuple, List
from abc import ABCMeta, abstractmethod
import csv
from scipy.sparse import lil_matrix
from data import Data, Pelicula, Game
from usuario import Usuari
import logging
import sys


# Matriu que guarda de forma efectiva molts zeros, basada en numpy, una vegada
# creada es s'utilitza com numpy.

logging.basicConfig(
    filename="log.txt",
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


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

    def score_top_popular_items(self, min_votos, columna):
        size = self._valoraciones.size()
        recuento = 0
        suma = 0
        for i in range(size[1]):
            if self._valoraciones[columna, i] != 0:
                recuento += 1
                suma += self._valoraciones[columna, i]
        media_global = suma / size[1]
        media = suma / recuento
        score = (recuento / (recuento + min_votos) * media) + (
            min_votos / (recuento + min_votos) * media_global
        )
        return score

    def top_popular_items(self, min_votos, usuario):
        score_dict = {}
        # print("Elija una opción")
        # print("Opción 1: listado de recomendaciones.")
        # print("Opción 2: añadir valoraciones.")
        # opcion=input()
        medias = []
        votos = []
        valoraciones = []
        size = self._valoraciones.shape
        print(size)
        for columna in range(size[0]):
            print(1)
            recuento = 0
            suma = 0
            for i in range(size[1]):
                if self._valoraciones[columna, i] != 0:
                    recuento += 1
                    suma += self._valoraciones[columna, i]
                    print(2)
            votos.append(recuento)
            if recuento < min_votos:
                media = 0
                medias.append(media)
            else:
                media = suma / recuento
                medias.append(media)
            media_global = (sum(medias)) / len(medias)

            for recuento, media in zip(votos, medias):
                if media == 0:
                    score = 0
                else:
                    score = (recuento / (recuento + min_votos) * media) + (
                        min_votos / (recuento + min_votos) * media_global
                    )
                valoraciones.append(score)
            for elemento, score in zip(self._elementos, valoraciones):
                score_dict[elemento] = score
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
    def read_data(self, DIRECTORY: str, NAMES_FILES: List[str]):
        raise NotImplementedError()


@dataclass
class Pelicules(Dataset):
    def read_data(self):
        DIRECTORY = "ml-latest-small"
        NAMES_FILES = ["movies.csv", "ratings.csv"]
        try:
            logging.debug("S'ha iniciant l'execució.")
            row = None
            with open(
                DIRECTORY + "/" + NAMES_FILES[0], "r", encoding="utf8"
            ) as csv_file:
                csvreader = csv.reader(csv_file)
                fields = next(csvreader)
                for row in csvreader:
                    self._elementos[0][self._columnas] = Pelicula(
                        row[1], row[0], self._columnas
                    )
                    repetida = True
                    i = 0
                    while repetida:
                        try:
                            self._elementos[1][row[1]]
                        except KeyError:
                            repetida = False
                            self._elementos[1][row[1]] = self._elementos[0][
                                self._columnas
                            ]
                        else:
                            logging.warning(
                                "Element repetit:\n\tDades execució:\n\t\t%s \n\t\t%s \n\t\t%s",
                                row,
                                self._filas,
                                self._columnas,
                            )
                            if i != 0:
                                row[1] = row[1][:-4]
                            row[1] = row[1] + " (" + str(i + 1) + ")"
                            i += 1
                    self._elementos[2][row[0]] = self._elementos[0][self._columnas]
                    row[2] = row[2].split("|")
                    self._elementos[0][self._columnas].caracteristicas = {
                        fields[2]: row[2]
                    }
                    self._columnas += 1
            logging.debug("S'ha finalitzat la lectura de 'Movies's.")
            with open(
                DIRECTORY + "/" + NAMES_FILES[1], "r", encoding="utf8"
            ) as csv_file:
                csvreader = csv.reader(csv_file)
                fields = next(csvreader)
                prev_usuari_nom = None
                prev_usuari_fila = None
                prev_elem_colum = None
                prev_elem_iden = None
                for row in csvreader:
                    if row[0] not in [
                        usuari.nom for usuari in self._usuarios[0].values()
                    ]:
                        self._usuarios[0][self._filas] = Usuari(row[0], self._filas)
                        self._usuarios[1][row[0]] = self._usuarios[0][self._filas]
                        self._filas += 1
                        if self._valoraciones is None:
                            self._valoraciones = lil_matrix((1, self._columnas))
                        else:
                            self._valoraciones.resize((self._filas + 1, self._columnas))
                    # if len(self._valoraciones.shape) == 1:
                    #     self._valoraciones[self._elementos[2][row[1]].columna] = float(
                    #         row[2]
                    #     )
                    # else:
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
            logging.debug("S'ha finalitzat la lectura de la database.")
        except:
            exc_tuple = sys.exc_info()
            type_error = str(exc_tuple[0]).split()[1][:-1]
            message = str(exc_tuple[1])
            logging.error(
                "S'ha parat l'excució, error:\n\t%s: %s\n Dades execució:\n\t%s \n\t%s \n\t%s",
                type_error,
                message,
                row,
                self._filas,
                self._columnas,
            )


class Board_Games(Dataset):
    def read_data(self):
        DIRECTORY = "archive"
        NAMES_FILES = [
            "games.csv",
            "mechanics.csv",
            "subcategories.csv",
            "user_ratings.csv",
        ]
        try:
            logging.debug("S'ha iniciant l'execució.")
            row = None
            fields_llegir = (3, 4, 8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 28)
            with open(
                DIRECTORY + "/" + NAMES_FILES[0], "r", encoding="utf8"
            ) as csv_file:
                csvreader = csv.reader(csv_file)
                fields_1 = next(csvreader)
                for row in csvreader:
                    self._elementos[0][self._columnas] = Game(
                        row[1], row[0], self._columnas
                    )
                    repetida = True
                    i = 0
                    while repetida:
                        try:
                            self._elementos[1][row[1]]
                        except KeyError:
                            repetida = False
                            self._elementos[1][row[1]] = self._elementos[0][
                                self._columnas
                            ]
                        else:
                            logging.warning(
                                "Element repetit:\n\tDades execució:\n\t\t%s \n\t\t%s \n\t\t%s",
                                row,
                                self._filas,
                                self._columnas,
                            )
                            if i != 0:
                                row[1] = row[1][:-4]
                            row[1] = row[1] + " (" + str(i + 1) + ")"
                            i += 1
                    self._elementos[2][row[0]] = self._elementos[0][self._columnas]
                    for i in fields_llegir:
                        self._elementos[0][self._columnas].caracteristicas[
                            fields_1[i]
                        ] = row[i]
                    for i in range(40, 48, 1):
                        self._elementos[0][self._columnas].caracteristicas[
                            fields_1[i]
                        ] = bool(int(row[i]))
                    self._columnas += 1
            logging.debug("S'ha finalitzat la lectura basica de 'Game's.")
            for j in range(1, 3):
                with open(
                    DIRECTORY + "/" + NAMES_FILES[j], "r", encoding="utf8"
                ) as csv_file:
                    csvreader = csv.reader(csv_file)
                    fields = next(csvreader)
                    for row in csvreader:
                        for i in range(1, len(row), 1):
                            self._elementos[2][row[0]].caracteristicas[
                                fields[i]
                            ] = bool(int(row[i]))
            logging.debug("S'ha finalitzat la lectura de 'Game's.")
            with open(
                DIRECTORY + "/" + NAMES_FILES[3], "r", encoding="utf8"
            ) as csv_file:
                csvreader = csv.reader(csv_file)
                fields = next(csvreader)
                prev_usuari_nom = None
                prev_usuari_fila = None
                prev_elem_colum = None
                prev_elem_iden = None
                for row in csvreader:
                    if row[2] not in [
                        usuari.nom for usuari in self._usuarios[0].values()
                    ]:
                        self._usuarios[0][self._filas] = Usuari(row[2], self._filas)
                        self._usuarios[1][row[2]] = self._usuarios[0][self._filas]
                        self._filas += 1
                        if self._valoraciones is None:
                            self._valoraciones = lil_matrix((1, self._columnas))
                        else:
                            self._valoraciones.resize((self._filas + 1, self._columnas))
                    # if len(self._valoraciones.shape) == 1:
                    #     self._valoraciones[self._elementos[2][row[0]].columna] = float(
                    #         row[1]
                    #     )
                    # else:
                    if prev_usuari_nom == row[2]:
                        fila = prev_usuari_fila
                    else:
                        prev_usuari_nom = row[2]
                        fila = self._usuarios[1][row[2]].fila
                        prev_usuari_fila = fila
                    if prev_elem_iden == row[0]:
                        columna = prev_elem_colum
                    else:
                        prev_elem_iden == row[0]
                        columna = self._elementos[2][row[0]].columna
                        prev_elem_colum = columna
                    self._valoraciones[fila, columna] = float(row[1])
            logging.debug("S'ha finalitzat la lectura de la base de dades.")
        except:
            exc_tuple = sys.exc_info()
            type_error = str(exc_tuple[0]).split()[1][:-1]
            message = str(exc_tuple[1])
            print(type_error + ": " + message)
            logging.error(
                "S'ha parat l'excució, error:\n\t%s: %s\n\tDades execució:\n\t\t%s \n\t\t%s \n\t\t%s",
                type_error,
                message,
                row,
                self._filas,
                self._columnas,
            )
