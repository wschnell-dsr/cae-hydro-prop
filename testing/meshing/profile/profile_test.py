#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """

import logging
import logging.config
import unittest
import matplotlib.pyplot as plt

from typing import List

from hydro_prop.meshing.profile import ProfileFactory, ProfileCnfVariant, ProfileType

'''
import salome
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder
'''


# pyright: reportAttributeAccessIssue=false
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


class TestProfile(unittest.TestCase):
    NPOINTS: int = 100
    TEST_PROFILE_CNFS: List[ProfileCnfVariant] = [
        {
            "key": "NACA 0008",
            "profile_type": ProfileType.NACA,
            "profile_code": "0008"
        },
        {
            "key": "NACA 1208",
            "profile_type": ProfileType.NACA,
            "profile_code": "1208"
        }
    ]

    def test_profile_plot(self):
        logging.config.dictConfig(LOGGER_CONFIG)
        logging.info("")
        tmp_factory = ProfileFactory()
        tmp_profiles = {}

        plt.clf()
        tmp_idx = 1
        for tmp_cnf in self.TEST_PROFILE_CNFS:

            try:
                tmp_profiles[tmp_cnf["key"]] = tmp_factory.create(tmp_cnf)
                tmp_profiles[tmp_cnf["key"]].calc_norm_x_distribution(self.NPOINTS)
                (x_upper, y_upper), (x_lower, y_lower) = tmp_profiles[tmp_cnf["key"]].profile_line(2.0, 5.0)
                (x_camber, y_camber) = tmp_profiles[tmp_cnf["key"]].camber_line(2.0, 5.0)
            except Exception:
                logging.exception("Exception")

            plt.subplot(len(self.TEST_PROFILE_CNFS), 1, tmp_idx)
            plt.title(f"{tmp_cnf["key"]}")
            plt.plot(x_upper, y_upper, '-', label="Upper line", color="blue")
            plt.plot(x_camber, y_camber, '-', label="Camber line", color="red")
            plt.plot(x_lower, y_lower, '-', label="Lower line", color="green")
            plt.ylabel("y")
            plt.xlabel("x")
            plt.grid(True)
            plt.legend()
            tmp_idx += 1
        plt.tight_layout()
        plt.show()

'''
class TestNacaProfileSalome(unittest.TestCase):
    NPOINTS: int = 200
    TEST_CODE = "0008"

    def test_naca_wire(self):
        logging.config.dictConfig(LOGGER_CONFIG)
        logging.info("")

        tmp_profile = NACAProfile(self.TEST_CODE)
        (x_upper, y_upper), (x_lower, y_lower) = tmp_profile.profile_coordinates(self.NPOINTS)
        y_camber = tmp_profile.camber_line(x_upper)

        salome.salome_init()
        self.geompy = geomBuilder.New()
        OO = self.geompy.MakeVertex(0, 0, 0)
        OX = self.geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = self.geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = self.geompy.MakeVectorDXDYDZ(0, 0, 1)
        self.geompy.addToStudy(OO, 'OO')
        self.geompy.addToStudy(OX, 'OX')
        self.geompy.addToStudy(OY, 'OY')
        self.geompy.addToStudy(OZ, 'OZ')
'''


if __name__ == "__main__":
    unittest.main()
