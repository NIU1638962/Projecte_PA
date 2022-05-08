# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 11:02:20 2022

@author: Joel Tapia Salvador (1638962)
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


def eul(message: str) -> str:
    """
    Underline message.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return EUL + message + ERESET


def cblack(message: str) -> str:
    """
    Message colour black.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CBLACK + message + ERESET


def cdred(message: str) -> str:
    """
    Message colour dark red.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CDRED + message + ERESET


def cgreen(message: str) -> str:
    """
    Message colour green.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CGREEN + message + ERESET


def clred(message: str) -> str:
    """
    Message colour light red.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CLRED + message + ERESET


def cdblue(message: str) -> str:
    """
    Message colour dark blue.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CDBLUE + message + ERESET


def cpurple(message: str) -> str:
    """
    Message colour purple.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CPURPLE + message + ERESET


def clblue(message: str) -> str:
    """
    Message colour light blue.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CLBLUE + message + ERESET


def cgray(message: str) -> str:
    """
    Message colour gray.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return CGRAY + message + ERESET


def bblack(message: str) -> str:
    """
    Message background black.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BBLACK + message + ERESET


def bdred(message: str) -> str:
    """
    Message background dark red.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BDRED + message + ERESET


def bgreen(message: str) -> str:
    """
    Message background green.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BGREEN + message + ERESET


def blred(message: str) -> str:
    """
    Message background light red.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BLRED + message + ERESET


def bdblue(message: str) -> str:
    """
    Message background dark blue.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BDBLUE + message + ERESET


def bpurple(message: str) -> str:
    """
    Message background purple.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BPURPLE + message + ERESET


def blblue(message: str) -> str:
    """
    Message background light blue.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BLBLUE + message + ERESET


def bgray(message: str) -> str:
    """
    Message background gray.

    Parameters
    ----------
    message : str
        Message to be transformed.

    Returns
    -------
    str
        Message tranformed.

    """
    return BGRAY + message + ERESET
