# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:59 2022
@author: Joel Tapia Salvador (1638962) i Aksel Serret Llopis ()
"""

from dataclasses import dataclass, field
from typing import List, Dict
from abc import ABCMeta


@dataclass
class Data(metaclass=ABCMeta):
    _titol: str
    _identificador: str
    _columna: int

    @property
    def titol(self) -> str:
        """
        Getter del atribut _titol

        Returns
        -------
        str
            Títol del objecte.

        """
        return self._titol

    @titol.setter
    def titol(self, titol: str):
        """
        Setter del atribut _titol.

        Parameters
        ----------
        titol : str
            Titol del objecte..

        Returns
        -------
        None.

        """
        self._titol = titol

    @property
    def identificador(self) -> str:
        """
        Getter del atribut _identificador.

        Returns
        -------
        str
            Identificador intern del dataset del objecte.

        """
        return self._identificador

    @property
    def columna(self) -> int:
        """
        Getter del atribut _columna.

        Returns
        -------
        int
            Columna en la matriu de valoracions del dataset.

        """
        return self._columna


@dataclass
class Pelicula(Data):
    _caracteristicas: Dict[str, List[str]] = field(init=False, default_factory=dict)

    @property
    def caracteristicas(self) -> Dict[str, List[str]]:
        """
        Getter del atribut _caracteristicas.

        Returns
        -------
        Dict[str, List[str]]
            Característiques identificatories del objecte.

        """
        return self._caracteristicas


@dataclass
class Game(Data):
    _caracteristicas: Dict[str, List[str]] = field(init=False, default_factory=dict)

    @property
    def caracteristicas(self) -> Dict[str, List[str]]:
        """
        Getter del atribut _caracteristicas.

        Returns
        -------
        Dict[str, List[str]]
            Característiques identificatories del objecte.

        """
        return self._caracteristicas
