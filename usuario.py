# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:01:16 2022
@author: Joel Tapia Salvador
Created on Wed Apr 27 17:08:55 2022
@author: marcs
"""
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Usuari:
    _nom: str
    _fila: int
    _gustos: Dict[str, List[str]] = field(init=False, default_factory=dict)

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        self._nom = nom

    @property
    def fila(self):
        return self._fila

    @fila.setter
    def fila(self, fila):
        self._fila = fila

    @property
    def gustos(self):
        return self._gustos

    @gustos.setter
    def gustos(self, valor):
        if isinstance(valor, dict):
            self._gustos = valor
        else:
            raise TypeError
