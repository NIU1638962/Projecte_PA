# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:01:16 2022
@author: Joel Tapia Salvador (1638962) i Aksel Serret Llopis ()
"""
from dataclasses import dataclass, field
import logging
from typing import List, Dict


@dataclass
class Usuari:
    _nom: str
    _fila: int
    _gustos: Dict[str, List[str]] = field(init=False, default_factory=dict)

    @property
    def nom(self) -> str:
        """
        Getter del atribut _nom.

        Returns
        -------
        str
            Nom del usuari.

        """
        return self._nom

    @property
    def fila(self) -> int:
        """
        Getter del atribut _fila.

        Returns
        -------
        int
            Fila en la qual es troben les valoracions del usuari dins de la mtriu
            de valoracions..

        """
        return self._fila

    @property
    def gustos(self) -> Dict[str, List[str]]:
        """
        Getter del atribut _gustos.

        Returns
        -------
        Dict[str, List[str]]
            Gustos identificatoris del usuari.

        """
        return self._gustos

    def __del__(self):
        """
        Per grabar al log d'execució si l'objecte s'ha eliminat.

        Returns
        -------
        None.

        """
        logging.debug("User deleted from existence.")
