#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """

import logging
import logging.config
import numpy
import unittest

from hydro_prop.meshing.blade import Blade, BladeCnf, PitchDistributionType, ChordDistributionType

from typing import List

import salome
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder


# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false
LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": 0,
    "formatters": {"standard": {"format": "%(asctime)s %(module)s %(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s"}},
    "handlers": {"default": {"level": "INFO", "formatter": "standard", "class": "logging.StreamHandler"}},
    "loggers": {
        "": {"handlers": ["default"], "level": "DEBUG"},
        "matplotlib": {"handlers": ["default"], "level": "INFO"},
        "hydro_prop.meshing.profile": {"handlers": ["default"], "level": "DEBUG", "propagate": False}
    },
}


class TestBladeSalome(unittest.TestCase):

    def test_blade_salome(self):
        logging.config.dictConfig(LOGGER_CONFIG)
        logging.info("test_blade_salome")

        salome.salome_init()
        self.geompy = geomBuilder.New()
        self.smesh = smeshBuilder.New()
        OO = self.geompy.MakeVertex(0, 0, 0)
        OX = self.geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = self.geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = self.geompy.MakeVectorDXDYDZ(0, 0, 1)
        self.geompy.addToStudy(OO, 'OO')
        self.geompy.addToStudy(OX, 'OX')
        self.geompy.addToStudy(OY, 'OY')
        self.geompy.addToStudy(OZ, 'OZ')

        tmp_blade_cnfs: List[BladeCnf] = [
            {
                "key": "blade_1",
                "debug": 1,
                "eps": 0.01,
                "rotation_direction": "RIGHT",
                "profile_pnts": 100,
                "radius_hub": 0.0072,
                "radius_tip": 0.030,
                "radius_eps": 0.0001,
                "radius_pnts": 20,
                "chord_center": 0.25,
                "profile_cnf": {
                    "key": "NACA 23012",
                    "profile_type": "NACA",
                    "profile_code": "23012"
                },
                "pitch_cnf": {
                    "pitch_type": "LINEAR",
                    "pitch_hub": 0.03,
                    "pitch_tip": 0.02
                },
                "chord_cnf": {
                    "chord_type": "ELLIPTIC",
                    "chord_hub":  0.02,
                    "chord_tip": 0.010
                },
                "thickness_distribution_cnf": {
                    "radius": [0.0, 1.0],
                    "thickness": [1.0, 1.0],
                },
                "skew_cnf": {
                    "exponent": 1.0,
                    "skew_max": 0.0
                },
                "rake_cnf": {
                    "exponent": 1.0,
                    "rake_max": 0.0
                }
            },
            {
                "key": "blade_2",
                "debug": True,
                "eps": 0.01,
                "rotation_direction": "RIGHT",
                "profile_pnts": 100,
                "radius_hub": 0.0025,
                "radius_tip": 0.020,
                "radius_eps": 0.0001,
                "radius_pnts": 20,
                "chord_center": 0.0,
                "profile_cnf": {
                    "key": "MIXED_ZERO_PARABOLIC",
                    "profile_type": "MIXED",
                    "mixed_cnf":
                    {
                        "camber_line_cnf": {
                            "camber_line_type": "PARABOLIC",
                            "camber": 0.2
                        },
                        "thickness_distribution_cnf": {
                            "thickness_distribution_type": "ELLIPTIC",
                            "max_thickness": 0.08
                        },
                    }
                },
                "pitch_cnf": {
                    "pitch_type": PitchDistributionType.LINEAR.name,
                    "pitch_hub": 0.1,
                    "pitch_tip": 0.1
                },
                "chord_cnf": {
                    "chord_type": ChordDistributionType.LINEAR_TABULATED.name,
                    "radius": numpy.linspace(0.0025, 0.020, 20).astype(float),
                    "chord": [0.008 * numpy.sin(numpy.pi * r / (2.0 * 0.0101)) for r in numpy.linspace(0.0025, 0.020, 20).astype(float)],
                },
                "thickness_distribution_cnf": {
                    "radius": [0.0, 1.0],
                    "thickness": [1.0, 1.0],
                },
                "skew_cnf": {
                    "exponent": 1.0,
                    "skew_max": 0.0
                },
                "rake_cnf": {
                    "exponent": 1.0,
                    "rake_max": 0.0
                },
            },
            {
                "key": "blade_3",
                "debug": True,
                "eps": 0.01,
                "rotation_direction": "RIGHT",
                "profile_pnts": 100,
                "radius_hub": 0.0025,
                "radius_tip": 0.020,
                "radius_eps": 0.0001,
                "radius_pnts": 40,
                "chord_center": 0.5,
                "profile_cnf": {
                    "key": "NACA 0012",
                    "profile_type": "NACA",
                    "profile_code": "0012"
                },
                "pitch_cnf": {
                    "pitch_type": PitchDistributionType.LINEAR.name,
                    "pitch_hub": 0.1,
                    "pitch_tip": 0.1
                },
                "chord_cnf": {
                    "comment": "OpenProp defaul distribution",
                    "chord_type": ChordDistributionType.CUBIC_SPLINE_TABULATED.name,
                    "radius":  [0.020 * rc for rc in [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]],
                    "chord": [0.040 * c for c in [0.1600, 0.1600, 0.1818, 0.2024, 0.2196, 0.2305, 0.2311, 0.2173, 0.1806, 0.1387, 0.00010]],
                },
                "thickness_distribution_cnf": {
                    "radius": [0.0, 1.0],
                    "thickness": [1.0, 1.0],
                },
                "skew_cnf": {
                    "exponent": 1.0,
                    "skew_max": 0.0
                },
                "rake_cnf": {
                    "exponent": 1.0,
                    "rake_max": 0.0
                },
            }
        ]
        for tmp_blade_cnf in tmp_blade_cnfs:
            tmp_blade = Blade(tmp_blade_cnf, self.geompy, OO, OX)
            tmp_blade.gen_blade()
            self.geompy.addToStudy(tmp_blade.blade, tmp_blade.key)


if __name__ == "__main__":
    unittest.main()
