# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 11:02:20 2022

@author: JoelT
"""
ERESET = "\33[0m"
EUL = "\33[4m"
CBLACK = "\33[30m"
CDRED = "\33[31m"
CGREEN = "\33[32m"
CLRED = "\33[33m"
CDBLUE = "\33[34m"
CPURPLE = "\33[35m"
CLBLUE = "\33[36m"
CGRAY = "\33[37m"
BBLACK = "\33[40m"
BDRED = "\33[41m"
BGREEN = "\33[42m"
BLRED = "\33[43m"
BDBLUE = "\33[44m"
BPURPLE = "\33[45m"
BLBLUE = "\33[46m"
BGRAY = "\33[47m"


def eul(message: str):
    return EUL + message + ERESET


def cblack(message: str):
    return CBLACK + message + ERESET


def cdred(message: str):
    return CDRED + message + ERESET


def cgreen(message: str):
    return CGREEN + message + ERESET


def clred(message: str):
    return CLRED + message + ERESET


def cdblue(message: str):
    return CDBLUE + message + ERESET


def cpurple(message: str):
    return CPURPLE + message + ERESET


def clblue(message: str):
    return CLBLUE + message + ERESET


def cgray(message: str):
    return CGRAY + message + ERESET


def bblack(message: str):
    return BBLACK + message + ERESET


def bdred(message: str):
    return BDRED + message + ERESET


def bgreen(message: str):
    return BGREEN + message + ERESET


def blred(message: str):
    return BLRED + message + ERESET


def bdblue(message: str):
    return BDBLUE + message + ERESET


def bpurple(message: str):
    return BPURPLE + message + ERESET


def blblue(message: str):
    return BLBLUE + message + ERESET


def bgray(message: str):
    return BGRAY + message + ERESET
