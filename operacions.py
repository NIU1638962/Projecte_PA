# -*- coding: utf-8 -*-
"""
Created on Fri May  6 08:47:59 2022

@author: JoelT
"""
import numpy as np


def similitud(u, v):
    con = (u != 0) * (v != 0)
    if np.any(con):
        return ((u[con] * v[con]).sum()) / (
            (np.sqrt((u[con] ** 2).sum())) * (np.sqrt((v[con] ** 2).sum()))
        )
    return 0
