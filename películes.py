# -*- coding: utf-8 -*-
"""
Created on Sat May  7 21:40:59 2022

@author: Joel Tapia Salvador (1638962) i Aksel Serret Llopis ()
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
        """
        Llegeix el dataset corresponent amb les valoracion corresponents,
        a partir del directori i arxius donats en la creació de la clase.

        Raises
        ------
        exc_tuple
            Qualsevol error generatdurant la lectura es guardat en el arxiu log
            i re-raised per parar la execució.

        Returns
        -------
        None.

        """
        try:
            # Comprovació de si existeixenel arxius binaris del dataset.
            if (
                self._directory + "_pickle" in os.listdir(".")
                and self._pickle
                and [
                    i.split("/")[1] in os.listdir("./" + self._directory + "_pickle")
                    for i in self._names_files_pickle
                ].count(True)
                == len(self._names_files_pickle)
            ):
                logging.debug(
                    "S'ha iniciat la lectura de la base de dades de películes a través de guardat binari."
                )
                # S'hi existeixen els carrega als atributs i finalitza la
                # lectura.
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
                                # etc., depenent de quantes vegades está
                                # repetit el títol i per tant de quantes
                                # vegades s'hagi repetit aquest bucle.
                                if i != 0:
                                    row[1] = row[1][:-4]
                                row[1] = row[1] + " (" + str(i + 1) + ")"
                                self._elementos[0][self._columnas].titol = row[1]
                                i += 1
                        # Afegim la referéncia al diccionari indexat per la id
                        # de la película.
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
                    # tindrem unes variables internes que guarden el nom i fila
                    # del anterior usuari del qual s'ha llegit la valoració. I
                    # que també guarden el nom i fila de la anterior pelicula
                    # del qual s'ha llegit la valoració. Favoreix la lectura
                    # més rapída de fitxers on les valoracions están ordenades
                    # per películes o usuaris.
                    prev_usuari_nom = None
                    prev_usuari_fila = None
                    prev_elem_colum = None
                    prev_elem_iden = None
                    # Recorrem la resta de les lineas del arxiu.
                    for row in csvreader:
                        if row[0] not in [
                            usuari.nom for usuari in self._usuarios[0].values()
                        ]:
                            logging.debug("Not in.")
                            # Si l'usuari o ha fet una valoració préviament es
                            # crea un objecte Usuari, i s'indexa per a la fila
                            # que ocuparà en la matriu de  valoracions a aquest
                            # usuari internament per aquesta fila es considera.
                            self._usuarios[0][self._filas] = Usuari(row[0], self._filas)
                            # També s'indexa al usuari pel seu nom d'usuari.
                            self._usuarios[1][row[0]] = self._usuarios[0][self._filas]
                            if self._valoraciones is None:
                                logging.debug("Valoracions is None.")
                                # Sí es el primer usuari en ser afegit es
                                # crea una lil_matrix amb la quantitat de
                                # columnes igual al nombre d'elements que s'han
                                # enmagatzemat previament.
                                self._valoraciones = lil_matrix((1, self._columnas))
                            else:
                                logging.debug("Valoracions is not None.")
                                # Si no s'afegeix la valoració a una nova fila
                                # de la matriu de valoracions.
                                self._valoraciones.resize(
                                    (self._filas + 1, self._columnas)
                                )
                            # S'incrementa el contador del nombre de files o
                            # usuaris que hi ha.
                            self._filas += 1
                        # Per agilitar el procesament es guarda  internament
                        # l'usuari valorat anteriorment i la película valorada
                        # anteriorment per agilitar la modificació en la matriu
                        # Afavoreix a els datasets ordenats pels elements o
                        # usuaris.
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
                        # Es modifica la poosició de la matriu amb la valoració
                        # llegida, les puntuacones son floats.
                        self._valoraciones[fila, columna] = float(row[2])
                logging.debug(
                    "S'ha finalitzat la lectura de la base de dades a través de csv."
                )
                if self._pickle:
                    # Una vegada llegit el dataset completament a través dels
                    # arxius csv, es guarden el atributs en arxius binaris per
                    # aumentar la velocitat de lectura la proxima vegada que es
                    # carregui el dataset.
                    logging.debug("S'ha iniciat el guardat binari de l'objecte.")
                    self._save_pickle()
                    logging.debug("S'ha finalitzat el guardat binari del objecte.")
        except:
            # Recupera el tipus d'error, el guarda en l'arxiu de logging i
            # aixeca el error per para l'execució e infromar al programa
            # principal.
            exc_tuple = sys.exc_info()
            type_error = str(exc_tuple[0]).split()[1][:-1]
            message = str(exc_tuple[1])
            logging.error(
                "S'ha parat l'excució, error:\n\t%s: %s\n Dades execució:\n\tRow: %s \n\tFilas: %s \n\tColumnas: %s",
                type_error,
                message,
                row,
                self._filas,
                self._columnas,
            )
            raise exc_tuple[0](message) from exc_tuple[1]
