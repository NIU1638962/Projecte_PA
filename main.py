# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 19:40:30 2022

@author: Joel Tapia Salvador
"""
from recomanador import Recomanador


N_RECOMANACIONS = 5
MIN_VOTS = 10
K_USUARIS = 10

recomanador = Recomanador(N_RECOMANACIONS, MIN_VOTS, K_USUARIS)
recomanador.recomanador()
