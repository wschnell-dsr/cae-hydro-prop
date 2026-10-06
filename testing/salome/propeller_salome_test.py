# -*- coding: utf-8 -*-
""" """
import argparse
import json
import logging
import logging.config
import os
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
    "handlers": {"default": {"level": "DEBUG", "formatter": "standard", "class": "logging.StreamHandler"}},
    "loggers": {
        "": {"handlers": ["default"], "level": "DEBUG"},
        "matplotlib": {"handlers": ["default"], "level": "INFO"},
        "hydro_prop.meshing": {"handlers": ["default"], "level": "DEBUG", "propagate": False}
    },
}


class TestPropellerSalome(unittest.TestCase):

    def setUp(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--study', required=True)
        parser.add_argument('--mesh', required=True)
        self.options, _ = parser.parse_known_args()

        with open(os.path.join(self.options.study, "config.json"), 'r') as f:
            self.study_data = json.load(f)
        self.mesh_data = self.study_data["meshing"][self.options.mesh]

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
        ref_pnt = self.geompy.MakeVertex(*self.mesh_data["ref_pnt"])
        ref_axis = self.geompy.MakeVectorDXDYDZ(*self.mesh_data["ref_axis"])
        norm_axis = self.geompy.MakeVectorDXDYDZ(*self.mesh_data["norm_axis"])

        tmp_prop_cnf = self.mesh_data["prop_cnf"]

        tmp_propeller = Propeller(tmp_prop_cnf, self.geompy, self.smesh, ref_pnt, ref_axis, norm_axis)
        tmp_propeller.gen_geom("propeller")
        os.makedirs("testing/data/geo/", exist_ok=True)
        tmp_propeller.export_geo("testing/data/geo/")

        #tmp_propeller.gen_mesh("propeller", mesh_cnf)
        #os.makedirs("testing/data/mesh/", exist_ok=True)
        #tmp_propeller.export_mesh("testing/data/mesh/")


if __name__ == "__main__":
    unittest.main()
