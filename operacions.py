# -*- coding: utf-8 -*-
"""
Created on Fri May  6 08:47:59 2022

@author: Joel Tapia Salvador (1638962)
"""
import numpy as np


def similitud(array_u: np.array, array_v: np.array) -> float:
    """
    Càlcula la similitud, posició a posició entre dos arrays de la mateixa
    mida, ignorant les posiciones on al menys un dels dos arrays té un 0.

    Parameters
    ----------
    array_u : np.array
        Array numpy numéric.
    array_v : np.array
        Array numpy numéric.

    Returns
    -------
    float
        Similitud entre els dos arrays, 0 si no hi ha cap posició on tot dos
        arrays no tenen el valor 0.

    """
    con = (array_u != 0) * (array_v != 0)
    if np.any(con):
        return ((array_u[con] * array_v[con]).sum()) / (
            (np.sqrt((array_u[con] ** 2).sum())) * (np.sqrt((array_v[con] ** 2).sum()))
        )
    return 0
