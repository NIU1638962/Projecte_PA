# -*- coding: utf-8 -*-
"""
Created on Sun May  8 12:20:25 2022

@author: Joel Tapia Salvador (1638962)
"""

import unittest
import numpy as np
from películes import Pelicules


DIRECTORY = "test_dataset"
NAMES_FILES = ("movies_test.csv", "ratings_test.csv")


class TestPelicules(unittest.TestCase):
    def setUp(self):
        self.dataset = Pelicules(DIRECTORY, NAMES_FILES)
        self.dataset.read_data()
        self.dataset._min_vots = 4
        self.dataset._score_top_popular_items()

    def test_elementos_0(self):
        self.assertEqual(list(self.dataset.elementos[0].keys()), list(range(6)))

    def test_elementos_1(self):
        self.assertEqual(
            list(self.dataset.elementos[1].keys()),
            [
                "Toy Story (1995)",
                "Jumanji (1995)",
                "Grumpier Old Men (1995)",
                "Waiting to Exhale (1995)",
                "Father of the Bride Part II (1995)",
                "Heat (1995)",
            ],
        )

    def test_elementos_2(self):
        self.assertEqual(
            list(self.dataset.elementos[2].keys()), [str(i) for i in range(1, 7)]
        )

    def test_elementos(self):
        self.assertEqual(
            [self.dataset.elementos[0][i] for i in range(6)],
            [
                self.dataset.elementos[1][self.dataset.elementos[0][i].titol]
                for i in range(6)
            ],
        )
        self.assertEqual(
            [self.dataset.elementos[0][i] for i in range(6)],
            [
                self.dataset.elementos[2][self.dataset.elementos[0][i].identificador]
                for i in range(6)
            ],
        )

    def test_elementos_carcte(self):
        self.assertEqual(
            [
                "|".join(self.dataset.elementos[0][i].caracteristicas["genres"])
                for i in range(6)
            ],
            [
                "Adventure|Animation|Children|Comedy|Fantasy",
                "Adventure|Children|Fantasy",
                "Comedy|Romance",
                "Comedy|Drama|Romance",
                "Comedy",
                "Action|Crime|Thriller",
            ],
        )

    def test_usuaris_0(self):
        self.assertEqual(list(self.dataset.usuarios[0].keys()), list(range(6)))

    def test_usuaris_1(self):
        self.assertEqual(
            list(self.dataset.usuarios[1].keys()), [str(i) for i in range(1, 7)]
        )

    def test_usuaris(self):
        self.assertEqual(
            [self.dataset.usuarios[0][i] for i in range(6)],
            [
                self.dataset.usuarios[1][self.dataset.usuarios[0][i].nom]
                for i in range(6)
            ],
        )

    def test_valoracions(self):
        self.assertTrue(
            np.all(
                self.dataset._valoraciones
                == np.array(
                    [
                        [5.0, 4.0, 3.0, 0, 0, 4.0],
                        [5.0, 5.0, 0, 0, 0, 5.0],
                        [0, 3.6, 0, 4.5, 5.0, 0],
                        [0, 0, 0, 3.8, 5.0, 4.0],
                        [3.6, 4.0, 2.5, 0, 0, 0],
                        [5.0, 2.9, 0, 0, 0, 3.0],
                    ]
                )
            ),
        )

    def test__score_top_popular_items(self):
        self.assertTrue(
            np.all(
                self.dataset._scores_top_popular_items
                == np.array(
                    [4.416666666666667, 4.025925925925925, 0, 0, 0, 4.091666666666667]
                )
            )
        )

    def test_top_popular_items(self):
        self.assertEqual(self.dataset.top_popular_items(4, 0), [])
        self.assertEqual(self.dataset.top_popular_items(4, 1), [])
        self.assertEqual(
            self.dataset.top_popular_items(4, 2),
            [
                (self.dataset.elementos[0][0], 4.416666666666667),
                (self.dataset.elementos[0][5], 4.091666666666667),
            ],
        )
        self.assertEqual(
            self.dataset.top_popular_items(4, 3),
            [
                (self.dataset.elementos[0][0], 4.416666666666667),
                (self.dataset.elementos[0][1], 4.025925925925925),
            ],
        )
        self.assertEqual(
            self.dataset.top_popular_items(4, 4),
            [(self.dataset.elementos[0][5], 4.091666666666667)],
        )
        self.assertEqual(self.dataset.top_popular_items(4, 5), [])

    def test__similitud_other_users_also(self):
        self.assertEqual(
            self.dataset._similitud_other_users_also(
                self.dataset._valoraciones.getrow(0), 0
            ),
            [
                [2, 1.0],
                [3, 1.0],
                [1, 0.9941348467724341],
                [4, 0.9890769524338549],
                [5, 0.9884727589141507],
                [0, 0],
            ],
        )
        self.assertEqual(
            self.dataset._similitud_other_users_also(
                self.dataset._valoraciones.getrow(1), 1
            ),
            [
                [2, 1.0],
                [3, 1.0],
                [4, 0.9986178293325096],
                [0, 0.9941348467724341],
                [5, 0.9663439552179203],
                [1, 0],
            ],
        )
        self.assertEqual(
            self.dataset._similitud_other_users_also(
                self.dataset._valoraciones.getrow(2), 2
            ),
            [[0, 1.0], [1, 1.0], [4, 1.0], [5, 1.0], [3, 0.9965620640298236], [2, 0]],
        )
        self.assertEqual(
            self.dataset._similitud_other_users_also(
                self.dataset._valoraciones.getrow(3), 3
            ),
            [[0, 1.0], [1, 1.0], [5, 1.0], [2, 0.9965620640298236], [3, 0], [4, 0]],
        )
        self.assertEqual(
            self.dataset._similitud_other_users_also(
                self.dataset._valoraciones.getrow(4), 4
            ),
            [
                [2, 1.0],
                [1, 0.9986178293325096],
                [0, 0.9890769524338549],
                [5, 0.9515994765632942],
                [3, 0],
                [4, 0],
            ],
        )
        self.assertEqual(
            self.dataset._similitud_other_users_also(
                self.dataset._valoraciones.getrow(5), 5
            ),
            [
                [2, 1.0],
                [3, 1.0],
                [0, 0.9884727589141507],
                [1, 0.9663439552179203],
                [4, 0.9515994765632942],
                [5, 0],
            ],
        )

    def test_other_users_also(self):
        self.assertEqual(
            self.dataset.other_users_also(1, 0),
            [
                (self.dataset.elementos[0][4], 4.633333333333334),
                (self.dataset.elementos[0][3], 4.133333333333334),
            ],
        )
        self.assertEqual(
            self.dataset.other_users_also(1, 1),
            [
                (self.dataset.elementos[0][4], 5.633333333333334),
                (self.dataset.elementos[0][3], 5.133333333333334),
                (self.dataset.elementos[0][2], 0.6333333333333337),
            ],
        )
        self.assertEqual(
            self.dataset.other_users_also(1, 2),
            [
                (self.dataset.elementos[0][0], 5.366666666666666),
                (self.dataset.elementos[0][5], 4.366666666666666),
                (self.dataset.elementos[0][2], 3.3666666666666663),
            ],
        )
        self.assertEqual(
            self.dataset.other_users_also(1, 3),
            [
                (self.dataset.elementos[0][0], 5.266666666666667),
                (self.dataset.elementos[0][1], 4.266666666666667),
                (self.dataset.elementos[0][2], 3.2666666666666666),
            ],
        )
        self.assertEqual(
            self.dataset.other_users_also(1, 4),
            [
                (self.dataset.elementos[0][4], 4.0),
                (self.dataset.elementos[0][3], 3.5000000000000004),
                (self.dataset.elementos[0][5], -0.9999999999999996),
            ],
        )
        self.assertEqual(
            self.dataset.other_users_also(1, 5),
            [
                (self.dataset.elementos[0][4], 4.2666666666666675),
                (self.dataset.elementos[0][3], 3.766666666666667),
                (self.dataset.elementos[0][2], -0.733333333333333),
            ],
        )

    def test_caract_to_str(self):
        self.assertEqual(
            [
                self.dataset.elementos[0][i].caract_to_str()
                for i in range(self.dataset.columnas)
            ],
            [
                "Adventure|Animation|Children|Comedy|Fantasy",
                "Adventure|Children|Fantasy",
                "Comedy|Romance",
                "Comedy|Drama|Romance",
                "Comedy",
                "Action|Crime|Thriller",
            ],
        )

    def test__tfidf_matrix(self):
        self.assertTrue(
            np.all(
                self.dataset._tfidf_matrix()
                == np.array(
                    [
                        [
                            0.0,
                            0.44674150776102867,
                            0.5447972125961776,
                            0.44674150776102867,
                            0.32320592952117017,
                            0.0,
                            0.0,
                            0.44674150776102867,
                            0.0,
                            0.0,
                        ],
                        [
                            0.0,
                            0.5773502691896257,
                            0.0,
                            0.5773502691896257,
                            0.0,
                            0.0,
                            0.0,
                            0.5773502691896257,
                            0.0,
                            0.0,
                        ],
                        [
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.5861569567966913,
                            0.0,
                            0.0,
                            0.0,
                            0.8101975203608325,
                            0.0,
                        ],
                        [
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.4169638817420929,
                            0.0,
                            0.702835993333765,
                            0.0,
                            0.5763355687419489,
                            0.0,
                        ],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [
                            0.5773502691896257,
                            0.0,
                            0.0,
                            0.0,
                            0.0,
                            0.5773502691896257,
                            0.0,
                            0.0,
                            0.0,
                            0.5773502691896257,
                        ],
                    ]
                )
            )
        )

    def test__perfil_usuari(self):
        tfidf_matrix = self.dataset._tfidf_matrix()
        self.assertTrue(
            np.all(
                self.dataset._perfil_usuari(0, tfidf_matrix)
                == np.array(
                    [
                        0.14433756729740643,
                        0.2839442884727279,
                        0.1702491289363055,
                        0.2839442884727279,
                        0.2109062823747453,
                        0.14433756729740643,
                        0.0,
                        0.2839442884727279,
                        0.1519120350676561,
                        0.14433756729740643,
                    ]
                )
            )
        )
        self.assertTrue(
            np.all(
                self.dataset._perfil_usuari(1, tfidf_matrix)
                == np.array(
                    [
                        0.19245008972987523,
                        0.34136392565021817,
                        0.18159907086539254,
                        0.34136392565021817,
                        0.10773530984039006,
                        0.19245008972987523,
                        0.0,
                        0.34136392565021817,
                        0.0,
                        0.19245008972987523,
                    ]
                )
            )
        )
        self.assertTrue(
            np.all(
                self.dataset._perfil_usuari(2, tfidf_matrix)
                == np.array(
                    [
                        0.0,
                        0.15866114267806508,
                        0.0,
                        0.15866114267806508,
                        0.5249112570869785,
                        0.0,
                        0.24143221145052995,
                        0.15866114267806508,
                        0.19797786712509696,
                        0.0,
                    ]
                )
            )
        )
        self.assertTrue(
            np.all(
                self.dataset._perfil_usuari(3, tfidf_matrix)
                == np.array(
                    [
                        0.18042195912175804,
                        0.0,
                        0.0,
                        0.0,
                        0.5144111523921838,
                        0.18042195912175804,
                        0.20865443552096147,
                        0.0,
                        0.17109962197026604,
                        0.18042195912175804,
                    ]
                )
            )
        )
        self.assertTrue(
            np.all(
                self.dataset._perfil_usuari(4, tfidf_matrix)
                == np.array(
                    [
                        0.0,
                        0.3878881687820006,
                        0.1941851450837861,
                        0.3878881687820006,
                        0.2602904691354397,
                        0.0,
                        0.0,
                        0.3878881687820006,
                        0.20054394068337436,
                        0.0,
                    ]
                )
            )
        )
        self.assertTrue(
            np.all(
                self.dataset._perfil_usuari(5, tfidf_matrix)
                == np.array(
                    [
                        0.15890374381365846,
                        0.3585342494912897,
                        0.24990697825512734,
                        0.3585342494912897,
                        0.1482596006977845,
                        0.15890374381365846,
                        0.0,
                        0.3585342494912897,
                        0.0,
                        0.15890374381365846,
                    ]
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
