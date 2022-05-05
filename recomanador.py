# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:23:23 2022

@author: JoelT
"""
from dataset import Pelicules, Board_Games
import console_messages as co

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
    opcio_dataset = None
    dataset = None
    while opcio_dataset != 3:
        menu_select_dataset()
        opcio_dataset = int(input(co.cgray("Selecciona opció: ")))
        if opcio_dataset == 1:
            dataset = Pelicules(DIRECTORY_PEL, NAMES_FILES_PEL)
        elif opcio_dataset == 2:
            dataset = Board_Games(DIRECTORY_GAM, NAMES_FILES_GAM)
        elif opcio_dataset == 3:
            print(co.clblue("Sortint del programa..."))
            dataset = None
        else:
            print(co.CDRED("Error: Seleccioni opció vàlida."))
            opcio_dataset = None
            dataset = None
        if dataset is not None:
            print(co.clblue("Carregant base de dades..."))
            dataset.read_data()
            print(co.clblue("Base de dades carregada."))
            opcio_recomanacio = None
            usuari = None
            while opcio_recomanacio != 4:
                menu_select_recomanacio()
                opcio_recomanacio = int(input(co.cgray("Selecciona una opció: ")))
                if opcio_recomanacio == 1:
                    while usuari() != "":
                        int(input(co.cgray("Selecciona un usuari: ")))
                        dataset.top_popular_items(10, usuari)
                elif opcio_recomanacio == 2:
                    print(co.cdred("Opció no implementada."))
                elif opcio_recomanacio == 3:
                    print(co.cdred("Opció no implementada."))
                elif opcio_recomanacio == 4:
                    print(co.clblue("Sortint del menú..."))
                    dataset = None
                else:
                    print(co.cdred("Error: Seleccioni opció vàlida."))
                    opcio_recomanacio = None


def menu_select_dataset():
    print("\n")
    print(co.cpurple("MENÚ SELECCIÓ DATA SET"))
    print(co.cgreen(" (1) Películes."))
    print(co.cgreen(" (2) Jocs de taula."))
    print(co.cgreen(" (3) Sortir del programa."))


def menu_select_recomanacio():
    print("\n")
    print(co.cpurple("MENÚ SELECCIÓ MÉTODE RECOMANACIÓ"))
    print(co.cgreen(" (1) Recomanació simple."))
    print(co.cgreen(" (2) Recomanació col·laborativa."))
    print(co.cgreen(" (3) Recomanació basada en continguts."))
    print(co.cgreen(" (4) Sortir del menú."))


recomanador()
