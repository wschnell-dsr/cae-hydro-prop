#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import meshing
import calculation
import postprocessing
import argparse

from typing import Any, Dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="", help="Singing bowl configs")
    args = parser.parse_args()

    tmp_meshes = {}

    tmp_configs: Dict[str, Any] = {
        "study": os.path.join("run", "study_default"),
        "meshing": {
            "mesh_01": meshing.singing_bowl.DEFAULT_CONFIG
        },
        "modal": {
            "modal_01": calculation.singing_bowl.DEFAULT_MODAL_CONFIG
        }
    }

    if os.path.exists(args.config) and os.path.isfile(args.config):
        with open(args.config, 'r') as jfile:
            tmp_configs = json.load(jfile)

    for tmp_key, tmp_mconfig in tmp_configs["meshing"].items():
        tmp_mesh_dir = os.path.join(tmp_configs["study"], "meshes", tmp_key)
        os.makedirs(tmp_mesh_dir, exist_ok=True)
        tmp_singing_bowl = meshing.SingingBowl(tmp_mconfig)
        tmp_singing_bowl.generate_geom()
        tmp_singing_bowl.generate_mesh()
        tmp_meshes[tmp_key] = {
            "mesh_file": tmp_singing_bowl.export_to_inp(os.path.join(tmp_configs["study"], "meshes", tmp_key, "mesh"))
        }
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






