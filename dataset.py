# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:00:34 2022

@author: Joel Tapia Salvador (1638962) i Aksel Serret Llopis ()
"""
from dataclasses import dataclass, field
from typing import Dict, Tuple, ClassVar, List
from abc import ABCMeta, abstractmethod
import logging
import pickle
import os
import numpy as np
from scipy.sparse import lil_matrix
from data import Data
from usuario import Usuari
from operacions import similitud
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class Dataset(metaclass=ABCMeta):

    _directory: str
    _names_files: Tuple[str]
    _max_pun: int = 10
    _min_vots: int = 10
    _k_usuaris: int = 10
    _pickle: bool = True
    _test: bool = False
    _elementos: Tuple[Dict[str, Data]] = field(init=False, default=({}, {}, {}))
    _usuarios: Tuple[Dict[str, Usuari]] = field(init=False, default=({}, {}))
    _valoraciones: lil_matrix = field(init=False, default=None)
    _columnas: int = field(init=False, default=0)
    _filas: int = field(init=False, default=0)
    _scores_top_popular_items: lil_matrix = field(init=False, default=None)
    _names_files_pickle: ClassVar[Tuple[str]] = (
        "valoraciones.dat",
        "elementos(0).dat",
        "elementos(1).dat",
        "elementos(2).dat",
        "usuarios(0).dat",
        "usuarios(1).dat",
        "filas.dat",
        "columnas.dat",
        "scores_top_popular_items.dat",
        "min_vots.dat",
    )

    def __post_init__(self):
        self._names_files_pickle = tuple(
            i[:-4] + "_" + str(self._min_vots) + "_" + str(self._k_usuaris)
            for i in self._names_files_pickle
        )
        if self._test:
            self._names_files_pickle = tuple(
                i + "_test" for i in self._names_files_pickle
            )
        self._names_files_pickle = tuple(i + ".dat" for i in self._names_files_pickle)
        self._names_files_pickle = tuple(
            self._directory + "_pickle" + "/" + i for i in self._names_files_pickle
        )

    @property
    def usuarios(self) -> Tuple[Dict[int, Usuari]]:
        """
        Getter del atribut _usuarios.
        Returns
        -------
        Tuple[Dict[int, Usuari]]
            Indexació del objectes usuaris per facilitar accés.

        """
        return self._usuarios

    @property
    def elementos(self) -> Tuple[Dict[int, Data]]:
        """
        Getter del atribut _elementos.

        Returns
        -------
        Tuple[Dict[int, Data]]
            Indexació del objectes data per facilitar accés.

        """
        return self._elementos

    @property
    def filas(self) -> int:
        """
        Getter del atribut _filas.

        Returns
        -------
        int
            Nombre de files o nombre d'usuaris guardats en l'objecte.

        """
        return self._filas

    @property
    def columnas(self) -> int:
        """
        Getter del atribut _columnes.

        Returns
        -------
        int
            Nombre de columnes o nombre d'elements guardats en l'objecte.

        """
        return self._columnas

    def generate_training_set(self, n_first):
        temp = self._valoraciones
        self._valoraciones = lil_matrix((self._filas, self._columnas))
        self._valoraciones[:, :n_first] = temp[:, :n_first]
        self._save_pickle()
        return temp

    def _score_top_popular_items(self):
        """
        Funció que càlcula les scores de cada columna ignorant valors en 0 i
        olumnes amb menys items nonzero que _min_vots i guarda el resultat en
        l'atribut __scores_top_popular_items.

        Returns
        -------
        None.

        """
        logging.debug("Càlculant scores.")
        avg_item = lil_matrix((1, self._columnas))
        num_vots = lil_matrix((1, self._columnas), dtype=int)
        score = lil_matrix((1, self._columnas))
        # Càlcula els nombres de vots (elements no equivalents a 0) i la mija
        # (si té el nombre mínim de vots) (no contant els 0) de cada columna.
        for columna in range(self._columnas):
            num_vots[0, columna] = self._valoraciones[:, columna].count_nonzero()
            if num_vots[0, columna] >= self._min_vots:
                avg_item[0, columna] = (self._valoraciones[:, columna].sum()) / (
                    num_vots[0, columna]
                )
        logging.debug("Nombre de vots:\n\t%s", num_vots)
        logging.debug("Mitjanes:\n\t%s", avg_item)
        avg_global = (avg_item.sum()) / avg_item.count_nonzero()
        logging.debug("Mitjana global:\n\t%s", avg_global)
        # Càlcula la puntuació de cada objecte, ignorant aquells que no tenen
        # el nombre mínim de vots requerits.
        for columna in range(self._columnas):
            if num_vots[0, columna] >= self._min_vots:
                score[0, columna] = (
                    ((num_vots[0, columna]) / (num_vots[0, columna] + self._min_vots))
                    * avg_item[0, columna]
                ) + (
                    ((self._min_vots) / (num_vots[0, columna] + self._min_vots))
                    * avg_global
                )
            else:
                score[0, columna] = 0
        logging.debug("Scores:\n\t%s", score)
        #  Guarda la matriu com a atribut per reutilitzarla després i no
        # requerir tornar-la a càlcular amb un altre usuari.
        self._scores_top_popular_items = score
        if self._pickle:
            self._save_pickle()

    def top_popular_items(self, usuario: int) -> List[Tuple[Data, float]]:
        """
        Càlcula i genera una llista ordenada (de més a menys) dels elements
        que més puntuació tenen, basat en les valoracions dels altres usuaris,
        ignorat les ja valorades pel usuari donat i les que tenen menys
        valoracions que min_vots.

        Parameters
        ----------
        min_vots : int
            Quantitat mínima de vots que necessita un element per calcular la
            seva score, en comptes de ser 0.
        usuario : int
            Indicador de la fila del usuari a quí es recomanarà els elements,
            no es recomanen els elelents ja valorats per aquest.

        Returns
        -------
        List[Tuple[Data, float]]
            Llista ordenada dels elements per score, referencia al element i la
            score en questió.

        """
        logging.debug(
            "Càlcul 'top_popular_items' amb min_vots: %s i usuari: %s.",
            self._min_vots,
            usuario,
        )
        # Comprobació de que els arguments de la funció están dins del límit
        # del dataset i evitar errors no controlats.
        assert 0 <= usuario < self._filas, "Usuari fora de rang."
        assert (
            self._min_vots < self._filas
        ), "Demanat més objectes comparat que disponibles."
        # Comprova si ja existeix la matriu amb les puntuacions i si no la
        # càlcula.
        if self._scores_top_popular_items is None:
            self._score_top_popular_items()
        logging.debug("Retornant resultat.")
        # Agafa les puntuacions de les columnes no valorades pel usuari donat
        # i les ordena de major a menor puntuació, retornant l'objecte Data
        # corresponent i la puntuació que té, per després poder obtenir el
        # element al que es refereix.
        return self._scores_top_popular_items

    def _similitud_other_users_also(
        self, usuario: lil_matrix, posicio: int
    ) -> List[List[float]]:
        """
        Càlcula la similitud entre l'usuari donat i tota la resta.

        Parameters
        ----------
        usuario : lil_matrix
            Valoracions del usuari amb qui calcular la posició.
        posicio : int
            Posió a la matriu per ignorar el usuari en sí (ja que la similitud
            serà la màxima).

        Returns
        -------
        List[List[float]]
            Llista de llistes amb l'usuari i la similitud que li correspon,
            ordenada de mayor a menor similitud.

        """
        logging.debug("Càlculant similituds amb usuari:\n\t%s: %s.", posicio, usuario)
        # Com que una fila ocupa molt menys d'espai de memoria es pot
        # prescindir de la lil_matrix i utilitzar l'array per agilitar el
        # càlcul.
        user_u = usuario.toarray()
        similitudes = []
        # Càlcula la similitus entre cada usuari i el usuari donat, guardant la
        # fila de l'usuari per referencia i la similitud, per al càlcul
        # posterior, quan es troba amb el mateix usuari, asigna 0.
        for fila in range(self._filas):
            if fila != posicio:
                user_v = self._valoraciones.getrow(fila).toarray()
                similitudes.append([fila, similitud(user_u, user_v)])
            else:
                similitudes.append([fila, 0])
        logging.debug("Retornant similituds.\n\t%s", similitudes)
        # Retona el càcul de les similitus ordenades de major a menor.
        return sorted(similitudes, key=lambda x: x[1], reverse=True)

    def other_users_also(self, usuario: int) -> List[Tuple[Data, float]]:
        """
        Càlcula i genera una llista ordenada (de més a menys) dels elements
        que més puntuació tenen, basat en les valoracions dels usuaris més
        similars al usuari donat, ignorat les ja valorades pel usuari donat.

        Parameters
        ----------
        usuario : int
            Indicador de la fila del usuari a quí es recomanarà els elements,
            no es recomanen els elelents ja valorats per aquest.

        Returns
        -------
        List[Tuple[Data, float]]
           Llista ordenada dels elements per score, referencia al element i la
           score en questió.

        """
        logging.debug(
            "Càlcul 'other_users_also' amb k: %s i usuari: %s.",
            self._k_usuaris,
            usuario,
        )
        # Comprobació de que els arguments de la funció están dins del límit
        # del dataset i evitar errors no controlats.
        assert 0 <= usuario < self._filas, "Usuari fora de rang."
        assert (
            0 < self._k_usuaris < self._filas
        ), "Demanat més objectes comparats que disponibles."
        # Obté la lil_matrix unidimensional del usuari, per facilitar els
        # càlcus.
        user_u = self._valoraciones.getrow(usuario)
        # Càlcula les similituds entre tots els usuaris i l'usuari demanat i
        # agafa els k amb mayor similitud (k primers).
        k_similars = self._similitud_other_users_also(user_u, usuario)[
            : self._k_usuaris
        ]
        scores = lil_matrix((1, self._columnas))
        # Càlcula la mitja de les valoracions del k més similars usuaris
        # (ignorant les valoracions amb 0) i les afegeix a la llista de
        # reférencia i similitud.
        for i, user in enumerate(k_similars):
            k_similars[i].append(
                (self._valoraciones[user[0], :].sum())
                / (self._valoraciones[user[0], :].count_nonzero())
            )
        logging.debug("Similituds i mitjanes:\n\t%s", k_similars)
        avg_u = (user_u.sum()) / (user_u.count_nonzero())
        logging.debug("Mitjana usuari: %s", avg_u)
        # Càlcula la puntuació de cada columna, donats el k usuaris més próxims.
        for columna in range(self._columnas):
            denominador = 0
            numerador = 0
            for user in k_similars:
                numerador += user[1] * (self._valoraciones[user[0], columna] - user[2])
                denominador += user[1]
            scores[0, columna] = avg_u + ((numerador) / (denominador))
        logging.debug("Scores:\n\t%s", scores)
        logging.debug("Retornant resultat.")
        # Agafa les puntuacions de les columnes no valorades pel usuari donat
        # i les ordena de major a menor puntuació, retornant l'objecte Data
        # corresponent i la puntuació que té, per després poder obtenir el
        # element al que es refereix.
        return scores

    def _tfidf_matrix(self):
        item_features = [
            self._elementos[0][i].caract_to_str() for i in range(self._columnas)
        ]
        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(item_features).toarray()
        return tfidf_matrix

    def _perfil_usuari(self, usuari, tfidf_matrix):
        valoraciones = self._valoraciones.getrow(usuari).toarray()
        return valoraciones.dot(tfidf_matrix) / valoraciones.sum()

    def because_you_liked(self, usuario: int):
        tfidf_matrix = self._tfidf_matrix()
        perfil_usuari = self._perfil_usuari(usuario, tfidf_matrix)
        tfidf_matrix = tfidf_matrix.reshape(
            (tfidf_matrix.shape[1], tfidf_matrix.shape[0])
        )
        puntuaciones = perfil_usuari.dot(tfidf_matrix)
        p = np.sqrt(np.square(perfil_usuari).sum())
        sumatorio = np.sqrt((np.square(tfidf_matrix)).sum(0))
        return puntuaciones / (p * sumatorio) * self._max_pun

    @abstractmethod
    def read_data(self):
        """
        Funció abstracta per llegir les bases de dades, necessita ser
        implemetada en cada clase derivada.

        Raises
        ------
        NotImplementedError
            Aquest métode depen del format del conjunt de dades, per tant s'ha
            de programar un lector inicial per a cada clase.

        Returns
        -------
        None.

        """
        raise NotImplementedError()

    def _save_pickle(self):
        """
        Guarda els atributs de la clase en un arxiu binari de lectura més
        ràpida que els arxius csv.

        Returns
        -------
        None.

        """
        logging.debug("_save_pickle Dataset-subclass object")
        if self._directory + "_pickle" not in os.listdir("."):
            os.mkdir("./" + self._directory + "_pickle")
        with open(self._names_files_pickle[0], "wb") as fitxer_0, open(
            self._names_files_pickle[1], "wb"
        ) as fitxer_1, open(self._names_files_pickle[2], "wb") as fitxer_2, open(
            self._names_files_pickle[3], "wb"
        ) as fitxer_3, open(
            self._names_files_pickle[4], "wb"
        ) as fitxer_4, open(
            self._names_files_pickle[5], "wb"
        ) as fitxer_5, open(
            self._names_files_pickle[6], "wb"
        ) as fitxer_6, open(
            self._names_files_pickle[7], "wb"
        ) as fitxer_7, open(
            self._names_files_pickle[8], "wb"
        ) as fitxer_8, open(
            self._names_files_pickle[9], "wb"
        ) as fitxer_9:
            pickle.dump(self._valoraciones, fitxer_0)
            pickle.dump(self._elementos[0], fitxer_1)
            pickle.dump(self._elementos[1], fitxer_2)
            pickle.dump(self._elementos[2], fitxer_3)
            pickle.dump(self._usuarios[0], fitxer_4)
            pickle.dump(self._usuarios[1], fitxer_5)
            pickle.dump(self._filas, fitxer_6)
            pickle.dump(self._columnas, fitxer_7)
            pickle.dump(self._scores_top_popular_items, fitxer_8)
            pickle.dump(self._min_vots, fitxer_9)

    def _load_pickle(self):
        """
        Carrega els atributs de la clase des de un arxiu binari de lectura més
        ràpida que els arxius csv.

        Returns
        -------
        None.

        """
        logging.debug("_load_pickle Dataset-subclass object")
        with open(self._names_files_pickle[0], "rb") as fitxer_0, open(
            self._names_files_pickle[1], "rb"
        ) as fitxer_1, open(self._names_files_pickle[2], "rb") as fitxer_2, open(
            self._names_files_pickle[3], "rb"
        ) as fitxer_3, open(
            self._names_files_pickle[4], "rb"
        ) as fitxer_4, open(
            self._names_files_pickle[5], "rb"
        ) as fitxer_5, open(
            self._names_files_pickle[6], "rb"
        ) as fitxer_6, open(
            self._names_files_pickle[7], "rb"
        ) as fitxer_7, open(
            self._names_files_pickle[8], "rb"
        ) as fitxer_8, open(
            self._names_files_pickle[9], "rb"
        ) as fitxer_9:
            self._valoraciones = pickle.load(fitxer_0)
            self._elementos = (
                pickle.load(fitxer_1),
                pickle.load(fitxer_2),
                pickle.load(fitxer_3),
            )
            self._usuarios = (pickle.load(fitxer_4), pickle.load(fitxer_5))
            self._filas = pickle.load(fitxer_6)
            self._columnas = pickle.load(fitxer_7)
            self._scores_top_popular_items = pickle.load(fitxer_8)
            self._min_vots = pickle.load(fitxer_9)

    def to_data_object(self, scores: lil_matrix, usuario: int):
        return [
            (self._elementos[0][i], scores[0, i])
            for i in scores.nonzero()[1]
            if (
                i not in list(self._valoraciones.getrow(usuario).nonzero()[1])
                and not np.isnan(scores[0, i])
            )
        ]
