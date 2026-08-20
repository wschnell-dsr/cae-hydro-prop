#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import datetime
import os
import subprocess
import shutil

from typing import Any, Dict, List, TypedDict


class CaseCnf(TypedDict):
    template: str
    case_dir: str
    case_file: str
    mesh_file: str
    data: Dict[str, Any]


class Case:
    __config: CaseCnf
    __case_file: str

    def __init__(self, arg_study: str, arg_config: CaseCnf):
        self.__study = arg_study
        self.__config = arg_config
        print(self.__config)
        os.makedirs(os.path.join(self.__study, self.__config["case_dir"]), exist_ok=True)
        self.__case_file = os.path.join(self.__study, self.__config["case_dir"], f"{self.__config['case_file']}")

    def generate_case(self) -> str:
        env = Environment(loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(self.__config["template"])
        with open(self.__case_file, 'w') as fh:
            fh.write(template.render(**self.__config["data"]))
        return self.__case_file

    def run(self) -> Dict[str, Any]:
        ccx = shutil.which("ccx")
        workdir = os.path.dirname(self.__case_file)
        basename = os.path.splitext(os.path.basename(self.__case_file))[0]
        tmp_sub_proc = subprocess.Popen([ccx, basename], cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        # Zeile für Zeile ausgeben
        with tmp_sub_proc.stdout:
            for line in tmp_sub_proc.stdout:
                print(line, end="")  # oder an Logger schicken

        rc = tmp_sub_proc.wait()
        if rc != 0:
            raise RuntimeError(f"ccx returned {rc}")

        modal_case: Dict[str, Any] = {
            "name": self.__case_file,
            "working_dir": workdir
        }

        return modal_case
