# -*- coding: utf-8 -*-
"""
Created on Sat May  7 21:42:32 2022

@author: Joel Tapia Slavdor
"""
import sys
import os
import logging
import csv
from dataclasses import dataclass
from scipy.sparse import lil_matrix
from dataset import Dataset
from data import Game
from usuario import Usuari


@dataclass
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
                                ] = list(bool(int(row[i])))
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
