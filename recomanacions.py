# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 10:11:27 2022

@author: Joel Tapia Salvador
"""
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
    _directoris = ClassVar[Tuple[str]] = ("ml-latest-small", "archive_reduced")
    _files = ClassVar[Tuple[Tuple[str]]] = (
        ("movies.csv", "ratings.csv"),
        ("games.csv", "mechanics.csv", "subcategories.csv", "user_ratings.csv",),
    )
    _name_file_pickle: str = field(init=False, default="_pickle/recomanacions.dat")

    @property
    def dataset(self):
        return self._dataset

    def __post_init__(self):
        assert (
            0 <= self._opcio_dataset < len(self._directoris)
        ), "Error: Seleccioni opció vàlida."
        self._create_dataset()
        if self._pickle:
            self._load_pickle()
        else:
            self._recomanacions = [None for i in range(self._dataset.filas)]

    def _save_pickle(self):
        with open(
            self._directoris[self._opcio_dataset] + self._name_file_pickle, "wb"
        ) as file:
            pickle.dump(self, file)

    def _load_pickle(self):
        with open(
            self._directoris[self._opcio_dataset] + self._name_file_pickle, "rb"
        ) as file:
            self = pickle.load(file)

    def _create_dataset(self):
        if self._opcio_dataset == 0:
            dataset = Pelicules(
                self._directoris[self._opcio_dataset],
                self._files[self._opcio_dataset],
                self._pickle,
            )
        elif self._opcio_dataset == 1:
            dataset = BoardGames(
                self._directoris[self._opcio_dataset],
                self._files[self._opcio_dataset],
                self._pickle,
            )
        logging.debug("Incialitzat 'dataset' a  objecte 'Board_Games'.\n\t%s", dataset)

    @abstractmethod
    def recomana(self, usuari):
        raise NotImplementedError()


@dataclass
class Recom_top_popular(Recomanacions):
    _name_file_pickle: str = field(
        init=False, default=super()._name_file_pickle[:-3] + "_top_popular.dat"
    )

    def recomana(self, usuari: int):
        if self._recomanacions[usuari] is None:
            self._recomanacions[usuari] = self._dataset.top_popular_items(
                self._min_vots, usuari
            )
            self._save_pickle()
        return self._recomanacions[usuari][self._k_usuaris]


@dataclass
class Recom_other_users(Recomanacions):
    _name_file_pickle: str = field(
        init=False, default=super()._name_file_pickle[:-3] + "_other_users.dat"
    )

    def recomana(self, usuari: int):
        if self._recomanacions[usuari] is None:
            self._recomanacions[usuari] = self._dataset.other_users_also(
                self._k_usuaris, usuari
            )
            self._save_pickle()
        return self._recomanacions[usuari][self._k_usuaris]


@dataclass
class Recom_you_liked(Recomanacions):
    _name_file_pickle: str = field(
        init=False, default=super()._name_file_pickle[:-3] + "_you_liked.dat"
    )

    def recomana(self, usuari):
        if self._recomanacions[usuari] is None:
            self._recomanacions[usuari] = self._dataset.because_you_liked(usuari)
            self._save_pickle()
        return self._recomanacions[usuari][self._k_usuaris]
