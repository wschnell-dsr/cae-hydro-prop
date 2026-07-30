#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config

from . import LOGGER_CONFIG

from .run_meshing import run_meshing

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", type=str, default="", help="Path to study")
    args = parser.parse_args()

    logging.config.dictConfig(LOGGER_CONFIG)
    logger = logging.getLogger("hydro_prop")

    run_meshing(args.study)






