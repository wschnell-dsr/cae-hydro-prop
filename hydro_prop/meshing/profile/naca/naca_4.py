#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import NACAProfile


class NACA4Profile(NACAProfile):

    def __init__(self, arg_profile_code: str):
        super().__init__(arg_profile_code)

        self._parse_profile_code()

    @property
    def series(self) -> int:
        return 4

    def _parse_profile_code(self):
        if len(self.profile_code) == 4:
            self._max_camber = 0.01 * int(self.profile_code[0])
            self._camber_position = 0.1 * int(self.profile_code[1])
            self._max_thickness = 0.01 * int(self.profile_code[2:])
            self._symmetric = (self._max_camber == 0.0)
            if self._max_camber > 0 and self._camber_position > 0:
                pass
            elif self._max_camber <= 0 and self._camber_position <= 0:
                pass
            else:
                self._max_camber = 0.0
                self._camber_position = 0.0
                raise ValueError("NACA-Profilcode inconsitant related to camber")
            self._logger.debug(f"Parsed profile code {self.profile_code}")
            self._logger.debug(f"max_camber {self._max_camber}")
            self._logger.debug(f"camber_position {self._camber_position}")
            self._logger.debug(f"max_thickness {self._max_thickness}")
            self._logger.debug(f"symmetric {self._symmetric}")
        else:
            raise ValueError("NACA-Profilcode has not 4 digits")

    def norm_camber_y(self, arg_x: float) -> float:
        tmp_y = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        else:
            """
            y_{c}=m/p^2*(2px-x^2)                  for 0<x<p
            y_{c}=m/(1-p)^2 * ()(1-2p)^2+2px -x^2) for p<x<1
            """
            if arg_x <= self._camber_position:
                tmp_y = (self._max_camber / (self._camber_position ** 2)) * (2 * self._camber_position * arg_x - arg_x ** 2)
            else:
                tmp_y = (self._max_camber / ((1 - self._camber_position) ** 2)) * ((1 - 2 * self._camber_position) + 2 * self._camber_position * arg_x - arg_x**2)
        return tmp_y

    def norm_camber_dydx(self, arg_x: float) -> float:
        tmp_dydx = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        else:
            """
            y_{c}=m/p^2*(2p-2*x)                  for 0<x<p
            y_{c}=m/(1-p)^2 * ()(1-2p)^2+2px -2*x) for p<x<1
            """
            if arg_x <= self._camber_position:
                tmp_dydx = (self._max_camber / (self._camber_position ** 2)) * (2.0 * self._camber_position - 2.0 * arg_x)
            else:
                tmp_dydx = 2.0 * self._camber_position - 2.0 * arg_x
        return tmp_dydx

    def norm_camber_dydx2(self, arg_x: float) -> float:
        tmp_dydx2 = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        else:
            if arg_x <= self._camber_position:
                tmp_dydx2 = -2.0 * (self._max_camber / (self._camber_position ** 2))
            else:
                tmp_dydx2 = - 2.0
        return tmp_dydx2


