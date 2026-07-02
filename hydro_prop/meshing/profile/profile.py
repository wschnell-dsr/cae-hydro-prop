#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import numpy as np


class Profile(ABC):
    _X_NORM_RANGE: tuple[float, float] = (0.0, 1.0)

    def __init__(self):
        pass

    @property
    def norm_range(self) -> tuple[float, float]:
        return self._X_NORM_RANGE

    def in_norm_range(self, arg_x: float) -> bool:
        if arg_x < self._X_NORM_RANGE[0] or arg_x > self._X_NORM_RANGE[1]:
            return False
        return True

    @abstractmethod
    def norm_camber_y(self, arg_x: float) -> float:
        pass

    @abstractmethod
    def norm_camber_dydx(self, arg_x: float) -> float:
        pass

    @abstractmethod
    def norm_camber_dydx2(self, arg_x: float) -> float:
        pass

    @abstractmethod
    def norm_thickness_y(self, arg_x: float) -> float:
        pass

    @abstractmethod
    def norm_camber_line(self) -> np.ndarray:
        pass

    @abstractmethod
    def norm_thickness_distribution(self) -> np.ndarray:
        pass

    @abstractmethod
    def norm_profile_line(self) -> tuple[np.ndarray, np.ndarray]:
        pass

    def profile_line(self, arg_length: float, alpha_deg=0.0) -> tuple[np.ndarray, np.ndarray]:
        norm = self.norm_profile_line()
        xup = norm[0][0] * arg_length
        yup = norm[0][1] * arg_length
        xlw = norm[1][0] * arg_length
        ylw = norm[1][1] * arg_length
        tmp_result = (xup, yup), (xlw, ylw)
        if alpha_deg != 0.0:
            alpha_rad = np.deg2rad(-alpha_deg)

            cos_alpha = np.cos(alpha_rad)
            sin_alpha = np.sin(alpha_rad)

            xup_rotated = xup * cos_alpha - yup * sin_alpha
            yup_rotated = xup * sin_alpha + yup * cos_alpha
            xlw_rotated = xlw * cos_alpha - ylw * sin_alpha
            ylw_rotated = xlw * sin_alpha + ylw * cos_alpha
            tmp_result = (xup_rotated, yup_rotated), (xlw_rotated, ylw_rotated)
        return tmp_result

    def camber_line(self, arg_length: float, alpha_deg=0.0) -> np.ndarray:
        norm = self.norm_camber_line()
        x = norm[0] * arg_length
        y = norm[1] * arg_length
        tmp_result = (x, y)
        if alpha_deg != 0.0:
            alpha_rad = np.deg2rad(-alpha_deg)

            cos_alpha = np.cos(alpha_rad)
            sin_alpha = np.sin(alpha_rad)

            x_rotated = x * cos_alpha - y * sin_alpha
            y_rotated = x * sin_alpha + y * cos_alpha
            tmp_result = (x_rotated, y_rotated)
        return tmp_result

