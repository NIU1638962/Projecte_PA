# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:59 2022

@author: Joel Tapia Salvador
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:25:24 2022

@author: marcs
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, datetime, timedelta
from abc import ABCMeta, abstractmethod

@dataclass
class Data :
    _titol: str()
    _identificador: int()
    _caracteristicas: Dict[int, str]
    
    @property
    def titol(self):
        return self._titol
    @titol.setter
    def titol(self, titol):
        self._titol=titol
    @property
    def identificador(self):
            return self._identificador
    @identificador.setter
    def identificador(self, iden):
        self._identificador=iden
    @property
    def caracteristicas(self):
        return self._caracteristicas
    @caracteristicas.setter
    def caracteristicas(self, valor):
        self._caracteristicas=valor
@dataclass
class Pelicula(Data):
    @property
    def titol(self):
        return self._titol
    @titol.setter
    def titol(self, titol):
        self._titol=titol
    @property
    def identificador(self):
            return self._identificador
    @identificador.setter
    def identificador(self, iden):
        self._identificador=iden
    @property
    def caracteristicas(self):
        return self._caracteristicas
    @caracteristicas.setter
    def caracteristicas(self, valor):
        self._caracteristicas=valor
    
@dataclass
class Game(Data):
    @property
    def titol(self):
        return self._titol
    @titol.setter
    def titol(self, titol):
        self._titol=titol
    @property
    def identificador(self):
            return self._identificador
    @identificador.setter
    def identificador(self, iden):
        self._identificador=iden
    @property
    def caracteristicas(self):
        return self._caracteristicas
    @caracteristicas.setter
    def caracteristicas(self, valor):
        self._caracteristicas=valor
    
