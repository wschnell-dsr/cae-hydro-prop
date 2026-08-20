#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import os
import json

from hydro_prop.calculix.case import Case, CaseCnf

from . import LOGGER_CONFIG


def run_ccx(arg_study: str, arg_case: str = ""):

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

    for tmp_key, tmp_case_dict in tmp_config["calculix"]["cases"].items():
        if arg_case == "" or arg_case == tmp_key:
            tmp_cases_dir = os.path.join(arg_study, "calculix", "cases")
            os.makedirs(tmp_cases_dir, exist_ok=True)
            tmp_case = Case(arg_study, tmp_case_dict)
            tmp_case.generate_case()
            tmp_case.run()
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", type=str, default="", help="Path to study")
    args = parser.parse_args()

    logging.config.dictConfig(LOGGER_CONFIG)
    logger = logging.getLogger("hydro_prop")

    run_ccx(args.study)







