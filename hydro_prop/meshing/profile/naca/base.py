#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import numpy as np
from enum import IntEnum

from abc import ABC, abstractmethod

from ..profile import Profile


class NACASeries(IntEnum):
    NACA_4 = 4
    NACA_5 = 5
    NACA_6 = 6
    UNKNOWN = 255


def profile_code_series(arg_profile_code: str) -> NACASeries:
    if len(arg_profile_code) == 4:
        return NACASeries.NACA_4
    elif len(arg_profile_code) == 5:
        return NACASeries.NACA_5
    elif len(arg_profile_code) == 6 or (len(arg_profile_code) == 7 and "-" in arg_profile_code):
        return NACASeries.NACA_6
    else:
        return NACASeries.UNKNOWN


class NACAProfile(Profile, ABC):
    _logger: logging.Logger
    __profile_code: str
    _max_camber: float
    """Max camber relative"""
    _camber_position: float
    """Max camber position 0.0 - 1.0"""
    _max_thickness: float
    """Max thickness   0.0 - 1.0"""
    _symmetric: bool
    _norm_x_distribution: np.ndarray

    _DEFAULT_N_POINTS: int = 100

    def __init__(self, arg_profile_code: str):
        super().__init__()
        self._logger = logging.getLogger("hydro_prop.meshing.profile.naca")
        self.__profile_code = arg_profile_code
        self._max_camber = 0.0
        self._camber_position = 0.0
        self._max_thickness = 0.0
        self._symmetric = True
        self._norm_x_distribution = np.linspace(self.norm_range[0], self.norm_range[1], self._DEFAULT_N_POINTS)

    @property
    @abstractmethod
    def series(self) -> NACASeries:
        pass

    @property
    def symmetric(self) -> NACASeries:
        return self._symmetric

    @property
    def profile_code(self) -> str:
        return self.__profile_code

    @abstractmethod
    def _parse_profile_code(self):
        pass

    def calc_norm_x_distribution(self, arg_n_pts: int = 0):
        tmp_n_points = self._DEFAULT_N_POINTS
        if arg_n_pts >= 5:
            tmp_n_points = arg_n_pts
        self._norm_x_distribution = np.linspace(self.norm_range[0], self.norm_range[1], tmp_n_points)

    def norm_thickness_y(self, arg_x: float) -> float:
        tmp_y = 0.0
        if arg_x < 1.0:
            a0, a1, a2, a3, a4 = 1.4845, -0.630, -1.758, 1.4215, -0.5075
            tmp_y = 2.0 * self._max_thickness * (a0 * np.sqrt(arg_x) + a1 * arg_x + a2 * arg_x**2 + a3 * arg_x**3 + a4 * arg_x**4)
        return tmp_y

    def norm_thickness_dydx(self, arg_x: float) -> float:
        a0, a1, a2, a3, a4 = 1.4845, -0.630, -1.758, 1.4215, -0.5075
        tmp_y = 2.0 * self._max_thickness * (0.5 * a0 / np.sqrt(max(arg_x, 1e-10)) + a1 + 2.0 * a2 * arg_x + 3.0 * a3 * arg_x**2 + 4.0 * a4 * arg_x**3)
        return tmp_y

    def norm_thickness_distribution(self) -> np.ndarray:
        tmp_y = np.array([self.norm_thickness_y(x) for x in self._norm_x_distribution])
        return tmp_y

    def norm_camber_line(self) -> np.ndarray:
        tmp_x = self._norm_x_distribution
        tmp_y = np.array([self.norm_camber_y(x) for x in self._norm_x_distribution])
        return (tmp_x, tmp_y)

    def norm_profile_line(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculates relative x-y-contours
        """
        x_c, y_c = self.norm_camber_line()
        self._logger.debug(f"Norm camber line of profile {self.profile_code}")
        self._logger.debug(x_c)
        self._logger.debug(y_c)
        y_t = self.norm_thickness_distribution()

        if self.symmetric:
            # Symmetrisches Profil
            x_upper = x_c
            y_upper = y_t / 2.0
            x_lower = x_c
            y_lower = -y_t / 2.0
        else:
            # Gewölbtes Profil
            theta = np.arctan(np.gradient(y_c, x_c))
            x_upper = x_c - y_t * np.sin(theta) / 2
            y_upper = y_c + y_t * np.cos(theta) / 2
            x_lower = x_c + y_t * np.sin(theta) / 2
            y_lower = y_c - y_t * np.cos(theta) / 2

        return (x_upper, y_upper), (x_lower, y_lower)


