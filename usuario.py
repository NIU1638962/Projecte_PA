# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:01:16 2022

@author: Joel Tapia Salvador
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:08:55 2022

@author: marcs
"""
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, datetime, timedelta
from abc import ABCMeta, abstractmethod

class Usuari:
    def __init__(self):
        self._index=0
        self._ident=""
    @property
    def index(self):
        return self._index
    @index.setter
    def index(self, valor):
        self._index=valor
    @property
    def ident(self):
        return self._index
    @ident.setter
    def ident(self, valor):
        self._ident=valor
