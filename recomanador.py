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
from avaluar import Avaluar, Avaluar_Test
from data import Data


logging.basicConfig(
    filename="logging.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s |%(pathname)s |%(funcName)s |%(lineno)d | %(message)s",
)


@dataclass
class Recomanador:
    _n: int
    _theta: int
    _n_recomanacions: int
    _min_vots: int
    _k_usuaris: int
    _pickle: bool = field(init=False, default=None)
    _opcio_mode: int = field(init=False, default=None)
    _opcio_dataset: int = field(init=False, default=None)
    _opcio_recomanacio: int = field(init=False, default=None)
    _avaluar: Avaluar = field(init=False, default=None)
    _usuari: int = field(init=False, default=None)

    def recomanador(self):
        """
        S'encarrega de gestionar les impresions per pantalla i inputs.

        Returns
        -------
        None.

        """
        logging.info("S'ha iniciat el recomanador.")
        try:
            while self._pickle is None:
                logging.info("S'ha iniciat el programa recomanació.")
                con_input = input("Inicialitzar a partir de fitxer binari S/N: ")
                if con_input in "Ss":
                    self._pickle = True
                elif con_input in "Nn":
                    self._pickle = False
                else:
                    print(co.cdred('Opció ha de ser "S" o "N".'))
                    logging.warning('Opció ha de ser "S" o "N".')
            while True:
                try:
                    self._mode()
                except AssertionError as message:
                    print(co.cdred(str(message)[7:]))
                    continue
                else:
                    break
        except:
            logging.error(
                "S'ha terminat el programa recomanació. \n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s",
                self._pickle,
                self._opcio_mode,
                self._opcio_dataset,
                self._opcio_recomanacio,
                self._avaluar,
                self._usuari,
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
        """
        S'encarrga de gestionar la selecció del mode d'execució.

        Returns
        -------
        None.

        """
        while True:
            try:
                self._menu_select_mode()
                self._opcio_mode = input(co.cgray("Selecciona una opció: "))
                logging.debug("Opció recomanació escollida: %s", self._opcio_mode)
                if self._opcio_mode in "Ss":
                    print(co.clblue("Sortint del programa..."))
                    self._pickle = None
                    self._opcio_mode = None
                    logging.debug(
                        "Opcio pickle i opcio cleared i sortint del programa.\n\t%s\n\t%s",
                        self._pickle,
                        self._opcio_mode,
                    )
                    return
                self._opcio_mode = int(self._opcio_mode)
            except ValueError as message:
                print(co.cdred("Opció ha de ser un enter postiu."))
                self._opcio_mode = None
                logging.warning(str(message))
            else:
                if 0 < self._opcio_mode <= 2:
                    self._dataset()
                else:
                    print(co.cdred("Seleccioni opció de mode vàlida."))
                    self._opcio_mode = None
                    logging.warning(
                        "Opció mode cleared, opció no correcta.\n\t%s",
                        self._opcio_mode,
                    )

    def _dataset(self):
        """
        S'encarerga de gestionar la selecció del tipus de dataset.

        Returns
        -------
        None.

        """
        while True:
            self._menu_select_dataset()
            try:
                self._opcio_dataset = input(co.cgray("Selecciona opció: "))
                logging.debug("Opció dataset escollida: %s", self._opcio_dataset)
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
            except ValueError as message:
                self._opcio_dataset = None
                print(co.cdred('Opció ha de ser un enter postiu o "S".'))
                logging.warning(str(message))
            else:
                self._recom()

    def _recom(self):
        """
        S'encarrega de gestionar la selecció del tipus de recomanació.

        Returns
        -------
        None.

        """
        while True:
            self._menu_select_recomanacio()
            try:
                self._opcio_recomanacio = input(co.cgray("Selecciona opció: "))
                if self._opcio_recomanacio in "Ss":
                    print(co.clblue("Sortint del menú..."))
                    self._opcio_dataset = None
                    self._opcio_recomanacio = None
                    self.del_avaluar()
                    logging.debug(
                        "Opció dataset ,opcio recomanacio i avaluar cleared.\n\t%s\n\t%s\n\t%s",
                        self._opcio_dataset,
                        self._opcio_recomanacio,
                        self._avaluar,
                    )
                    return
                self._opcio_recomanacio = int(self._opcio_recomanacio)
                logging.debug(
                    "Opció recomanació escollida: %s", self._opcio_recomanacio
                )
            except ValueError as message:
                self._opcio_recomanacio = None
                print(co.cdred('Opció ha de ser un enter postiu o "S".'))
                logging.warning(str(message))
            else:
                if bool(self._opcio_mode - 1):
                    self._avaluar = Avaluar_Test(
                        self._n, self._theta, self._opcio_recomanacio - 1, self._pickle,
                    )
                else:
                    self._avaluar = Avaluar(
                        self._n, self._theta, self._opcio_recomanacio - 1, self._pickle,
                    )
                self._avaluar.inicia(
                    self._opcio_dataset - 1,
                    self._n_recomanacions,
                    self._min_vots,
                    self._k_usuaris,
                )
                self._usr()

    def _usr(self):
        """
        S'encarrega de la selecció d'usuari.

        Returns
        -------
        None.

        """
        while True:
            self._usuari = input(
                co.cgray(
                    "Selecciona un usuari entre 0-"
                    + str(self._avaluar.recomanacio.dataset.filas - 1)
                    + " : "
                )
            )
            logging.debug("Usuari escollid: %s", self._usuari)
            if self._usuari == "":
                print(co.clblue("Sortint de selecció d'usuari..."))
                self._opcio_recomanacio = None
                self.del_avaluar()
                self._usuari = None
                logging.debug(
                    "Opcio recomanacio, avaluar i usuari cleared, sortint de selecció d'usuari.\n\t%s\n\t%s\n\t%s",
                    self._opcio_recomanacio,
                    self._avaluar,
                    self._usuari,
                )
                return
            try:
                self._usuari = int(self._usuari)
            except ValueError as message:
                print(co.cdred("Usuari ha de ser un enter postiu."))
                logging.warning(str(message))
            else:
                self._avaluar.visualitza(self._avaluar.recomana(self._usuari))

    def _menu_select_mode(self):
        """
        Imprimeix per pantalla el menu de selecció de mode.

        Returns
        -------
        None.

        """
        logging.debug("Menú selecció mode.")
        print("\n")
        print(co.cpurple("MENÚ SELECCIÓ MODE"))
        print(co.cgreen(" (1) Fer recomanació."))
        print(co.cgreen(" (2) Avaluar recomanacions."))
        print(co.cgreen('Sortir del menú: "S".'))

    def _menu_select_dataset(self):
        """
        Imprimeix per pantalla el menú de selecció de dataset.

        Returns
        -------
        None.

        """
        logging.debug("Menú selecció dataset.")
        print("\n")
        print(co.cpurple("MENÚ SELECCIÓ DATA SET"))
        print(co.cgreen(" (1) Películes."))
        print(co.cgreen(" (2) Jocs de taula."))
        print(co.cgreen('Sortir del menú: "S".'))

    def _menu_select_recomanacio(self):
        """
        Imprimeix per pantalla el menú de selecció de tipus de recomanació.

        Returns
        -------
        None.

        """
        logging.debug("Menú selecció recomanació.")
        print("\n")
        print(co.cpurple("MENÚ SELECCIÓ MÉTODE RECOMANACIÓ"))
        print(co.cgreen(" (1) Recomanació simple."))
        print(co.cgreen(" (2) Recomanació col·laborativa."))
        print(co.cgreen(" (3) Recomanació basada en continguts."))
        print(co.cgreen('Sortir del menú: "S".'))

    def del_avaluar(self):
        """
        Elimina totes les referecies als objectes usuaris, data, dataset,
        recomanacions i avaluar de la selecció anterior.

        Returns
        -------
        None.

        """
        logging.info("Iniciant eliminació.")
        if self._avaluar is not None:
            self._avaluar.del_recomanacio()
            del self._avaluar
            self._avaluar = None
        return
