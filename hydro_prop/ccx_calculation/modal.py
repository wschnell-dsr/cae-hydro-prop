#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import datetime
import os
import subprocess
import shutil

from typing import Any, Dict, NotRequired, TypedDict


class ModalCnf(TypedDict):
    name: str
    template: str
    mesh: str
    material: Dict[str, Any]
    elset_name: str
    mesh_file: NotRequired[str]
    date: NotRequired[datetime.datetime]


DEFAULT_MODAL_CNF: ModalCnf = {
    "name": "modal",
    "template": os.path.join("resource", "modal.inp.jinja"),
    "mesh": "mesh_01",
    "material": {"name": "STEEL", "density": 7850, "youngs": 210e9, "pratio": 0.3},
    "elset_name": "C3D4",
    "boundary_fix": "bottom_outside",
    "n_frequencies": 16
}


class Modal:
    __config: ModalCnf
    __case_file: str

    def __init__(self, arg_config: ModalCnf, arg_meshes: Dict[str, Any]):
        self.__config = arg_config
        self.__config["date"] = datetime.datetime.now()
        self.__config["mesh_file"] = arg_meshes[self.__config["mesh"]]["mesh_file"]
        self.__case_file = ""

    def generate_case(self, arg_output_dir: str) -> str:
        env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(self.__config["template"])
        self.__case_file = os.path.join(arg_output_dir, f"{self.__config['name']}.inp")
        self.__config["mesh_file"] = os.path.relpath(os.path.abspath(self.__config["mesh_file"]), os.path.dirname(os.path.abspath(self.__case_file)))
        with open(self.__case_file, 'w') as fh:
            fh.write(template.render(**self.__config))
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
            "name": self.__config['name'],
            "working_dir": workdir
        }

        return modal_case


if __name__ == "__main__":
    tmp_config: ModalCnf = DEFAULT_MODAL_CNF
    tmp_modal = Modal(tmp_config)
    tmp_modal.run("mesh")
