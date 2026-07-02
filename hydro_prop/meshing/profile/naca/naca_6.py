#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

from .base import NACAProfile


class NACA6Profile(NACAProfile):
    EPSILON: float = 1e-16
    __design_lift_coefficient: float
    __laminar_position: float
    __a: float
    ''' Position of minimum pressure (0.0 to 1.0)'''
    __g: float
    __h: float

    def __init__(self, arg_profile_code: str):
        super().__init__(arg_profile_code)

        self._parse_profile_code()

    @property
    def series(self) -> int:
        return 6

    def _parse_profile_code(self):
        if len(self.profile_code) == 6 or (len(self.profile_code) == 7 and "-" in self.profile_code):
            """
            NACA 6-digit series mean camber line calculation
            NACA 6-Series format: 6-digit-code mit Bindestrich (z.B. "612-415")
            Format: ABCDEF → AB-CDEF oder nur ABCDEF (wird zu AB-CDEF)
            - 1st digit (A): Series number (must be 6)
            - 2nd digit (B): Chordwise position of minimum pressure coefficient (a) × 10
            - 3rd digit (C): Design lift coefficient (c_li) × 10
            - 4th digit (D): Laminar flow code
            - 5-6 digits (EF): Maximum thickness × 100
            Parameters:
                a: Chordwise position of minimum pressure (2nd digit / 10)
                c_li: Design lift coefficient (3rd digit / 10)
            """
            # Normalisiere den Code: füge Bindestrich ein, falls nicht vorhanden
            if "-" in self.profile_code:
                code_parts = self.profile_code.split("-")
                if len(code_parts) != 2:
                    raise ValueError("NACA 6-Series Code muss Format AB-CDEF haben")
                first_part = code_parts[0]
                second_part = code_parts[1]
            else:
                # Wenn kein Bindestrich, nimm an es ist 6-stellig: ABCDEF → AB-CDEF
                if len(self.profile_code) != 6:
                    raise ValueError("NACA 6-Series Code muss 6 Ziffern haben")
                first_part = self.profile_code[0:3]
                second_part = self.profile_code[3:6]
            # Parse NACA 6-digit code
            self.__series_num = int(first_part[0])  # Must be 6
            if int(first_part[0]) != 6:
                raise ValueError("NACA 6 Series must begin with 6")
            # Extract parameters from code
            self.__a = int(first_part[1]) / 10.0
            self.__design_lift_coefficient = int(second_part[0]) / 10.0
            self.__laminar_position = int(second_part[1]) / 10.0
            self._max_thickness = 0.01 * int(second_part[2:])
            # Pre-calculate constant g using logarithmic terms
            # g = -1/(1-a) × [a²×(½×ln(a) - ¼) + ¼]
            # This parameter relates to the pressure distribution shape
            self.__g = -1.0 / (1.0 - self.__a) * (
                self.__a**2 * (0.5 * math.log(self.__a) - 0.25) + 0.25
            )
            # Pre-calculate constant h
            # h = 1/(1-a) × [½×(1-a)²×ln(1-a) - ¼×(1-a)²] + g
            # This is used in the camber line equation for continuity
            self.__h = 1.0 / (1.0 - self.__a) * (
                0.5 * (1.0 - self.__a)**2 * math.log(1.0 - self.__a) -
                0.25 * (1.0 - self.__a)**2
            ) + self.__g
            self._symmetric = False
        else:
            raise ValueError("NACA-Profilcode has not 6 digits")

    def norm_camber_y(self, arg_x: float) -> float:
        tmp_y = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        else:
            """
            NACA 6-digit series mean camber line
            The camber line uses complex logarithmic terms for a smooth
            pressure distribution defined by the aerodynamic design.
            Formula:
            y_c = (c_li / (2π(a+1))) × [
                1/(1-a) × (½(a-x)²×ln|a-x| - ½(1-x)²×ln(1-x) + ¼(1-x)² - ¼(a-x)²)
                - x×ln(x) + g - h×x
            ]
            Where:
            - a: Chordwise position of minimum pressure
            - c_li: Design lift coefficient
            - g, h: Pre-calculated constants from pressure distribution
            - x: Position along chord (0 to 1)
            """
            a = self.__a
            c_li = self.__design_lift_coefficient
            g = self.__g
            h = self.__h
            # Avoid logarithm singularities at x=0 and x=a
            # Use small epsilon to prevent log(0)
            x_safe = min(max(arg_x, self.EPSILON), 1.0 - self.EPSILON)
            # Main camber line equation components:
            # Part 1: Logarithmic term from pressure distribution
            part1 = 1.0 / (1.0 - a) * (
                0.5 * (a - arg_x)**2 * math.log(abs(a - x_safe)) -   # Upstream log term
                0.5 * (1.0 - arg_x)**2 * math.log(1.0 - x_safe) +       # Downstream log term
                0.25 * (1.0 - arg_x)**2 -                              # Quadratic correction (aft)
                0.25 * (a - arg_x)**2                                  # Quadratic correction (forward)
            )
            # Part 2: Logarithmic damping term
            part2 = -x_safe * math.log(x_safe)
            # Part 3: Constant integration terms
            part3 = g - h * arg_x
            # Complete camber line equation
            tmp_y = (c_li / (2.0 * math.pi * (a + 1.0))) * (
                part1 + part2 + part3
            )
        return tmp_y

    def norm_camber_dydx(self, arg_x: float) -> float:
        tmp_dydx = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        else:
            tmp_dydx = 0.0
        return tmp_dydx

    def norm_camber_dydx2(self, arg_x: float) -> float:
        tmp_dydx2 = 0.0
        if not self.in_norm_range(arg_x):
            raise ValueError(f"x = {arg_x} not in norm range")
        elif self.symmetric:
            pass
        else:
            tmp_dydx2 = 0.0
        return tmp_dydx2


