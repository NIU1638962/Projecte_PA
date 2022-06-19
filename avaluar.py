# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:42:35 2022

@author: JoelT
"""
import os
from dataclasses import dataclass, field
import logging
import pickle
from scipy.sparse import lil_matrix
import numpy as np
from typing import ClassVar, Tuple, List
from recomanacions import (
    Recom_other_users,
    Recom_top_popular,
    Recom_you_liked,
    Recomanacions,
)
from data import Data
import console_messages as co


@dataclass
class Avaluar:
    _n: int
    _theta: float
    _opcio_recomanacio: int
    _pickle: bool = True
    _test: bool = field(init=False, default=False)
    _recomanacio: Recomanacions = field(init=False, default=None)
    _original: lil_matrix = field(init=False, default=None)
    _resultat: List[
        Tuple[
            List[Tuple[Data, float]],
            List[Tuple[Data, float]],
            Tuple[float, float, float],
        ]
    ] = field(init=False, default_factory=list)
    _name_file_pickle: ClassVar[Tuple[str]] = ("original", "resultat.dat")

    @property
    def recomanacio(self):
        return self._recomanacio

    def inicia(
        self, opcio_dataset: int, n_recomanacions: int, min_vots: int, k_usuaris: int,
    ):
        assert (
            0 <= self._opcio_recomanacio < 3
        ), "Error: Seleccioni opció de recomanació vàlida."
        assert (
            0 < self._theta <= 1
        ), "Theta no cumpleix els parametres de percentatge, ha d'estar entre 0 i 1."
        self._create_recomanacio(opcio_dataset, n_recomanacions, min_vots, k_usuaris)
        self._theta = self._theta * self._recomanacio.max_pun

    def _create_recomanacio(
        self, opcio_dataset: int, n_recomanacions: int, min_vots: int, k_usuaris: int,
    ):
        if self._opcio_recomanacio == 0:
            self._recomanacio = Recom_top_popular(
                opcio_dataset, n_recomanacions, self._pickle
            )
            logging.debug(
                "Incialitzat 'recomanacio' a  objecte 'Recom_top_popular'.\n\t%s",
                self._recomanacio,
            )
        elif self._opcio_recomanacio == 1:
            self._recomanacio = Recom_other_users(
                opcio_dataset, n_recomanacions, self._pickle
            )
            logging.debug(
                "Incialitzat 'recomanacio' a  objecte 'Recom_other_users'.\n\t%s",
                self._recomanacio,
            )
        elif self._opcio_recomanacio == 2:
            self._recomanacio = Recom_you_liked(
                opcio_dataset, n_recomanacions, self._pickle
            )
            logging.debug(
                "Incialitzat 'recomanacio' a  objecte 'Recom_you_liked'.\n\t%s",
                self._recomanacio,
            )
        self._recomanacio.inicia(
            self._n,
            self._opcio_recomanacio,
            self._theta / self._recomanacio.max_pun,
            min_vots,
            k_usuaris,
            self._test,
        )

    def recomana(self, usuari: int):
        return self._recomanacio.recomana(usuari)

    def visualitza(self, recomanacio: List[Tuple[Data, float]]):
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

    def del_recomanacio(self):
        self._recomanacio.del_dataset()
        del self._recomanacio
        while len(self._resultat) > 0:
            del self._resultat[0]
        del self._resultat
        return

    def __del__(self):
        logging.debug("Avaluar deleted from existence.")


@dataclass
class Avaluar_Test(Avaluar):
    _test: bool = field(init=False, default=True)

    def inicia(self, opcio_dataset, n_recomanacions, min_vots, k_usuaris):
        super().inicia(opcio_dataset, n_recomanacions, min_vots, k_usuaris)
        self._name_file_pickle = tuple(
            i[:-4]
            + "_"
            + str(self._n)
            + "_"
            + str(self._opcio_recomanacio)
            + "_"
            + str(self._theta / self._recomanacio.max_pun)
            + "_"
            + str(n_recomanacions)
            + "_"
            + str(min_vots)
            + "_"
            + str(k_usuaris)
            + ".dat"
            for i in self._name_file_pickle
        )
        if self._pickle and [
            i in os.listdir("./" + self._recomanacio.directori + "_pickle")
            for i in self._name_file_pickle
        ].count(True) == len(self._name_file_pickle):
            logging.debug("Entrant a pickle.\n\t%s", self._pickle)
            self._load_pickle()
        else:
            logging.debug("No entrant a pickle.\n\t%s", self._pickle)
            self._resultat = [None for i in range(self._recomanacio.dataset.filas)]
            self._original = self._recomanacio.dataset.generate_training_set(self._n)
            self._save_pickle()

    def _save_pickle(self):
        logging.debug("_save_pickle Avaluar-class object")
        with open(
            self._recomanacio.directori + "_pickle/" + self._name_file_pickle[0], "wb",
        ) as file1, open(
            self._recomanacio.directori + "_pickle/" + self._name_file_pickle[1], "wb",
        ) as file2:
            pickle.dump(self._original, file1)
            pickle.dump(self._resultat, file2)

    def _load_pickle(self):
        logging.debug("_load_pickle Avaluar-class object")
        with open(
            self._recomanacio.directori + "_pickle/" + self._name_file_pickle[0], "rb",
        ) as file1, open(
            self._recomanacio.directori + "_pickle/" + self._name_file_pickle[1], "rb",
        ) as file2:
            self._original = pickle.load(file1)
            self._resultat = pickle.load(file2)

    def recomana(self, usuari):
        if self._resultat[usuari] is None:
            resultats = self._recomanacio.unsorted_undata_recomana(usuari)
            test_u = self._original[usuari].copy()
            self._resultat[usuari] = (
                self._recomanacio.recomana(usuari),
                [
                    i
                    for i in sorted(
                        self._recomanacio.dataset.to_data_object(
                            test_u[:, self._n :], usuari
                        ),
                        key=lambda x: x[1],
                        reverse=True,
                    )
                    if i[1] > self._theta
                ],
                (
                    self._mae(resultats, test_u),
                    self._precision(resultats, test_u),
                    self._recall(resultats, test_u),
                ),
            )
        if pickle:
            self._save_pickle()
        return self._resultat[usuari]

    def _mae(self, resultats: lil_matrix, test_u: lil_matrix):
        resultats = resultats[:, self._n :]
        test_u = lil_matrix(test_u[:, self._n :])
        con = test_u != 0
        num = (np.abs(resultats[con] - test_u[con])).sum()
        den = (test_u[con]).count_nonzero()
        try:
            res = num / den
        except ZeroDivisionError:
            if 0 <= num < 0.01:
                return 0
            else:
                return float("inf")
        else:
            return res

    def _precision(self, resultats: lil_matrix, test_u: lil_matrix):
        dtype = [("resultats", float), ("test_u", float)]
        resultats = resultats[:, self._n :].toarray()
        resultats = resultats.reshape((resultats.shape[1]))
        test_u = test_u[:, self._n :].toarray()
        test_u = test_u.reshape((test_u.shape[1]))
        con = test_u == 0
        resultats[con] = 0
        temp = np.array([(i, j) for i, j in zip(resultats, test_u)], dtype=dtype)
        temp = np.flip(np.sort(temp, order="resultats"))[
            self._recomanacio.n_recomanacions
        ]
        con = temp["test_u"] > self._theta
        num = temp[con].size
        den = self._recomanacio.n_recomanacions
        try:
            res = num / den
        except ZeroDivisionError:
            if 0 <= num < 0.01:
                return 0
            else:
                return float("inf")
        else:
            return res

    def _recall(self, resultats: lil_matrix, test_u: lil_matrix):
        dtype = [("resultats", float), ("test_u", float)]
        resultats = resultats[:, self._n :].toarray()
        resultats = resultats.reshape((resultats.shape[1]))
        test_u = test_u[:, self._n :].toarray()
        test_u = test_u.reshape((test_u.shape[1]))
        con = test_u == 0
        resultats[con] = 0
        temp = np.array([(i, j) for i, j in zip(resultats, test_u)], dtype=dtype)
        temp = np.flip(np.sort(temp, order="resultats"))[
            self._recomanacio.n_recomanacions
        ]
        con1 = temp["test_u"] > self._theta
        con2 = test_u > self._theta
        num = temp[con1].size
        den = test_u[con2].size
        try:
            res = num / den
        except ZeroDivisionError:
            if 0 <= num < 0.01:
                return 0
            else:
                return float("inf")
        else:
            return res

    def visualitza(
        self,
        resultat: Tuple[
            List[Tuple[Data, float]],
            List[Tuple[Data, float]],
            Tuple[float, float, float],
        ],
    ):
        if resultat == ():
            logging.warn("Resultat está buit.")
            print(co.cpurple("No hi ha recomanacions."))
        elif resultat is not None:
            logging.info("Iniciant visualització de les recomanacions.")
            logging.debug("\n\t%s", resultat)
            print(co.cpurple("\nMillors prediccions del sistema:"))
            for elem in resultat[0]:
                print("\t" + co.cgreen("Identificador: ") + str(elem[0].titol))
                print("\t" + co.cgreen("Score: ") + str(elem[1]))
            print(co.cpurple("\nValoracions de l'usuari que superen el llindar:"))
            for elem in resultat[1]:
                print("\t" + co.cgreen("Identificador: ") + str(elem[0].titol))
                print("\t" + co.cgreen("Score: ") + str(elem[1]))
            print(co.cpurple("\nMesures de comparació: "))
            for nom, pun in zip(
                ("Mean absolute error", "Precision", "Recall"), resultat[2]
            ):
                print("\t" + co.cgreen(nom + ": ") + str(pun))
            logging.info("Visualització finalitzada.")
