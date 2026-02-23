""" Módulo de género del docente. """

from enum import Enum


class Gender(str, Enum):
    """ Enum para el género del docente. """
    MASCULINO = "M"
    FEMENINO = "F"
