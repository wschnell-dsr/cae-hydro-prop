#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import NACAProfile


class NACA5Profile(NACAProfile):
    __design_lift_coefficient: float
    __reflex: int
    __r: float
    __k1: float
    __k1_k2: float

    def __init__(self, arg_profile_code: str):
        super().__init__(arg_profile_code)

        self._parse_profile_code()

    @property
    def series(self) -> int:
        return 5

    def _parse_profile_code(self):
        if len(self.profile_code) == 5:
            self.__design_lift_coefficient = 0.15 * int(self.profile_code[0])
            self._camber_position = 0.05 * int(self.profile_code[1])
            self.__reflex = int(self.profile_code[2])
            self._max_thickness = 0.01 * int(self.profile_code[3:])
            self._symmetric = False

            if self.__reflex == 0:
                # STANDARD (NON-REFLEXED) CAMBER LINE
                # This uses a standard camber line equation
                p = self._camber_position

                # Calculate r (related to maximum camber position)
                # Polynomial interpolation formula (3rd degree):
                # r = 3.333...×p³ + 0.700...×p² + 1.196...×p - 0.003...
                self.__r = (3.33333333333212 * p**3 + 0.700000000000909 * p**2 + 1.19666666666638 * p - 0.00399999999996247)

                # Calculate k1 (camber scaling parameter)
                # Polynomial interpolation formula (4th degree):
                # k1 = 1514933.333...×p⁴ - 1087744.000...×p³ + 286455.266...×p² - 32968.470...×p + 1420.185...
                self.__k1 = (1514933.33335235 * p**4 - 1087744.00001147 * p**3 + 286455.266669048 * p**2 - 32968.4700001967 * p + 1420.18500000524)
                # Not used for non reflecting
                self.__k2_k1 = 0.0

            elif self.__reflex == 1:
                # REFLEXED CAMBER LINE
                # This uses a reflexed (curved-up) camber line for improved aerodynamics
                p = self._camber_position

                # Calculate r (related to maximum camber position for reflexed line)
                # Polynomial interpolation formula (3rd degree):
                # r = 10.666...×p³ - 2.000...×p² + 1.733...×p - 0.034...
                self.__r = (10.6666666666861 * p**3 - 2.00000000001601 * p**2 + 1.73333333333684 * p - 0.0340000000002413)

                # Calculate k1 (camber scaling parameter for reflexed line)
                # Polynomial interpolation formula (3rd degree):
                # k1 = -27973.333...×p³ + 17972.800...×p² - 3888.406...×p + 289.076...
                self.__k1 = (-27973.3333333385 * p**3 + 17972.8000000027 * p**2 - 3888.40666666711 * p + 289.076000000022)

                # Calculate k2/k1 ratio (additional parameter for reflexed camber line)
                # Polynomial interpolation formula (3rd degree):
                # k2/k1 = 85.527...×p³ - 34.982...×p² + 4.803...×p - 0.215...
                self.__k2_k1 = (85.5279999999984 * p**3 - 34.9828000000004 * p**2 + 4.80324000000028 * p - 0.21526000000003)
            self._logger.debug(f"Parsed profile code {self.profile_code}")
            self._logger.debug(f"max_camber {self._max_camber}")
            self._logger.debug(f"camber_position {self._camber_position}")
            self._logger.debug(f"max_thickness {self._max_thickness}")
            self._logger.debug(f"symmetric {self._symmetric}")
            self._logger.debug(f"design_lift_coefficient {self.__design_lift_coefficient}")
            self._logger.debug(f"reflex {self.__reflex}")
            self._logger.debug(f"r {self.__r}")
            self._logger.debug(f"k1 {self.__k1}")
            self._logger.debug(f"k2_k1 {self.__k2_k1}")
        else:
            raise ValueError("NACA-Profilcode has not 5 digits")

    def norm_camber_y(self, arg_x: float) -> float:
        tmp_y = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        elif self.__reflex == 0:
            # STANDARD CAMBER LINE EQUATION
            # For 0 ≤ x ≤ r:
            #   y_c = (k1/6) × [x³ - 3×r×x² + r²×(3-r)×x]
            #
            # For r < x ≤ 1:
            #   y_c = (k1×r³/6) × (1 - x)
            if arg_x < self.__r:
                # Forward section of camber line
                tmp_y = (self.__k1 / 6.0) * (
                    arg_x**3 - 3 * self.__r * arg_x**2 + self.__r**2 * (3 - self.__r) * arg_x
                )
            else:
                # Aft section of camber line (linear decay)
                tmp_y = (self.__k1 * self.__r**3 / 6.0) * (1.0 - arg_x)
        elif self.__reflex == 1:
            # REFLEXED CAMBER LINE EQUATION
            # This produces an S-shaped camber line for reflexed airfoils
            # For 0 ≤ x ≤ r:
            #   y_c = (k1/6) × [(x-r)³ - (k2/k1)×(1-r)³×x - r³×x + r³]
            # For r < x ≤ 1:
            #   y_c = (k1/6) × [(k2/k1)×(x-r)³ - (k2/k1)×(1-r)³×x - r³×x + r³]
            k2_k1 = self.__k2_k1
            if arg_x < self.__r:
                tmp_y = (self.__k1 / 6.0) * (
                        (arg_x - self.__r)**3 - k2_k1 * (1 - self.__r)**3 * arg_x -
                    self.__r**3 * arg_x + self.__r**3
                )
            else:
                tmp_y = (self.__k1 / 6.0) * (
                    k2_k1 * (arg_x - self.__r)**3 - k2_k1 * (1 - self.__r)**3 * arg_x - self.__r**3 * arg_x + self.__r**3
                )
        return tmp_y

    def norm_camber_dydx(self, arg_x: float) -> float:
        tmp_dydx = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        elif self.__reflex == 0:
            if arg_x < self.__r:
                tmp_dydx = (self.__k1 / 6.0) * (
                    3.0 * arg_x**2 - 6.0 * self.__r * arg_x + self.__r**2 * (3 - self.__r)
                )
            else:
                tmp_dydx = - (self.__k1 * self.__r**3 / 6.0)
        elif self.__reflex == 1:
            k2_k1 = self.__k2_k1
            if arg_x < self.__r:
                tmp_dydx = (self.__k1 / 6.0) * (
                        3.0 * (arg_x - self.__r)**2 - k2_k1 * (1 - self.__r)**3 - self.__r**3
                )
            else:
                tmp_dydx = (self.__k1 / 6.0) * (
                    3.0 * k2_k1 * (arg_x - self.__r)**2 - k2_k1 * (1 - self.__r)**3 - self.__r**3
                )
        return tmp_dydx

    def norm_camber_dydx2(self, arg_x: float) -> float:
        tmp_dydx2 = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        elif self.__reflex == 0:
            if arg_x < self.__r:
                tmp_dydx2 = (self.__k1 / 6.0) * (
                    6.0 * arg_x - 6.0 * self.__r
                )
            else:
                tmp_dydx2 = 0.0
        elif self.__reflex == 1:
            k2_k1 = self.__k2_k1
            if arg_x < self.__r:
                tmp_dydx2 = (self.__k1 / 6.0) * (
                        6.0 * (arg_x - self.__r)
                )
            else:
                tmp_dydx2 = (self.__k1 / 6.0) * (
                    6.0 * k2_k1 * (arg_x - self.__r)
                )
        return tmp_dydx2
