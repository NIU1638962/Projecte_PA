# -*- coding: utf-8 -*-
"""
Created on Sat May  7 21:40:59 2022

@author: Joel Tapia Salvador
"""
import sys
import os
import logging
import csv
from dataclasses import dataclass
from scipy.sparse import lil_matrix
from dataset import Dataset
from data import Pelicula
from usuario import Usuari


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
                        # guarda al diccionari indexat per la posició en la
                        # colmuna de la matriu de self._valoraciones.
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
                            # Si ja existeix un element amb aquest índex.
                            else:
                                logging.warning(
                                    "Element repetit:\n\tDades execució:\n\t\t%s \n\t\t%s \n\t\t%s",
                                    row,
                                    self._filas,
                                    self._columnas,
                                )
                                # L'hi canviem el títul afegint " (1)", o "(2)",
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
