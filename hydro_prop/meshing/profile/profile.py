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

    def profile_line(self, arg_length: float, alpha_deg=0.0, p_rot: tuple[float, float] = (0.0, 0.0)) -> tuple[np.ndarray, np.ndarray]:
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

            xup_rotated = (xup - p_rot[0]) * cos_alpha - (yup - p_rot[1]) * sin_alpha + p_rot[0]
            yup_rotated = (xup - p_rot[0]) * sin_alpha + (yup - p_rot[1]) * cos_alpha + p_rot[1]
            xlw_rotated = (xlw - p_rot[0]) * cos_alpha - (ylw - p_rot[1]) * sin_alpha + p_rot[0]
            ylw_rotated = (xlw - p_rot[0]) * sin_alpha + (ylw - p_rot[1]) * cos_alpha + p_rot[1]
            tmp_result = (xup_rotated, yup_rotated), (xlw_rotated, ylw_rotated)
        return tmp_result

    def camber_line(self, arg_length: float, alpha_deg=0.0, p_rot: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
        norm = self.norm_camber_line()
        x = norm[0] * arg_length
        y = norm[1] * arg_length
        tmp_result = (x, y)
        if alpha_deg != 0.0:
            alpha_rad = np.deg2rad(-alpha_deg)

            cos_alpha = np.cos(alpha_rad)
            sin_alpha = np.sin(alpha_rad)

            x_rotated = (x - p_rot[0]) * cos_alpha - (y - p_rot[1]) * sin_alpha + p_rot[0]
            y_rotated = (x - p_rot[0]) * sin_alpha + (y - p_rot[1]) * cos_alpha + p_rot[1]
            tmp_result = (x_rotated, y_rotated)
        return tmp_result

