# -*- coding: utf-8 -*-
"""
Created on Mon May  9 00:07:11 2022

@author: JoelT
"""

with open("user_ratings.csv", "r") as file1, open("user_ratings1.csv", "w") as file2:
    file2.writelines(file1.readlines()[:1713])
