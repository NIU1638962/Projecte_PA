# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 10:11:27 2022

@author: Joel Tapia Salvador
"""
import os
from dataclasses import dataclass, field
from abc import ABCMeta, abstractmethod
from typing import List, Tuple, ClassVar
import logging
import pickle
from data import Data
from dataset import Dataset
from películes import Pelicules
from board_games import BoardGames


@dataclass
class Recomanacions(metaclass=ABCMeta):
    _opcio_dataset: int
    _n_recomanacions: int = 5
    _pickle: bool = True
    _recomanacions: List[List[Tuple[Data, float]]] = field(
        init=False, default_factory=list
    )
    _dataset: Dataset = field(init=False, default=None)
    _directoris: ClassVar[Tuple[str]] = ("ml-latest-small", "archive_reduced")
    _files: ClassVar[Tuple[Tuple[str]]] = (
        ("movies.csv", "ratings.csv"),
        ("games.csv", "mechanics.csv", "subcategories.csv", "user_ratings.csv",),
    )
    _max_pun: ClassVar[Tuple[int]] = (5, 10)
    _name_file_pickle: str = field(init=False, default="recomanacions.dat")

    @property
    def dataset(self):
        return self._dataset

    @property
    def n_recomanacions(self):
        return self._n_recomanacions

    @property
    def directori(self):
        return self._directoris[self._opcio_dataset]

    @property
    def max_pun(self):
        return self._max_pun[self._opcio_dataset]

    def inicia(self, n, theta, min_vots, k_usuaris, test):
        logging.debug("Iniciant inicia Recomanacions-subclass object.")
        assert (
            0 <= self._opcio_dataset < len(self._directoris)
        ), "Error: Seleccioni opció de dataset vàlida."
        self._create_dataset(n, theta, min_vots, k_usuaris, test)
        logging.debug(
            "Directori: \n\t%s",
            "./" + self._directoris[self._opcio_dataset] + "_pickle",
        )
        logging.debug("Arxiu: \n\t%s", self._name_file_pickle)
        if self._pickle and self._name_file_pickle in os.listdir(
            "./" + self._directoris[self._opcio_dataset] + "_pickle"
        ):
            logging.debug("Entrant a pickle.\n\t%s", self._pickle)
            self._load_pickle()
        else:
            logging.debug("No entrant a pickle.\n\t%s", self._pickle)
            self._recomanacions = [None for i in range(self._dataset.filas)]

    def _save_pickle(self):
        logging.debug("_save_pickle Recomanacions-subclass object")
        with open(
            self._directoris[self._opcio_dataset] + "_pickle/" + self._name_file_pickle,
            "wb",
        ) as file:
            pickle.dump(self._recomanacions, file)

    def _load_pickle(self):
        logging.debug("_load_pickle Recomanacions-subclass object")
        with open(
            self._directoris[self._opcio_dataset] + "_pickle/" + self._name_file_pickle,
            "rb",
        ) as file:
            self._recomanacions = pickle.load(file)

    def _create_dataset(self, n, theta, min_vots, k_usuaris, test):
        if self._opcio_dataset == 0:
            self._dataset = Pelicules(
                self._directoris[self._opcio_dataset],
                self._files[self._opcio_dataset],
                self._max_pun[self._opcio_dataset],
                min_vots,
                k_usuaris,
                self._pickle,
                test,
            )
            logging.debug(
                "Incialitzat 'dataset' a  objecte 'Películes'.\n\t%s", self._dataset
            )
        elif self._opcio_dataset == 1:
            self._dataset = BoardGames(
                self._directoris[self._opcio_dataset],
                self._files[self._opcio_dataset],
                self._max_pun[self._opcio_dataset],
                min_vots,
                k_usuaris,
                self._pickle,
                test,
            )
            logging.debug(
                "Incialitzat 'dataset' a  objecte 'Board_Games'.\n\t%s", self._dataset
            )
        self._dataset.inicia(n, theta, self._n_recomanacions)
        self._dataset.read_data()

    @abstractmethod
    def unsorted_undata_recomana(self, usuari):
        raise NotImplementedError()

    def recomana(self, usuari):
        if self._recomanacions[usuari] is None:
            self._recomanacions[usuari] = sorted(
                self._dataset.to_data_object(
                    self.unsorted_undata_recomana(usuari), usuari
                ),
                key=lambda x: x[1],
                reverse=True,
            )

            if self._pickle:
                self._save_pickle()
        return self._recomanacions[usuari][: self._n_recomanacions]


@dataclass
class Recom_top_popular(Recomanacions):
    def inicia(self, n, theta, min_vots, k_usuaris, test):
        self._name_file_pickle = (
            super()._name_file_pickle[:-4]
            + "_top_popular_"
            + str(self._n_recomanacions)
            + "_"
            + str(min_vots)
            + "_"
            + str(k_usuaris)
        )
        if test:
            self._name_file_pickle += "_test"
        self._name_file_pickle += ".dat"
        super().inicia(n, theta, min_vots, k_usuaris, test)

    def unsorted_undata_recomana(self, usuari: int):
        return self._dataset.top_popular_items(usuari)


@dataclass
class Recom_other_users(Recomanacions):
    def inicia(self, n, theta, min_vots, k_usuaris, test):
        self._name_file_pickle = (
            super()._name_file_pickle[:-4]
            + "_other_users_"
            + str(self._n_recomanacions)
            + "_"
            + str(min_vots)
            + "_"
            + str(k_usuaris)
        )
        if test:
            self._name_file_pickle += "_test"
        self._name_file_pickle += ".dat"
        super().inicia(n, theta, min_vots, k_usuaris, test)

    def unsorted_undata_recomana(self, usuari: int):
        return self._dataset.other_users_also(usuari)


@dataclass
class Recom_you_liked(Recomanacions):
    def inicia(self, n, theta, min_vots, k_usuaris, test):
        self._name_file_pickle = (
            super()._name_file_pickle[:-4]
            + "_you_liked_"
            + str(self._n_recomanacions)
            + "_"
            + str(min_vots)
            + "_"
            + str(k_usuaris)
        )
        if test:
            self._name_file_pickle += "_test"
        self._name_file_pickle += ".dat"
        super().inicia(n, theta, min_vots, k_usuaris, test)

    def unsorted_undata_recomana(self, usuari):
        return self._dataset.because_you_liked(usuari)
