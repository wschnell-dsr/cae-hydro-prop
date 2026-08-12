# -*- coding: utf-8 -*-
import os
import shutil
from deepmerge import always_merger
from typing import Any, Dict, List, TypedDict

from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.TemplateFile import TemplateFile
from PyFoam.Applications.Runner import Runner


class Resource(TypedDict):
    source: str
    target: str


class ParsedParameterFileCnf(TypedDict):
    parameter_file: str
    replace: Dict[str, Any]


class TemplateFileCnf(TypedDict):
    template_file: str
    template_target_file: str
    placeholder: Dict[str, Any]


class CaseCnf(TypedDict):
    case_template: str
    case_target: str
    resources: List[Resource]
    parsed_parameter_files: List[ParsedParameterFileCnf]
    template_files: List[ParsedParameterFileCnf]
    runner_args: List[List[str]]


class Case:
    __cnf: CaseCnf

    def __init__(self, arg_study: str, arg_cnf: CaseCnf):
        self.__study = arg_study
        self.__cnf = arg_cnf

        self.case_template = os.path.join(self.__study, self.__cnf["case_template"])
        self.case_target = os.path.join(self.__study, self.__cnf["case_target"])
        if os.path.exists(self.case_target):
            shutil.rmtree(self.case_target)
        origin = SolutionDirectory(self.case_template, archive=None, paraviewLink=False)
        self.case = origin.cloneCase(self.case_target)

    def pre_pro(self):
        for tmp_res in self.__cnf["resources"]:
            tmp_res_src = os.path.join(self.__study, tmp_res["source"])
            tmp_res_tar = os.path.join(self.case.name, tmp_res["target"])
            if os.path.isfile(tmp_res_src):
                os.makedirs(os.path.dirname(tmp_res_tar), exist_ok=True)
                shutil.copy(tmp_res_src, tmp_res_tar)
            elif os.path.isdir(tmp_res_src):
                shutil.copytree(tmp_res_src, tmp_res_tar)
        for tmp_ppf in self.__cnf["parsed_parameter_files"]:
            tmp_file_dict = ParsedParameterFile(os.path.join(self.case.name, tmp_ppf["file"]))
            for key, item in tmp_ppf["placeholder"].items():
                if key in tmp_file_dict:
                    if isinstance(item, dict):
                        tmp_file_dict[key] = always_merger.merge(tmp_file_dict[key], item)
                    else:
                        tmp_file_dict[key] = item
            tmp_file_dict.writeFile()
        for tmp_tf in self.__cnf["template_files"]:
            tmp_template = TemplateFile(os.path.join(self.case.name, tmp_tf["template_file"]))
            tmp_template.writeToFile(os.path.join(self.case.name, tmp_tf["template_target_file"]), tmp_tf["placeholder"])
            os.remove(os.path.join(self.case.name, tmp_tf["template_file"]))
        for tmp_run in self.__cnf["pre_pro_runner_args"]:
            tmp_args = tmp_run
            tmp_args.extend(["-case", self.case.name])
            Runner(args=tmp_args, silent=False)

    def solve(self):
        for tmp_run in self.__cnf["runner_args"]:
            tmp_args = tmp_run
            tmp_args.extend(["-case", self.case.name])
            Runner(args=tmp_args, silent=False)

    def post_pro(self):
        for tmp_run in self.__cnf["post_pro_runner_args"]:
            tmp_args = tmp_run
            tmp_args.extend(["-case", self.case.name])
            Runner(args=tmp_args, silent=False)
