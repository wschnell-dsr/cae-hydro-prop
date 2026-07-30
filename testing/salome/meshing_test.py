#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """

import logging
import logging.config
import unittest

import salome
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder

from hydro_prop.meshing.meshing import create_mesh, MeshParameters

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


class TestMeshingSalome(unittest.TestCase):

    def test_meshing_salome(self):
        logging.config.dictConfig(LOGGER_CONFIG)
        logging.info("test_meshing_salome")

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
        self.cylinder = self.geompy.MakeCylinder(OO, OX, 0.004, 0.01)
        self.geompy.addToStudy(self.cylinder, 'cylinder')

        tmp_meshing_params: MeshParameters = {
            "algorithm": "NETGEN_1D2D3D",
            "min_size": 0.001,
            "max_size": 0.001,
            "fineness": "FINE",
            "optimize": None,
            "second_order": None
        }
        self.mesh = create_mesh(self.smesh, self.cylinder, "test_mesh", tmp_meshing_params)
        self.mesh.Compute()
