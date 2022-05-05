# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:59 2022
@author: Joel Tapia Salvador
Created on Wed Apr 27 17:25:24 2022
@author: marcs
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
    def titol(self):
        return self._titol

    @titol.setter
    def titol(self, titol):
        self._titol = titol

    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, iden):
        self._identificador = iden

    @property
    def columna(self):
        return self._columna

    @columna.setter
    def columna(self, colm):
        self._columna = colm


@dataclass
class Pelicula(Data):
    _caracteristicas: Dict[str, List[str]] = field(init=False, default_factory=dict)

    @property
    def caracteristicas(self):
        return self._caracteristicas

    @caracteristicas.setter
    def caracteristicas(self, valor):
        if isinstance(valor, dict):
            self._caracteristicas = valor
        else:
            raise TypeError


@dataclass
class Game(Data):
    _caracteristicas: Dict[str, int] = field(init=False, default_factory=dict)

    @property
    def caracteristicas(self):
        return self._caracteristicas

    @caracteristicas.setter
    def caracteristicas(self, valor):
        if isinstance(valor, dict):
            self._caracteristicas = valor
        else:
            raise TypeError
