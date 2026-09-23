# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import logging
import os
import glob
import shutil
import pandas
from deepmerge import always_merger
from typing import Any, Dict, List, Tuple, TypedDict

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
    engine: str
    template_file: str
    template_target_file: str
    placeholder: Dict[str, Any]


class CaseCnf(TypedDict):
    case_template: str
    case_target: str
    resources: List[Resource]
    parsed_parameter_files: List[ParsedParameterFileCnf]
    template_files: List[ParsedParameterFileCnf]
    pre_pro_runner_args: List[List[str]]
    runner_args: List[List[str]]
    post_pro_runner_args: List[List[str]]
    post_pro: List[Dict[str, Any]]


class Case:
    __cnf: CaseCnf
    __clean: bool
    __pre_pro: bool
    __solve: bool
    __post_pro: bool

    def __init__(self, arg_study: str, arg_cnf: CaseCnf, arg_opt: Tuple[bool, bool, bool, bool]):
        self.__logger = logging.getLogger("hydro_prop.openfoam")
        self.__study = arg_study
        self.__cnf = arg_cnf
        self.__clean = arg_opt[0]
        self.__pre_pro = arg_opt[1]
        self.__solve = arg_opt[2]
        self.__post_pro = arg_opt[3]

        self.case_template = os.path.join(self.__study, self.__cnf["case_template"])
        self.case_target = os.path.join(self.__study, self.__cnf["case_target"])
        if os.path.exists(self.case_target) and self.__clean:
            shutil.rmtree(self.case_target)

        if not os.path.exists(self.case_target):
            origin = SolutionDirectory(self.case_template, archive=None, paraviewLink=False)
            self.case = origin.cloneCase(self.case_target)
        else:
            self.case = SolutionDirectory(self.case_target, archive=None, paraviewLink=False)
        self.__logger.debug(f"Case {self.case.name} generated")

    def pre_pro(self):
        if self.__pre_pro:
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
                if tmp_tf["engine"] == "pyFoamTemplate":
                    tmp_template = TemplateFile(os.path.join(self.case.name, tmp_tf["template_file"]))
                    tmp_template.writeToFile(os.path.join(self.case.name, tmp_tf["template_target_file"]), tmp_tf["placeholder"])
                    os.remove(os.path.join(self.case.name, tmp_tf["template_file"]))
                elif tmp_tf["engine"] == "jinja2":
                    env = Environment(loader=FileSystemLoader(self.case.name), trim_blocks=True, lstrip_blocks=True)
                    template = env.get_template(tmp_tf["template_file"])
                    with open(os.path.join(self.case.name, tmp_tf["template_target_file"]), 'w') as fh:
                        fh.write(template.render(**tmp_tf["placeholder"]))
                    os.remove(os.path.join(self.case.name, tmp_tf["template_file"]))
            for tmp_run in self.__cnf["pre_pro_runner_args"]:
                tmp_args = tmp_run
                tmp_args.extend(["-case", self.case.name])
                Runner(args=tmp_args, silent=False)

    def solve(self):
        if self.__solve:
            for tmp_run in self.__cnf["runner_args"]:
                tmp_args = tmp_run
                tmp_args.extend(["-case", self.case.name])
                Runner(args=tmp_args, silent=False)

    def post_pro(self):
        if self.__post_pro:
            self.__logger.debug(f"Running post_pro on {self.case.name}")
            if "post_pro_runner_args" in self.__cnf:
                for tmp_run in self.__cnf["post_pro_runner_args"]:
                    tmp_args = tmp_run
                    tmp_args.extend(["-case", self.case.name])
                    Runner(args=tmp_args, silent=False)
            if "post_pro" in self.__cnf:
                for tmp_post in self.__cnf["post_pro"]:
                    if tmp_post["type"] == "parse_regex":
                        self.__logger.debug(f"Glob for files with {os.path.join(self.case.name, tmp_post["glob"])}")
                        tmp_files = glob.glob(os.path.join(self.case.name, tmp_post["glob"]))
                        df_all = None
                        for tmp_file in tmp_files:
                            self.__logger.debug(f"Parse file {tmp_file}")
                            tmp_lines = []
                            with open(tmp_file, 'r') as f:
                                tmp_lines = f.readlines()

                            df = pandas.DataFrame(tmp_lines, columns=['raw'])
                            df[tmp_post["columns"]] = df['raw'].str.extract(tmp_post["pattern"]).apply(pandas.to_numeric, errors='coerce')
                            df = df.dropna(subset=tmp_post["columns"]).drop(columns=['raw'])
                            df = df.set_index('step')
                            if df_all is None:
                                df_all = df
                            else:
                                df_all.update(df)
                        for tmp_col, tmp_expr in tmp_post["expressions"].items():
                            df_all[tmp_col] = df.eval(tmp_expr)
                        df_all.to_csv(os.path.join(self.case.name, tmp_post["output"]))



