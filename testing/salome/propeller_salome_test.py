#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """

import logging
import os
import logging.config
import numpy
import unittest

from hydro_prop.meshing.blade import PitchDistributionType, ChordDistributionType
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
            "n_blades": 3,
            "hub_length": 0.01,
            "hub_radius": 0.0026,
            "hub_cap_cnf": {
                "form": "ELLIPTIC",
                "length": 0.006
            },
            "blade_offset": 0.005,
            "blade_cnf": {
                "key": "blade_1",
                "debug": True,
                "eps": 0.01,
                "rotation_direction": "RIGHT",
                "profile_pnts": 200,
                "radius_hub": 0.0025,
                "radius_tip": 0.020,
                "radius_eps": 0.0001,
                "radius_pnts": 50,
                "chord_center": 0.5,
                "profile_cnf": {
                    "key": "NACA 0012",
                    "profile_type": "NACA",
                    "profile_code": "0012"
                },
                "pitch_cnf": {
                    "pitch_type": PitchDistributionType.LINEAR.name,
                    "pitch_hub": 0.05,
                    "pitch_tip": 0.05
                },
                "chord_cnf": {
                    "comment": "OpenProp defaul distribution",
                    "chord_type": ChordDistributionType.CUBIC_SPLINE_TABULATED.name,
                    "radius":  [0.020 * rc for rc in [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]],
                    "chord": [0.040 * c for c in [0.1600, 0.1600, 0.1818, 0.2024, 0.2196, 0.2305, 0.2311, 0.2173, 0.1806, 0.1387, 0.00010]],
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
            "algorithm": "NETGEN_1D2D3D",
            "min_size": 0.0001,
            "max_size": 0.0005,
            "fineness": "MODERATE",
            "optimize": 1,
            "second_order": 0,
            "gmsh_3d_algo": "DELAUNAY",
            "gmsh_sub_div_algo": "AUTOMATIC",
            "gmsh_remesh_algo": "NO_SPLIT",
            "gmsh_remesh_param": "HARMONIC",
            "smouth_steps": 10,
            "size_factor": 0.6,
            "curvature": 5
        }

        tmp_propeller = Propeller(tmp_prop_cnf, self.geompy, self.smesh, OO, OX, OY)
        tmp_propeller.gen_geom("propeller")
        os.makedirs("testing/data/geo/", exist_ok=True)
        tmp_propeller.export_geo("testing/data/geo/")

        tmp_propeller.gen_mesh("propeller", mesh_cnf)
        os.makedirs("testing/data/mesh/", exist_ok=True)
        tmp_propeller.export_mesh("testing/data/mesh/")


if __name__ == "__main__":
    unittest.main()




