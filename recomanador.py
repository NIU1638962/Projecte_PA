# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:23:23 2022

@author: Joel Tapia Salvador (1638962)
"""
import sys
import traceback
import logging
from typing import List, Tuple
from películes import Pelicules
from board_games import BoardGames
from data import Data
import console_messages as co
from recomanacions import (
    Recomanacions,
    Recom_top_popular,
    Recom_other_users,
    Recom_you_liked,
)


logging.basicConfig(
    filename="logging.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s |%(pathname)s |%(funcName)s |%(lineno)d | %(message)s",
)

N_RECOMANACIONS = 5
MIN_VOTS = 10
K_USUARIS = 10


def recomanador():
    pickle = True
    opcio_dataset = None
    opcio_recomanacio = None
    recomanacions = None
    usuari = None
    recomanacio = None
    try:
        logging.info("S'ha iniciat el programa recomanació.")
        while True:
            menu_select_dataset()
            try:
                opcio_dataset = input(co.cgray("Selecciona opció: "))
                if opcio_dataset in "Ss":
                    print(co.clblue("Sortint del programa..."))
                    recomanacions = None
                    logging.debug(
                        "Opcio cleared i sortint del programa.\n\t%s", opcio_dataset()
                    )
                    break
                opcio_dataset = int(opcio_dataset)
                logging.debug("Opció dataset escollida: %s", opcio_dataset)
            except ValueError as message:
                print(co.cdred("Opció ha de ser un enter postiu."))
                logging.warning(str(message))
            opcio_recomanacio = None
            usuari = None
            while opcio_recomanacio != 4:
                menu_select_recomanacio()
                try:
                    opcio_recomanacio = int(input(co.cgray("Selecciona una opció: ")))
                except ValueError as message:
                    print(co.cdred("Opció ha de ser un enter postiu."))
                    logging.warning(str(message))
                else:
                    logging.debug("Opció recomanació escollida: %s", opcio_recomanacio)
                    try:
                        if opcio_recomanacio == 1:
                            print(co.clblue("Carregant recomanacions..."))
                            recomanacions = Recom_top_popular(
                                opcio_dataset,
                                N_RECOMANACIONS,
                                MIN_VOTS,
                                K_USUARIS,
                                pickle,
                            )
                            print(co.clblue("Recomanacions carregades."))
                        elif opcio_recomanacio == 2:
                            print(co.clblue("Carregant recomanacions..."))
                            recomanacions = Recom_other_users(
                                opcio_dataset,
                                N_RECOMANACIONS,
                                MIN_VOTS,
                                K_USUARIS,
                                pickle,
                            )
                            print(co.clblue("Recomanacions carregades."))
                        elif opcio_recomanacio == 3:
                            print(co.clblue("Carregant recomanacions..."))
                            recomanacions = Recom_you_liked(
                                opcio_dataset,
                                N_RECOMANACIONS,
                                MIN_VOTS,
                                K_USUARIS,
                                pickle,
                            )
                            print(co.clblue("Recomanacions carregades."))
                        elif opcio_recomanacio == 4:
                            print(co.clblue("Sortint del menú..."))
                            recomanacions = None
                            opcio_recomanacio = None
                            logging.info(
                                "Opció recomanació i recomanacio cleared, opció no correcta.\n\t%s\n\t%s",
                                opcio_recomanacio,
                                recomanacions,
                            )
                        else:
                            print(co.cdred("Error: Seleccioni opció vàlida."))
                            opcio_recomanacio = None
                            recomanacions = None
                            logging.warning(
                                "Opció recomanació i recomanacio cleared, opció no correcta.\n\t%s\n\t%s",
                                opcio_recomanacio,
                                recomanacions,
                            )
                    except AssertionError as message:
                        print(co.cdred(str(message)))
                        logging.warning(str(message))
                    except NotImplementedError as message:
                        print(co.cdred(str(message)))
                        logging.warning(str(message))
                    else:
                        while usuari != "":
                            usuari = input(
                                co.cgray(
                                    "Selecciona un usuari entre 0-"
                                    + str(recomanacions.dataset.filas - 1)
                                    + " : "
                                )
                            )
                            logging.debug("Usuari escollid: %s", usuari)
                            if usuari == "":
                                print(co.clblue("Sortint de selecció d'usuari..."))
                                recomanacio = None
                                usuari = None
                                logging.debug(
                                    "Usuari i  recomanacio cleared, sortint del programa.\n\t%s\n\t%s",
                                    usuari,
                                    recomanacio,
                                )
                                break
                            try:
                                usuari = int(usuari)
                            except ValueError as message:
                                print(co.cdred("Usuari ha de ser un enter postiu."))
                                logging.warning(str(message))
                            else:
                                recomanacio = recomanacions.recomana(usuari)
                                logging.debug("Recomanacions: %s", recomanacio)
                                visualitza_rec(recomanacio)
                                recomanacio = None
    except:
        logging.error(
            "S'ha terminat el programa recomanació. \n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s",
            pickle,
            opcio_dataset,
            opcio_recomanacio,
            recomanacions,
            usuari,
            recomanacio,
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


def visualitza_rec(recomanacio: List[Tuple[Data, int]]):
    if recomanacio == []:
        logging.warn("Recomanació está buit.")
        print(co.cpurple("No hi ha recomanacions."))
    elif recomanacio is not None:
        logging.info("Iniciant visualització de les recomanacions.")
        logging.debug("\n\t%s", recomanacio)
        for i, elem in enumerate(recomanacio):
            print(co.cpurple("Recomanació " + str(i + 1)))
            elem[0].visualitza()
            print("\t" + co.cgreen("Score") + ": " + str(elem[1]))
        logging.info("Visualització finalitzada.")


def menu_select_dataset():
    logging.debug("Menú selecció dataset.")
    print("\n")
    print(co.cpurple("MENÚ SELECCIÓ DATA SET"))
    print(co.cgreen(" (1) Películes."))
    print(co.cgreen(" (2) Jocs de taula."))
    print(co.cgreen(" (3) Sortir del programa."))


def menu_select_recomanacio():
    logging.debug("Menú selecció recomanació.")
    print("\n")
    print(co.cpurple("MENÚ SELECCIÓ MÉTODE RECOMANACIÓ"))
    print(co.cgreen(" (1) Recomanació simple."))
    print(co.cgreen(" (2) Recomanació col·laborativa."))
    print(co.cgreen(" (3) Recomanació basada en continguts."))
    print(co.cgreen(" (4) Sortir del menú."))


# recomanador()
