# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:23:23 2022

@author: Joel Tapia Salvador (1638962)
"""
import sys
import traceback
import logging
from dataclasses import dataclass, field
from typing import List, Tuple
import console_messages as co
from recomanacions import (
    Recomanacions,
    Recom_top_popular,
    Recom_other_users,
    Recom_you_liked,
)
from data import Data


logging.basicConfig(
    filename="logging.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s |%(pathname)s |%(funcName)s |%(lineno)d | %(message)s",
)


@dataclass
class Recomanador:
    _n_recomanacions: int
    _min_vots: int
    _k_usuaris: int
    _pickle: bool = field(init=False, default=None)
    _opcio_mode: int = field(init=False, default=None)
    _opcio_dataset: int = field(init=False, default=None)
    _opcio_recomanacio: int = field(init=False, default=None)
    _recomanacions: Recomanacions = field(init=False, default=None)
    _usuari: int = field(init=False, default=None)
    _recomanacio: List[Tuple[Data, float]] = field(init=False, default=None)

    def recomanador(self):
        try:
            while self._pickle is None:
                logging.info("S'ha iniciat el programa recomanació.")
                con_input = input("Inicialitzar a partir de fitxer binari S/N: ")
                if con_input in "Ss":
                    self._pickle = True
                elif con_input in "Nn":
                    self._pickle = False
                else:
                    print(co.cdred('Opció ha de ser "S" o "N" postiu.'))
                    logging.warning('Opció ha de ser "S" o "N" postiu.')
            self._mode()
        except:
            logging.error(
                "S'ha terminat el programa recomanació. \n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s",
                self._pickle,
                self._opcio_mode,
                self._opcio_dataset,
                self._opcio_recomanacio,
                self._recomanacions,
                self._usuari,
                self._recomanacio,
            )
            exc_tuple = sys.exc_info()
            type_error = str(exc_tuple[0]).split()[1][:-1]
            message = str(exc_tuple[1])
            print(
                co.cdred("An error has occured.")
                + "\n\t"
                + co.eul("Error Type:")
                + " \n\t\t"
                + type_error
                + "\n\t"
                + co.eul("Error message:")
                + " \n\t\t"
                + message
            )
            traceback.print_exc()
        else:
            logging.info("S'ha finalitzat correctament el programa recomanació.")

    def _mode(self):
        while True:
            try:
                self._menu_select_mode()
                self._opcio_mode = int(input(co.cgray("Selecciona una opció: ")))
            except ValueError as message:
                print(co.cdred("Opció ha de ser un enter postiu."))
                self._opcio_mode = None
                logging.warning(str(message))
            else:
                logging.debug("Opció recomanació escollida: %s", self._opcio_mode)
                if self._opcio_mode == 1:
                    self._dataset()
                elif self._opcio_mode == 2:
                    pass
                elif self._opcio_mode == 3:
                    print(co.clblue("Sortint del programa..."))
                    self._pickle = None
                    self._opcio_mode = None
                    logging.debug(
                        "Opcio pickle i opcio cleared i sortint del programa.\n\t%s\n\t%s",
                        self._pickle,
                        self._opcio_mode,
                    )
                    return
                else:
                    print(co.cdred("Error: Seleccioni opció vàlida."))
                    self._opcio_mode = None
                    logging.warning(
                        "Opció mode cleared, opció no correcta.\n\t%s",
                        self._opcio_mode,
                    )

    def _dataset(self):
        while True:
            self._menu_select_dataset()
            try:
                self._opcio_dataset = input(co.cgray("Selecciona opció: "))
                if self._opcio_dataset in "Ss":
                    print(co.clblue("Sortint del menú..."))
                    self._opcio_mode = None
                    self._opcio_dataset = None
                    logging.debug(
                        "Opció mode i opcio dataset cleared.\n\t%s\n\t%s",
                        self._opcio_mode,
                        self._opcio_dataset,
                    )
                    return
                self._opcio_dataset = int(self._opcio_dataset)
                logging.debug("Opció dataset escollida: %s", self._opcio_dataset)
            except ValueError as message:
                self._opcio_dataset = None
                print(co.cdred('Opció ha de ser un enter postiu o "S".'))
                logging.warning(str(message))
            else:
                self._recom()

    def _recom(self):
        while True:
            self._menu_select_recomanacio()
            try:
                self._opcio_recomanacio = int(input(co.cgray("Selecciona una opció: ")))
            except ValueError as message:
                print(co.cdred("Opció ha de ser un enter postiu."))
                logging.warning(str(message))
            else:
                logging.debug(
                    "Opció recomanació escollida: %s", self._opcio_recomanacio,
                )
                try:
                    if self._opcio_recomanacio == 1:
                        print(co.clblue("Carregant recomanacions..."))
                        self._recomanacions = Recom_top_popular(
                            self._opcio_dataset - 1,
                            self._n_recomanacions,
                            self._min_vots,
                            self._k_usuaris,
                            self._pickle,
                        )
                        print(co.clblue("Recomanacions carregades."))
                    elif self._opcio_recomanacio == 2:
                        print(co.clblue("Carregant recomanacions..."))
                        self._recomanacions = Recom_other_users(
                            self._opcio_dataset - 1,
                            self._n_recomanacions,
                            self._min_vots,
                            self._k_usuaris,
                            self._pickle,
                        )
                        print(co.clblue("Recomanacions carregades."))
                    elif self._opcio_recomanacio == 3:
                        print(co.clblue("Carregant recomanacions..."))
                        self._recomanacions = Recom_you_liked(
                            self._opcio_dataset - 1,
                            self._n_recomanacions,
                            self._min_vots,
                            self._k_usuaris,
                            self._pickle,
                        )
                        print(co.clblue("Recomanacions carregades."))
                    elif self._opcio_recomanacio == 4:
                        print(co.clblue("Sortint del menú..."))
                        self._opcio_dataset = None
                        self._opcio_recomanacio = None
                        self._recomanacions = None
                        logging.debug(
                            "Opció dataset, opcio recomanació i recomanacio cleared, sortint del menú.\n\t%s\n\t%s\n\t%s",
                            self._opcio_dataset,
                            self._opcio_recomanacio,
                            self._recomanacions,
                        )
                        return
                    else:
                        print(co.cdred("Error: Seleccioni opció vàlida."))
                        self._opcio_recomanacio = None
                        self._recomanacions = None
                        logging.warning(
                            "Opció recomanació i recomanacio cleared, opció no correcta.\n\t%s\n\t%s",
                            self._opcio_recomanacio,
                            self._recomanacions,
                        )
                except AssertionError as message:
                    print(co.cdred(str(message)))
                    logging.warning(str(message))
                except NotImplementedError as message:
                    print(co.cdred(str(message)))
                    logging.warning(str(message))
                else:
                    self._usr()

    def _usr(self):
        while True:
            self._usuari = input(
                co.cgray(
                    "Selecciona un usuari entre 0-"
                    + str(self._recomanacions.dataset.filas - 1)
                    + " : "
                )
            )
            logging.debug("Usuari escollid: %s", self._usuari)
            if self._usuari == "":
                print(co.clblue("Sortint de selecció d'usuari..."))
                self._opcio_recomanacio = None
                self._recomanacio = None
                self._usuari = None
                logging.debug(
                    "Opcio recoamanacio, recomanacio i usuari cleared, sortint de selecció d'usuari.\n\t%s\n\t%s\n\t%s",
                    self._opcio_recomanacio,
                    self._recomanacio,
                    self._usuari,
                )
                return
            try:
                self._usuari = int(self._usuari)
            except ValueError as message:
                print(co.cdred("Usuari ha de ser un enter postiu."))
                logging.warning(str(message))
            else:
                self._recomanacio = self._recomanacions.recomana(self._usuari)
                logging.debug(
                    "Recomanacions: %s", self._recomanacio,
                )
                self._visualitza_rec()
                self._recomanacio = None

    def _visualitza_rec(self):
        if self._recomanacio == []:
            logging.warn("Recomanació está buit.")
            print(co.cpurple("No hi ha recomanacions."))
        elif self._recomanacio is not None:
            logging.info("Iniciant visualització de les recomanacions.")
            logging.debug("\n\t%s", self._recomanacio)
            for i, elem in enumerate(self._recomanacio):
                print(co.cpurple("Recomanació " + str(i + 1)))
                elem[0].visualitza()
                print("\t" + co.cgreen("Score") + ": " + str(elem[1]))
            logging.info("Visualització finalitzada.")

    def _menu_select_mode(self):
        logging.debug("Menú selecció mode.")
        print("\n")
        print(co.cpurple("MENÚ SELECCIÓ MODE"))
        print(co.cgreen(" (1) Fer recomanació."))
        print(co.cgreen(" (2) Avaluar recomanacions."))
        print(co.cgreen(" (3) Sortir del programa."))

    def _menu_select_dataset(self):
        logging.debug("Menú selecció dataset.")
        print("\n")
        print(co.cpurple("MENÚ SELECCIÓ DATA SET"))
        print(co.cgreen(" (1) Películes."))
        print(co.cgreen(" (2) Jocs de taula."))
        print(co.cgreen('Sortir del menú: "S".'))

    def _menu_select_recomanacio(self):
        logging.debug("Menú selecció recomanació.")
        print("\n")
        print(co.cpurple("MENÚ SELECCIÓ MÉTODE RECOMANACIÓ"))
        print(co.cgreen(" (1) Recomanació simple."))
        print(co.cgreen(" (2) Recomanació col·laborativa."))
        print(co.cgreen(" (3) Recomanació basada en continguts."))
        print(co.cgreen(" (4) Sortir del menú."))
