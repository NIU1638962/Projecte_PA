# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:59 2022
@author: Joel Tapia Salvador (1638962) i Aksel Serret Llopis ()
"""

from dataclasses import dataclass, field
from typing import List, Dict
from abc import ABCMeta, abstractclassmethod
import console_messages as co


@dataclass
class Data(metaclass=ABCMeta):
    _titol: str
    _identificador: str
    _columna: int
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

    @caracteristicas.setter
    def caracteristicas(self, new_value):
        self._caracteristicas = new_value

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

    @abstractclassmethod
    def visualitza(self):
        raise NotImplementedError

    @abstractclassmethod
    def caract_to_str(self) -> str:
        raise NotImplementedError


@dataclass
class Pelicula(Data):
    def visualitza(self):
        print("\t" + co.cgreen("Títol") + ": " + self.titol)
        for cat in self._caracteristicas.keys():
            print("\t" + co.cgreen(cat) + ": " + ", ".join(self.caracteristicas[cat]))

    def caract_to_str(self) -> str:
        carac = ""
        for cat in self._caracteristicas.keys():
            carac += "|".join(self.caracteristicas[cat])
        return carac


@dataclass
class Game(Data):
    def visualitza(self):
        print("\t" + co.cgreen("Títol") + ": " + self.titol)
        for cat in self.caracteristicas.keys():
            if (
                isinstance(self.caracteristicas[cat], list)
                and len(self.caracteristicas[cat]) > 0
            ):
                print(
                    "\t" + co.cgreen(cat) + ": " + ", ".join(self.caracteristicas[cat])
                )
            elif (
                isinstance(self.caracteristicas[cat], bool)
                and self.caracteristicas[cat]
            ):
                print("\t" + co.cgreen(cat))
            elif isinstance(self.caracteristicas[cat], str):
                print("\t" + co.cgreen(cat) + ": " + self.caracteristicas[cat])

    def caract_to_str(self) -> str:
        carac = ""
        for cat in self.caracteristicas.keys():
            if (
                isinstance(self.caracteristicas[cat], list)
                and len(self.caracteristicas[cat]) > 0
            ):
                carac += "|".join(self.caracteristicas[cat])
            elif (
                isinstance(self.caracteristicas[cat], bool)
                and self.caracteristicas[cat]
            ):
                carac += "|" + str(cat)
            elif isinstance(self.caracteristicas[cat], str):
                carac += "|" + self.caracteristicas[cat]
        return carac
