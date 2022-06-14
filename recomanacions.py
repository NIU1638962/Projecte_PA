# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 10:11:27 2022

@author: Joel Tapia Salvador
"""
from dataclasses import dataclass, field
from abc import ABCMeta, abstractmethod
from typing import List, Tuple
import logging
from data import Data
from dataset import Dataset
from películes import Pelicules
from board_games import BoardGames

DIRECTORIS = ("ml-latest-small", "archive_reduced")
FILES = (
    ("movies.csv", "ratings.csv"),
    ("games.csv", "mechanics.csv", "subcategories.csv", "user_ratings.csv",),
)


@dataclass
class Recomanacions(metaclass=ABCMeta):
    _opcio_dataset: int
    _n_recomanacions: int = 0
    _min_vots: int = 0
    _k_usuaris: int = 0
    _pickle: bool = True
    _recomanacions: List[List[Tuple[Data, float]]] = field(
        init=False, default_factory=list
    )
    _dataset: Dataset = field(init=False, default=None)

    @property
    def dataset(self):
        return self._dataset

    def __post_init__(self):
        assert (
            0 <= self._opcio_dataset < len(DIRECTORIS)
        ), "Error: Seleccioni opció vàlida."
        if self._pickle:
            self._load_pickle()
        else:
            pass

    def _load_pickle(self):
        pass

    def _create_dataset(self):
        if self._opcio_dataset == 0:
            dataset = Pelicules(DIRECTORIS[0], FILES[0])
            logging.debug(
                "Incialitzat 'dataset' a  objecte 'Películes'.\n\t%s", dataset
            )
        elif self._opcio_dataset == 1:
            dataset = BoardGames(DIRECTORIS[1], FILES[1])
            logging.debug(
                "Incialitzat 'dataset' a  objecte 'Board_Games'.\n\t%s", dataset
            )

    @abstractmethod
    def recomana(self, usuari):
        raise NotImplementedError()


@dataclass
class Recom_top_popular(Recomanacions):
    def recomana(self, usuari: int):
        self._dataset.top_popular_items(self._min_vots, usuari)


@dataclass
class Recom_other_users(Recomanacions):
    def recomana(self, usuari: int):
        self._dataset.other_users_also(self._k_usuaris, usuari)


@dataclass
class Recom_you_liked(Recomanacions):
    def recomana(self, usuari):
        self._dataset.because_you_liked(usuari)
