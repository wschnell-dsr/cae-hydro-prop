# -*- coding: utf-8 -*-
import argparse
from jinja2 import Environment, FileSystemLoader
import logging
import os
import json
import shutil


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", type=str, default="", help="Path to study")
    args = parser.parse_args()

    if os.path.isdir(args.study) and os.path.isfile(os.path.join(args.study, "config.json.jinja")) and os.path.isfile(os.path.join(args.study, "parameter.json")):
        env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
        tmp_template = env.get_template(os.path.join(args.study, "config.json.jinja"))
        tmp_paramter = None
        with open(os.path.join(args.study, "parameter.json")) as f_json_param:
            tmp_paramter = json.load(f_json_param)
        with open(os.path.join(args.study, "config.json"), 'w') as fh:
            fh.write(tmp_template.render(**tmp_paramter))
