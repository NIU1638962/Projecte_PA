# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:23:23 2022

@author: JoelT
"""
import sys
import traceback
import logging
from typing import List, Tuple
from películes import Pelicules
from board_games import Board_Games
from data import Data
import console_messages as co


logging.basicConfig(
    filename="log.txt",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s |%(pathname)s |%(funcName)s |%(lineno)d | %(message)s",
)

N_RECOMANACIONS = 5
MIN_VOTS = 10
K_USUARIS = 10
DIRECTORY_PEL = "ml-latest-small"
NAMES_FILES_PEL = ("movies.csv", "ratings.csv")
DIRECTORY_GAM = "archive"
NAMES_FILES_GAM = (
    "games.csv",
    "mechanics.csv",
    "subcategories.csv",
    "user_ratings.csv",
)


def recomanador():
    try:
        logging.info("S'ha iniciat el programa recomanació.")
        opcio_dataset = None
        dataset = None
        while opcio_dataset != 3:
            menu_select_dataset()
            opcio_dataset = int(input(co.cgray("Selecciona opció: ")))
            logging.debug("Opció dataset escollida: %s", opcio_dataset)
            if opcio_dataset == 1:
                dataset = Pelicules(DIRECTORY_PEL, NAMES_FILES_PEL)
                logging.debug(
                    "Incialitzat 'dataset' a  objecte 'Películes'.\n\t%s", dataset
                )
            elif opcio_dataset == 2:
                dataset = Board_Games(DIRECTORY_GAM, NAMES_FILES_GAM)
                logging.debug(
                    "Incialitzat 'dataset' a  objecte 'Board_Games'.\n\t%s", dataset
                )
            elif opcio_dataset == 3:
                print(co.clblue("Sortint del programa..."))
                dataset = None
                logging.debug("Dataset cleared i sortint del programa.\n\t%s", dataset)
            else:
                print(co.cdred("Error: Seleccioni opció vàlida."))
                opcio_dataset = None
                dataset = None
                logging.warning(
                    "Dataset i opció dataset cleared, opció no correcta.\n\t%s\n\t%s",
                    opcio_dataset,
                    dataset,
                )
            if dataset is not None:
                print(co.clblue("Carregant base de dades..."))
                dataset.read_data()
                print(co.clblue("Base de dades carregada."))
                opcio_recomanacio = None
                usuari = None
                while opcio_recomanacio != 4:
                    menu_select_recomanacio()
                    opcio_recomanacio = int(input(co.cgray("Selecciona una opció: ")))
                    logging.debug("Opció recomanació escollida: %s", opcio_recomanacio)
                    if opcio_recomanacio in (1, 2, 3):
                        usuari = input(
                            co.cgray(
                                "Selecciona un usuari entre 0-"
                                + str(dataset.filas)
                                + " : "
                            )
                        )
                        logging.debug("Usuari escollid: %s", usuari)
                        while usuari != "":
                            recomanacio = None
                            try:
                                usuari = int(usuari)
                            except ValueError as message:
                                print(co.cdred("Usuari ha de ser un enter postiu."))
                                logging.warning(str(message))
                            else:
                                try:
                                    if opcio_recomanacio == 1:
                                        recomanacio = dataset.top_popular_items(
                                            MIN_VOTS, int(usuari)
                                        )
                                    elif opcio_recomanacio == 2:
                                        recomanacio = dataset.other_users_also(
                                            K_USUARIS, int(usuari)
                                        )
                                    elif opcio_recomanacio == 3:
                                        print(co.cdred("Opció no implementada."))
                                except AssertionError as message:
                                    print(co.cdred(str(message)))
                                    logging.warning(str(message))
                                else:
                                    logging.debug("Recomanacions: %s", recomanacio)
                                    visualitza_rec(recomanacio[:N_RECOMANACIONS])
                                    recomanacio = None
                            usuari = input(co.cgray("Selecciona un usuari: "))
                            logging.debug("Usuari escollid: %s", usuari)
                    elif opcio_recomanacio == 4:
                        print(co.clblue("Sortint del menú..."))
                        dataset = None
                        logging.info(
                            "Dataset cleared i sortint de la selecció de recomanació.\n\t%s",
                            dataset,
                        )
                    else:
                        print(co.cdred("Error: Seleccioni opció vàlida."))
                        opcio_recomanacio = None
                        logging.warning(
                            "Opció recomanació cleared, opció no correcta.\n\t%s",
                            opcio_dataset,
                        )
    except:
        logging.fatal("S'ha terminat el programa recomanació. \n\t%s", dataset)
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
    if recomanacio is not None:
        logging.info("Iniciant visualització de les recomanacions.")
        logging.debug("\n\t%s", recomanacio)
        for i, elem in enumerate(recomanacio):
            print(co.cpurple("Recomendació " + str(i + 1)))
            print("\t" + co.cgreen("Títol") + ": " + elem[0].titol)
            for cat in elem[0].caracteristicas.keys():
                if elem[0].caracteristicas[cat]:
                    print(
                        "\t"
                        + co.cgreen(cat)
                        + ": "
                        + ", ".join(elem[0].caracteristicas[cat])
                    )
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


recomanador()
