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
    _min_vots: int = 10
    _k_usuaris: int = 10
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
    _name_file_pickle: str = field(init=False, default="recomanacions.dat")

    @property
    def dataset(self):
        return self._dataset

    def __post_init__(self):
        logging.debug("Iniciant __post_init__ Recomanacions-subclass object.")
        assert (
            0 <= self._opcio_dataset < len(self._directoris)
        ), "Error: Seleccioni opció vàlida."
        self._create_dataset()
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

    def _create_dataset(self):
        if self._opcio_dataset == 0:
            self._dataset = Pelicules(
                self._directoris[self._opcio_dataset],
                self._files[self._opcio_dataset],
                self._pickle,
            )
            logging.debug(
                "Incialitzat 'dataset' a  objecte 'Películes'.\n\t%s", self._dataset
            )
        elif self._opcio_dataset == 1:
            self._dataset = BoardGames(
                self._directoris[self._opcio_dataset],
                self._files[self._opcio_dataset],
                self._pickle,
            )
            logging.debug(
                "Incialitzat 'dataset' a  objecte 'Board_Games'.\n\t%s", self._dataset
            )
        self._dataset.read_data()

    @abstractmethod
    def recomana(self, usuari):
        raise NotImplementedError()


@dataclass
class Recom_top_popular(Recomanacions):
    def __post_init__(self):
        self._name_file_pickle = (
            super()._name_file_pickle[:-4]
            + "_top_popular_"
            + str(self._n_recomanacions)
            + "_"
            + str(self._min_vots)
            + "_"
            + str(self._k_usuaris)
            + ".dat"
        )
        super().__post_init__()

    def recomana(self, usuari: int):
        if self._recomanacions[usuari] is None:
            self._recomanacions[usuari] = self._dataset.top_popular_items(
                self._min_vots, usuari
            )
            if self._pickle:
                self._save_pickle()
        return self._recomanacions[usuari][: self._n_recomanacions]


@dataclass
class Recom_other_users(Recomanacions):
    def __post_init__(self):
        self._name_file_pickle = (
            super()._name_file_pickle[:-4]
            + "_other_users_"
            + str(self._n_recomanacions)
            + "_"
            + str(self._min_vots)
            + "_"
            + str(self._k_usuaris)
            + ".dat"
        )
        super().__post_init__()

    def recomana(self, usuari: int):
        if self._recomanacions[usuari] is None:
            self._recomanacions[usuari] = self._dataset.other_users_also(
                self._k_usuaris, usuari
            )
            if self._pickle:
                self._save_pickle()
        return self._recomanacions[usuari][: self._n_recomanacions]


@dataclass
class Recom_you_liked(Recomanacions):
    def __post_init__(self):
        self._name_file_pickle = (
            super()._name_file_pickle[:-4]
            + "_you_liked_"
            + str(self._n_recomanacions)
            + "_"
            + str(self._min_vots)
            + "_"
            + str(self._k_usuaris)
            + ".dat"
        )
        super().__post_init__()

    def recomana(self, usuari):
        if self._recomanacions[usuari] is None:
            self._recomanacions[usuari] = self._dataset.because_you_liked(usuari)
            if self._pickle:
                self._save_pickle()
        return self._recomanacions[usuari][: self._n_recomanacions]
