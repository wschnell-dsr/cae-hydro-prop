# -*- coding: utf-8 -*-
from salome.geom import geomBuilder
from typing import Any, Optional, TypedDict
from salome.smesh import smeshBuilder

from .blade import Blade, BladeCnf

try:
    from unv2ccx import Converter
except ModuleNotFoundError:
    Converter = None


class PropCnf(TypedDict):
    n_blades: int
    hub_length: float
    hub_offset: float
    blade_cnf: BladeCnf


class Propeller:
    __cnf: PropCnf
    blade: Any
    blades_cmp: Any
    blades: Any
    hub: Any
    propeller: Any

    def __init__(self, arg_cnf: PropCnf, arg_geompy: geomBuilder, arg_ref_pnt: Any, arg_ref_axis: Any, arg_key: Optional[str]):
        self.geompy = arg_geompy
        self.__cnf = arg_cnf
        self.blade = Blade(self.blade_cnf, self.geompy, arg_ref_pnt, arg_ref_axis)
        self.blades_cmp = self.geompy.MultiRotate1DNbTimes(self.blade.blade, arg_ref_axis, self.n_blades)
        self.hub = self.geompy.MakeTranslationVectorDistance(
            self.geompy.MakeCylinder(arg_ref_pnt, arg_ref_axis, self.blade.radius_hub, self.hub_length),
            arg_ref_axis,
            self.hub_offset
        )
        self.hub_cap = self.geompy.MakeTranslationVectorDistance(
            self.geompy.MakeSpherePntR(arg_ref_pnt, self.blade.radius_hub), arg_ref_axis, self.hub_length + self.hub_offset
        )

        self.propeller = self.geompy.MakeFuseList([self.hub, self.hub_cap, self.blades_cmp], False, False)
        self.blades = self.geompy.ExtractShapes(self.blades_cmp, self.geompy.ShapeType["SOLID"], True)

        if arg_key:
            self.geompy.addToStudy(self.propeller, arg_key)
            blidx = 0
            for tmp_blade in self.blades:
                self.geompy.addToStudy(tmp_blade, f"{arg_key}_blade_{blidx}")
                blidx += 1

        self.propeller_faces = self.geompy.ExtractShapes(self.propeller, self.geompy.ShapeType["FACE"], True)
        self.blade_faces = {}
        blidx = 0
        for tmp_blade in self.blades:
            self.blade_faces[blidx] = self.geompy.ExtractShapes(tmp_blade, self.geompy.ShapeType["FACE"], True)
            blidx += 1
        for tmp_face in self.propeller_faces:
            if self.geompy.MinDistanceComponents(tmp_face, self.vt_out_center)[0] < 1e-5:
                self.boundary_ids["bottom_outside"].append(tmp_face)

    @property
    def blade_cnf(self) -> BladeCnf:
        return self.__cnf["blade_cnf"]

    @property
    def n_blades(self) -> int:
        return self.__cnf["n_blades"]

    @property
    def hub_length(self) -> float:
        return self.__cnf["hub_length"]

    @property
    def hub_offset(self) -> float:
        return self.__cnf["hub_offset"]
