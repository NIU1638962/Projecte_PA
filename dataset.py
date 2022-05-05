# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:34 2022

@author: Joel Tapia Salvador
"""
from dataclasses import dataclass, field
from typing import Dict, Tuple, ClassVar
from abc import ABCMeta, abstractmethod
import csv
from scipy.sparse import lil_matrix
from data import Data, Pelicula, Game
from usuario import Usuari
import logging
import sys
import pickle
import os

logging.basicConfig(
    filename="log.txt",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


@dataclass
class Dataset(metaclass=ABCMeta):
    _directory: str
    _names_files: Tuple[str]
    _elementos: Tuple[Dict[int, Data]] = field(init=False, default=({}, {}, {}))
    _usuarios: Tuple[Dict[int, Usuari]] = field(init=False, default=({}, {}))
    _valoraciones: lil_matrix = field(init=False, default=None)
    _columnas: int = field(init=False, default=0)
    _filas: int = field(init=False, default=0)
    _scores_top_popular_items: lil_matrix[int] = field(init=False, default=None)
    _min_vots: int = field(ini=False, default=None)
    _names_files_pickle: ClassVar[Tuple[str]] = (
        "valoraciones.dat",
        "elementos(0).dat",
        "elementos(1).dat",
        "elementos(2).dat",
        "usuarios(0).dat",
        "usuarios(1).dat",
        "filas.dat",
        "columnas.dat",
    )

    def __post_init__(self):
        self._names_files_pickle = tuple(
            [self._directory + "_pickle" + "/" + i for i in self._names_files_pickle]
        )

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

    def top_popular_items(self, min_vots, usuario):
        # score_dict = {}
        if self._scores_top_popular_items is None or self._min_vots == min_vots:
            self._min_vots = min_vots
            avg_item = lil_matrix((1, self._columnas))
            num_vots = lil_matrix((1, self._columnas), dtype=int)
            score = lil_matrix((1, self._columnas))
            for columna in range(self._columnas):
                num_vots[0, columna] = self._valoraciones[:, columna].count_nonzero()
                if num_vots[0, columna] >= min_vots:
                    avg_item[0, columna] = (self._valoraciones[:, columna].sum()) / (
                        num_vots[0, columna]
                    )
                avg_global = avg_item.mean()
            for columna in range(self._columnas):
                if num_vots[0, columna] >= min_vots:
                    score[0, columna] = (
                        ((num_vots[0, columna]) / (num_vots[0, columna] + min_vots))
                        * avg_item[0, columna]
                    ) + (((min_vots) / (num_vots[0, columna] + min_vots)) * avg_global)
                else:
                    score[0, columna] = 0
            self._scores_top_popular_items = score
        # for score, index in zip(valoraciones, range(self._columnas - 1)):
        #     titulo = self._elementos[0][index]._titol
        #     score_dict[titulo] = score
        # # score_dict = sorted(score_dict.items(), key=lambda x: x[1])
        # valoraciones_usuario = self._valoraciones.getrow(usuario)
        # indices = []
        # rec_usuario = {}
        # indices = valoraciones_usuario.nonzero()
        # print(len(indices[1]))
        # for index in indices[1]:
        #     titol = list(score_dict.keys())
        #     titol = titol[index]
        #     rec_usuario[titol] = score_dict[titol]
        # rec_usuario = sorted(rec_usuario.items(), key=lambda x: x[1], reverse=True)
        # print(len(rec_usuario))
        return rec_usuario

    @abstractmethod
    def read_data(self):
        raise NotImplementedError()

    def _save_pickle(self):
        os.mkdir("./" + self._directory + "_pickle")
        with open(self._names_files_pickle[0], "wb") as fitxer_1, open(
            self._names_files_pickle[1], "wb"
        ) as fitxer_2, open(self._names_files_pickle[2], "wb") as fitxer_3, open(
            self._names_files_pickle[3], "wb"
        ) as fitxer_4, open(
            self._names_files_pickle[4], "wb"
        ) as fitxer_5, open(
            self._names_files_pickle[5], "wb"
        ) as fitxer_6, open(
            self._names_files_pickle[6], "wb"
        ) as fitxer_7, open(
            self._names_files_pickle[7], "wb"
        ) as fitxer_8:
            pickle.dump(self._valoraciones, fitxer_1)
            pickle.dump(self._elementos[0], fitxer_2)
            pickle.dump(self._elementos[1], fitxer_3)
            pickle.dump(self._elementos[2], fitxer_4)
            pickle.dump(self._usuarios[0], fitxer_5)
            pickle.dump(self._usuarios[1], fitxer_6)
            pickle.dump(self._filas, fitxer_7)
            pickle.dump(self._columnas, fitxer_8)

    def _load_pickle(self):
        with open(self._names_files_pickle[0], "rb") as fitxer_1, open(
            self._names_files_pickle[1], "rb"
        ) as fitxer_2, open(self._names_files_pickle[2], "rb") as fitxer_3, open(
            self._names_files_pickle[3], "rb"
        ) as fitxer_4, open(
            self._names_files_pickle[4], "rb"
        ) as fitxer_5, open(
            self._names_files_pickle[5], "rb"
        ) as fitxer_6, open(
            self._names_files_pickle[6], "rb"
        ) as fitxer_7, open(
            self._names_files_pickle[7], "rb"
        ) as fitxer_8:
            self._valoraciones = pickle.load(fitxer_1)
            self._elementos = (
                pickle.load(fitxer_2),
                pickle.load(fitxer_3),
                pickle.load(fitxer_4),
            )
            self._usuarios = (pickle.load(fitxer_5), pickle.load(fitxer_6))
            self._filas = pickle.load(fitxer_7)
            self._columnas = pickle.load(fitxer_8)


@dataclass
class Pelicules(Dataset):
    def read_data(self):
        try:
            if self._directory + "_pickle" in os.listdir("."):
                logging.debug(
                    "S'ha iniciat la lectura de la base de dades de películes a través de guardat binari."
                )
                self._load_pickle()
                logging.debug(
                    "S'ha finalitzat la lectura de la base de dades a través de guardat binari."
                )
            else:
                logging.debug(
                    "S'ha iniciat la lectura de la base de dades de películes a través de csv."
                )
                row = None
                # Obrim arxiu amb les dades de les pelicules.
                with open(
                    self._directory + "/" + self._names_files[0], "r", encoding="utf8"
                ) as csv_file:
                    csvreader = csv.reader(csv_file)
                    # Llegim la capçelera del arxiu csv.
                    fields = next(csvreader)
                    # Recorrem la resta de les lineas del arxiu.
                    for row in csvreader:
                        # Crea l'objecte película en cuestió de la línea i el
                        # guarda al diccionari indexat per la posició en la coluna
                        # de la matriu de self._valoraciones.
                        self._elementos[0][self._columnas] = Pelicula(
                            row[1], row[0], self._columnas
                        )
                        # Cada película té una posició única en la matriu i un
                        # identificador únic, peró poden haver-hi películes amb
                        # títols repetits, per no sobre escriure al diccionari
                        # indexat pels títols de películes.
                        repetida = True
                        i = 0
                        while repetida:
                            # Comprovem si ja existeix un elements indexat per
                            # aquest títol.
                            try:
                                self._elementos[1][row[1]]
                            # Si no ho está, afegim l'index i la referencia a
                            # l'objecte película.
                            except KeyError:
                                repetida = False
                                self._elementos[1][row[1]] = self._elementos[0][
                                    self._columnas
                                ]
                            # Si ja existeix un element amb aquest index.
                            else:
                                logging.warning(
                                    "Element repetit:\n\tDades execució:\n\t\t%s \n\t\t%s \n\t\t%s",
                                    row,
                                    self._filas,
                                    self._columnas,
                                )
                                # L'hi canviem el titulo afegint " (1)", o "(2)",
                                # etc., depenent de quantes vegades está repetit el
                                # títol i per tant de quantes vegades s'hagi
                                # repetit aquest bucle.
                                if i != 0:
                                    row[1] = row[1][:-4]
                                row[1] = row[1] + " (" + str(i + 1) + ")"
                                self._elementos[0][self._columnas].titol = row[1]
                                i += 1
                        # Afegim la referéncia al diccionari indexat per la id de
                        # la película.
                        self._elementos[2][row[0]] = self._elementos[0][self._columnas]
                        # Afegim al diccionarí de categories una llista de la
                        # característica corresponent.
                        row[2] = row[2].split("|")
                        self._elementos[0][self._columnas].caracteristicas = {
                            fields[2]: row[2]
                        }
                        self._columnas += 1
                logging.debug("S'ha finalitzat la lectura de 'Movies's.")
                # Obrim l'arxiu amb les valoracions dels usuaris.
                with open(
                    self._directory + "/" + self._names_files[1], "r", encoding="utf8"
                ) as csv_file:
                    csvreader = csv.reader(csv_file)
                    # Llegim la capçelera del arxiu csv.
                    fields = next(csvreader)
                    # Per agilitar el proces i no tenir que fer tantes crides a
                    # dins dels diccionaris i objectes "Pelicula()" i "Usuari()",
                    # tindrem unes variables internes que guarden el nom i fila del
                    # anterior usuari del qual s'ha llegit la valoració. I que
                    # també guarden el nom i fila de la anterior pelicula del qual
                    # s'ha llegit la valoració. Favoreix la lectura més rapída de
                    # fitxers on les valoracions están ordenades per películes o
                    # usuaris.
                    prev_usuari_nom = None
                    prev_usuari_fila = None
                    prev_elem_colum = None
                    prev_elem_iden = None
                    # Recorrem la resta de les lineas del arxiu.
                    for row in csvreader:
                        if row[0] not in [
                            usuari.nom for usuari in self._usuarios[0].values()
                        ]:
                            self._usuarios[0][self._filas] = Usuari(row[0], self._filas)
                            self._usuarios[1][row[0]] = self._usuarios[0][self._filas]
                            if self._valoraciones is None:
                                self._valoraciones = lil_matrix((1, self._columnas))
                            else:
                                self._valoraciones.resize(
                                    (self._filas + 1, self._columnas)
                                )
                            self._filas += 1
                        if prev_usuari_nom == row[0]:
                            fila = prev_usuari_fila
                        else:
                            prev_usuari_nom = row[0]
                            fila = self._usuarios[1][row[0]].fila
                            prev_usuari_fila = fila
                        if prev_elem_iden == row[1]:
                            columna = prev_elem_colum
                        else:
                            prev_elem_iden = row[1]
                            columna = self._elementos[2][row[1]].columna
                            prev_elem_colum = columna
                        self._valoraciones[fila, columna] = float(row[2])
                logging.debug(
                    "S'ha finalitzat la lectura de la base de dades a través de csv."
                )
                logging.debug("S'ha iniciat el guardat binari de l'objecte.")
                self._save_pickle()
                logging.debug("S'ha finalitzat el guardat binari del objecte.")
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
            raise exc_tuple[0](message) from exc_tuple[1]


class Board_Games(Dataset):
    def read_data(self):
        try:
            if self._directory + "_pickle" in os.listdir("."):
                logging.debug(
                    "S'ha iniciat la lectura de la base de dades de jocs a través de guardat binari."
                )
                self._load_pickle()
                logging.debug(
                    "S'ha finalitzat la lectura de la base de dades a través de guardat binari."
                )
            else:
                logging.debug(
                    "S'ha iniciat la lectura de la base de dades de jocs a través de csv."
                )
                row = None
                fields_llegir = (3, 4, 8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 28)
                with open(
                    self._directory + "/" + self._names_files[0], "r", encoding="utf8"
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
                                self._elementos[0][self._columnas].titol = row[1]
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
                        self._directory + "/" + self._names_files[j],
                        "r",
                        encoding="utf8",
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
                    self._directory + "/" + self._names_files[3], "r", encoding="utf8"
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
                                self._valoraciones.resize(
                                    (self._filas + 1, self._columnas)
                                )
                        if prev_usuari_nom == row[2]:
                            fila = prev_usuari_fila
                        else:
                            prev_usuari_nom = row[2]
                            fila = self._usuarios[1][row[2]].fila
                            prev_usuari_fila = fila
                        if prev_elem_iden == row[0]:
                            columna = prev_elem_colum
                        else:
                            prev_elem_iden = row[0]
                            columna = self._elementos[2][row[0]].columna
                            prev_elem_colum = columna
                        self._valoraciones[fila, columna] = float(row[1])
                logging.debug(
                    "S'ha finalitzat la lectura de la base de dades a través de csv."
                )
                logging.debug("S'ha iniciat el guardat binari de l'objecte.")
                self._save_pickle()
                logging.debug("S'ha finalitzat el guardat binari del objecte.")
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
            raise exc_tuple[0](message) from exc_tuple[1]
