#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """

import logging
import os
import logging.config
import unittest

from hydro_prop.meshing.propeller import PropCnf, Propeller
from hydro_prop.meshing.meshing import MeshParameters

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


class TestPropellerSalome(unittest.TestCase):

    def test_propeller_salome(self):
        logging.config.dictConfig(LOGGER_CONFIG)
        logging.info("test_propeller_salome")

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

        tmp_prop_cnf: PropCnf = {
            "n_blades": 2,
            "hub_length": 0.01,
            "hub_radius": 0.00225,
            "hub_cap_cnf": {
                "form": "ELLIPTIC",
                "length": 0.006
            },
            "blade_offset": 0.0025,
            "blade_cnf": {
                "key": "blade_1",
                "profile_pnts": 100,
                "radius_hub": 0.002,
                "radius_tip": 0.020,
                "radius_eps": 0.00005,
                "radius_pnts": 40,
                "profile_cnf": {
                    "key": "NACA 0012",
                    "profile_type": "NACA",
                    "profile_code": "0012"
                },
                "pitch_cnf": {
                    "pitch_type": "LINEAR",
                    "pitch_hub": 45.0,
                    "pitch_tip": 80.0,
                },
                "chord_cnf": {
                    "chord_type": "ELLIPTIC",
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
                }
            }
        }

        mesh_cnf: MeshParameters = {
            "algorithm": "GMSH",
            "min_size": 0.000,
            "max_size": 0.00025,
            "fineness": None,
            "optimize": None,
            "second_order": None,
            "gmsh_3d_algo": "DELAUNAY",
            "gmsh_sub_div_algo": "AUTOMATIC",
            "gmsh_remesh_algo": "NO_SPLIT",
            "gmsh_remesh_param": "HARMONIC",
            "smouth_steps": 10,
            "size_factor": 0.4,
            "curvature": 5
        }

        tmp_propeller = Propeller(tmp_prop_cnf, self.geompy, self.smesh, OO, OX, OY)
        tmp_propeller.gen_geom("propeller")
        tmp_propeller.gen_mesh("propeller", mesh_cnf)

        os.makedirs("testing/data/", exist_ok=True)
        tmp_propeller.export_mesh("testing/data/")


if __name__ == "__main__":
    unittest.main()




