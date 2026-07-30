#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import os
import json

from hydro_prop.meshing.propeller import Propeller

import salome
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder

from . import LOGGER_CONFIG


def run_meshing(arg_study: str):

    tmp_meshes = {}
    tmp_config = {}
    if (
        os.path.exists(arg_study) and
        os.path.isdir(arg_study) and
        os.path.exists(os.path.join(arg_study, "config.json")) and
        os.path.isfile(os.path.join(arg_study, "config.json"))
    ):
        with open(os.path.join(arg_study, "config.json"), 'r') as jfile:
            tmp_config = json.load(jfile)
    else:
        logger.fatal(f"Path to study config does not exist {os.path.join(arg_study, "config.json")}")
        exit(1)

    for tmp_key, tmp_mconfig in tmp_config["meshing"].items():
        tmp_mesh_dir = os.path.join(arg_study, "meshes", tmp_key)
        os.makedirs(tmp_mesh_dir, exist_ok=True)

        salome.salome_init()
        geompy = geomBuilder.New()
        smesh = smeshBuilder.New()
        ref_pnt = geompy.MakeVertex(*tmp_mconfig["ref_pnt"])
        ref_axis = geompy.MakeVectorDXDYDZ(*tmp_mconfig["ref_axis"])
        tmp_mesh = Propeller(tmp_mconfig["prop_cnf"], geompy, smesh, ref_pnt, ref_axis)
        tmp_mesh.gen_geom("propeller")
        tmp_mesh.gen_mesh("propeller", tmp_mconfig["mesh_cnf"])
        tmp_meshes[tmp_key] = {
            "mesh_file": tmp_mesh.export_mesh(os.path.join(args.study, "meshes", tmp_key))
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", type=str, default="", help="Path to study")
    args = parser.parse_args()

    logging.config.dictConfig(LOGGER_CONFIG)
    logger = logging.getLogger("hydro_prop")

    run_meshing(args.study)

    '''
    modal_cases = []
    for tmp_key, tmp_mconfig in tmp_configs["modal"].items():
        tmp_modal_dir = os.path.join(tmp_configs["study"], "modal", tmp_key)
        os.makedirs(tmp_modal_dir, exist_ok=True)
        tmp_singing_bowl_modal = calculation.SingingBowlModal(tmp_mconfig, tmp_meshes)
        tmp_singing_bowl_modal.generate_case(tmp_modal_dir)
        tmp_case = tmp_singing_bowl_modal.run()
        modal_cases.append(tmp_case)

    for tmp_case in modal_cases:
        tmp_modal = postprocessing.SingingBowlModal(tmp_case)
        tmp_modal.ccx_2_paraview()
        tmp_modal.parse_modal_dat()
        tmp_modal.animate()
    '''






