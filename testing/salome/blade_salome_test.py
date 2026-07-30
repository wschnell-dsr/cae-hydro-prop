#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """

import logging
import logging.config
import unittest

from hydro_prop.meshing.profile import ProfileType
from hydro_prop.meshing.blade import Blade, BladeCnf, PitchDistributionType, ChordDistributionType

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

        tmp_blade_1_cnf: BladeCnf = {
            "key": "blade_1",
            "profile_pnts": 100,
            "radius_hub": 0.006,
            "radius_tip": 0.020,
            "radius_eps": 0.00001,
            "radius_pnts": 20,
            "profile_cnf": {
                "key": "NACA 0008",
                "profile_type": ProfileType.NACA,
                "profile_code": "0008"
            },
            "pitch_cnf": {
                "pitch_type": PitchDistributionType.LINEAR,
                "pitch_hub": 80.0,
                "pitch_tip": 30.0,
            },
            "chord_cnf": {
                "chord_type": ChordDistributionType.LINEAR,
                "chord_hub": 0.010,
                "chord_tip": 0.001,
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

        tmp_blade_1 = Blade(tmp_blade_1_cnf, self.geompy, OO, OX)
        self.geompy.addToStudy(tmp_blade_1.blade, "blade_1")

        tmp_blade_2_cnf: BladeCnf = {
            "key": "blade_2",
            "profile_pnts": 100,
            "radius_hub": 0.006,
            "radius_tip": 0.020,
            "radius_eps": 0.00001,
            "radius_pnts": 20,
            "profile_cnf": {
                "key": "NACA 0008",
                "profile_type": ProfileType.NACA,
                "profile_code": "0008"
            },
            "pitch_cnf": {
                "pitch_type": PitchDistributionType.LINEAR,
                "pitch_hub": 80.0,
                "pitch_tip": 30.0,
            },
            "chord_cnf": {
                "chord_type": ChordDistributionType.ELLIPTIC,
                "chord_hub": 0.010,
                "chord_tip": 0.001,
            },
            "skew_cnf": {
                "exponent": 1.0,
                "skew_max": 20.0
            },
            "rake_cnf": {
                "exponent": 1.0,
                "rake_max": 20.0
            },
        }
        tmp_blade_2 = Blade(tmp_blade_2_cnf, self.geompy, OO, OX)
        self.geompy.addToStudy(tmp_blade_2.blade, "blade_2")


if __name__ == "__main__":
    unittest.main()




