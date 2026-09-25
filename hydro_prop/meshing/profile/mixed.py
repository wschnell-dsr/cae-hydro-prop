#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import numpy as np
from enum import IntEnum

from typing import TypedDict, TypeAlias, Union

from ..profile import Profile


class CamberLineType(IntEnum):
    ZERO = 0
    PARABOLIC = 1


class CamberLineCnf(TypedDict):
    camber_line_type: str


class CamberdLineParabolicCnf(CamberLineCnf):
    camber: float


CamberLineCnfVariant: TypeAlias = Union[None, CamberLineCnf, CamberdLineParabolicCnf]


class ThicknessDistributionType(IntEnum):
    PARABOLIC = 0
    ELLIPTIC = 1


class ThicknessDistributionCnf(TypedDict):
    thickness_distribution_type: str


class ThicknessDistributionParabolicCnf(ThicknessDistributionCnf):
    max_thickness: float


class ThicknessDistributionEllipticCnf(ThicknessDistributionCnf):
    max_thickness: float


ThicknessDistributionCnfVariant: TypeAlias = Union[None, ThicknessDistributionCnf, ThicknessDistributionParabolicCnf, ThicknessDistributionEllipticCnf]


class MixedProfileCnf(TypedDict):
    camber_line_cnf: CamberLineCnfVariant
    thickness_distribution_cnf: ThicknessDistributionCnfVariant


class MixedProfile(Profile):
    _logger: logging.Logger
    _norm_x_distribution: np.ndarray
    __profile_cnf: MixedProfileCnf

    _DEFAULT_N_POINTS: int = 100

    def __init__(self, arg_profile_cnf: MixedProfileCnf):
        super().__init__()
        self._logger = logging.getLogger("hydro_prop.meshing.profile.mixed")
        self.__profile_cnf = arg_profile_cnf
        self._norm_x_distribution = np.linspace(self.norm_range[0], self.norm_range[1], self._DEFAULT_N_POINTS)

    def calc_norm_x_distribution(self, arg_n_pts: int = 0):
        tmp_n_points = self._DEFAULT_N_POINTS
        if arg_n_pts >= 5:
            tmp_n_points = arg_n_pts
        self._norm_x_distribution = np.linspace(self.norm_range[0], self.norm_range[1], tmp_n_points)

    def norm_thickness_y(self, arg_x: float) -> float:
        tmp_y = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.__profile_cnf["thickness_distribution_cnf"]["thickness_distribution_type"] == ThicknessDistributionType.PARABOLIC.name:
            tmp_y = -4.0 * self.__profile_cnf["thickness_distribution_cnf"]["max_thickness"] * (arg_x - 1.0) * arg_x
        elif self.__profile_cnf["thickness_distribution_cnf"]["thickness_distribution_type"] == ThicknessDistributionType.ELLIPTIC.name:
            if arg_x < 1e-5 or arg_x > 1.0 - 1e-5:
                tmp_y = 0
            else:
                tmp_y = self.__profile_cnf["thickness_distribution_cnf"]["max_thickness"] * np.sqrt(1.0 - ((arg_x - 0.5)**2 / 0.25))
        return tmp_y

    def norm_thickness_dydx(self, arg_x: float) -> float:
        # not used
        tmp_dydx = 0
        if self.__profile_cnf["thickness_distribution_cnf"]["thickness_distribution_type"] == ThicknessDistributionType.PARABOLIC.name:
            tmp_dydx = self.__profile_cnf["thickness_distribution_cnf"]["max_thickness"]
        return tmp_dydx

    def norm_thickness_distribution(self) -> np.ndarray:
        tmp_y = np.array([self.norm_thickness_y(x) for x in self._norm_x_distribution])
        return tmp_y

    def norm_camber_y(self, arg_x: float) -> float:
        tmp_y = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.__profile_cnf["camber_line_cnf"]["camber_line_type"] == CamberLineType.ZERO.name:
            tmp_y = 0.0
        elif self.__profile_cnf["camber_line_cnf"]["camber_line_type"] == CamberLineType.PARABOLIC.name:
            tmp_y = - 0.5 * self.__profile_cnf["camber_line_cnf"]["camber"] * (arg_x**2 - arg_x)
        return tmp_y

    def norm_camber_dydx(self, arg_x: float) -> float:
        # not used
        tmp_dydx = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.__profile_cnf["camber_line_cnf"]["camber_line_type"] == CamberLineType.ZERO.name:
            tmp_dydx = 0.0
        elif self.__profile_cnf["camber_line_cnf"]["camber_line_type"] == CamberLineType.PARABOLIC.name:
            tmp_dydx = - 0.5 * self.__profile_cnf["camber_line_cnf"]["camber"] * (2.0*arg_x - 1.0)
        return tmp_dydx

    def norm_camber_dydx2(self, arg_x: float) -> float:
        # not used
        tmp_dydx2 = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.__profile_cnf["camber_line_cnf"]["camber_line_type"].name == CamberLineType.ZERO.name:
            tmp_dydx2 = 0.0
        elif self.__profile_cnf["camber_line_cnf"]["camber_line_type"].name == CamberLineType.PARABOLIC.name:
            tmp_dydx2 = - self.__profile_cnf["camber_line_cnf"]["camber"]
        return tmp_dydx2

    def norm_camber_line(self) -> np.ndarray:
        tmp_x = self._norm_x_distribution
        tmp_y = np.array([self.norm_camber_y(x) for x in self._norm_x_distribution])
        return (tmp_x, tmp_y)

    def norm_profile_line(self) -> tuple[np.ndarray, np.ndarray]:
        x_c, y_c = self.norm_camber_line()
        y_t = self.norm_thickness_distribution()

        if np.all(y_c == 0.0):
            x_upper = x_c
            y_upper = y_t / 2.0
            x_lower = x_c
            y_lower = -y_t / 2.0
        else:
            theta = np.arctan(np.gradient(y_c, x_c))
            x_upper = x_c - y_t * np.sin(theta) / 2
            y_upper = y_c + y_t * np.cos(theta) / 2
            x_lower = x_c + y_t * np.sin(theta) / 2
            y_lower = y_c - y_t * np.cos(theta) / 2
        return (x_upper, y_upper), (x_lower, y_lower)


