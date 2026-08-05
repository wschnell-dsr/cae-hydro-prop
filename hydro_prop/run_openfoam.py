#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import os
import json

from hydro_prop.open_foam.case import Case

from . import LOGGER_CONFIG


def run_case(arg_study: str, arg_type: str, arg_case: str = ""):

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

    for tmp_key, tmp_case_dict in tmp_config["openfoam"][arg_type].items():
        if arg_case == "" or arg_case == tmp_key:
            tmp_cases_dir = os.path.join(arg_study, "openfoam", arg_type)
            os.makedirs(tmp_cases_dir, exist_ok=True)
            tmp_case = Case(arg_study, tmp_case_dict)
            tmp_case.pre_pro()
            tmp_case.solve()
            tmp_case.post_pro()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", type=str, default="", help="Path to study")
    parser.add_argument("--type", type=str, required=True, help="meshes or cases")
    parser.add_argument("--case", type=str, default="", help="Case")
    args = parser.parse_args()

    logging.config.dictConfig(LOGGER_CONFIG)
    logger = logging.getLogger("hydro_prop")

    run_case(args.study, args.type, args.case)
