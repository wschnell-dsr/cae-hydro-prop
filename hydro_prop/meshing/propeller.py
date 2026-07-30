# -*- coding: utf-8 -*-
import os
from salome.geom import geomBuilder
from typing import Any, Optional, TypedDict
from salome.smesh import smeshBuilder
import  SMESH, SALOMEDS

from .meshing import MeshParameters, create_mesh


from .blade import Blade, BladeCnf

try:
    from unv2ccx import Converter
except ModuleNotFoundError:
    Converter = None


class PropCnf(TypedDict):
    n_blades: int
    hub_length: float
    blade_offset: float
    blade_cnf: BladeCnf


class Propeller:
    __cnf: PropCnf
    geompy: geomBuilder
    blade: Any
    blades_cmp: Any
    blades: Any
    hub: Any
    propeller: Any

    __DETECT_SELF_INTERSECTIONS: bool = False
    __REMOVE_EXTRA_EDGES: bool = False
    __BB_TOL: float = 1e-5

    def __init__(self, arg_cnf: PropCnf, arg_geompy: geomBuilder, arg_smesh: smeshBuilder, arg_ref_pnt: Any, arg_ref_axis: Any):
        self.geompy = arg_geompy
        self.smesh = arg_smesh
        self.__cnf = arg_cnf
        self.ref_pnt_hub = arg_ref_pnt
        self.ref_axis = arg_ref_axis

    def gen_geom(self, arg_key: Optional[str]):

        if arg_key:
            self.geompy.addToStudy(self.ref_pnt_hub, f"{arg_key}_ref_pnt_hub")
            self.geompy.addToStudy(self.ref_axis, f"{arg_key}ref_axis")

        self.ref_pnt_blades = self.geompy.MakeTranslationVectorDistance(self.ref_pnt_hub, self.ref_axis, self.blade_offset)
        self.geompy.addToStudy(self.ref_pnt_blades, "ref_pnt_blades")

        self.blade = Blade(self.blade_cnf, self.geompy, self.ref_pnt_blades, self.ref_axis)
        self.blades_cmp = self.geompy.MultiRotate1DNbTimes(self.blade.blade, self.ref_axis, self.n_blades)
        self.blades = self.geompy.ExtractShapes(self.blades_cmp, self.geompy.ShapeType["SOLID"], True)
        self.hub = self.geompy.MakeCylinder(self.ref_pnt_hub, self.ref_axis, self.hub_radius, self.hub_length)
        self.hub_cap = self.geompy.MakeTranslationVectorDistance(
            self.geompy.MakeSpherePntR(self.ref_pnt_hub, self.hub_radius), self.ref_axis, self.hub_length
        )

        # Cutting
        for tmp_blade_idx in range(len(self.blades)):
            self.blades[tmp_blade_idx] = self.geompy.MakeCutList(self.blades[tmp_blade_idx], [self.hub])
        self.hub_cap = self.geompy.MakeCutList(self.hub_cap, [self.hub])

        # Fuse
        fuse_list = [self.hub, self.hub_cap]
        for tmp_blade_idx in range(len(self.blades)):
            fuse_list.append(self.blades[tmp_blade_idx])
        self.propeller = self.geompy.MakeFuseList(fuse_list, self.__DETECT_SELF_INTERSECTIONS, self.__REMOVE_EXTRA_EDGES)

        if arg_key:
            self.geompy.addToStudy(self.propeller, arg_key)
            self.geompy.addToStudy(self.hub, f"{arg_key}_hub")
            self.geompy.addToStudy(self.hub_cap, f"{arg_key}_hub_cap")
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

        self.boundary_ids = {}
        for tmp_face in self.propeller_faces:
            belongs_to_blade = False
            tmp_face_bb = self.geompy.BoundingBox(tmp_face)
            for blidx, blade_faces in self.blade_faces.items():
                for tmp_bl_face in blade_faces:
                    tmp_bl_face_bb = self.geompy.BoundingBox(tmp_bl_face)
                    if self.is_same_bb(tmp_face_bb, tmp_bl_face_bb):
                        if f"blade_{blidx}" not in self.boundary_ids:
                            self.boundary_ids[f"blade_{blidx}"] = []
                        self.boundary_ids[f"blade_{blidx}"].append(tmp_face)
                        belongs_to_blade = True
            if not belongs_to_blade:
                if self.geompy.MinDistance(tmp_face, self.ref_pnt_hub) < self.__BB_TOL:
                    if "hub_front" not in self.boundary_ids:
                        self.boundary_ids["hub_front"] = []
                    self.boundary_ids["hub_front"].append(tmp_face)
                else:
                    if "hub" not in self.boundary_ids:
                        self.boundary_ids["hub"] = []
                    self.boundary_ids["hub"].append(tmp_face)

        self.boundary_grps = {}
        for key, ids in self.boundary_ids.items():
            self.boundary_grps[key] = self.geompy.CreateGroup(self.propeller, self.geompy.ShapeType["FACE"])
            self.geompy.UnionList(self.boundary_grps[key], self.boundary_ids[key])
            self.geompy.addToStudyInFather(self.propeller, self.boundary_grps[key], key)

    def gen_mesh(self, arg_key: Optional[str], arg_mesh_params: MeshParameters):

        self.propeller_mesh = create_mesh(self.smesh, self.propeller, arg_key, arg_mesh_params)

        self.mesh_on_geom_boundaries = []
        for tmp_key in self.boundary_grps:
            self.mesh_on_geom_boundaries.append((tmp_key, self.propeller_mesh.GroupOnGeom(self.boundary_grps[tmp_key], tmp_key, SMESH.FACE)))

        is_done = self.propeller_mesh.Compute()
        if is_done:
            self.propeller_mesh.CheckCompute()

    def export_mesh(self, arg_dir: str):
        try:
            self.propeller_mesh.ExportUNV(os.path.join(arg_dir, "propeller.unv"), 0)
        except Exception:
            print('ExportUNV() failed. Invalid file name?')

        for tmp_bnd in self.mesh_on_geom_boundaries:
            self.propeller_mesh.ExportSTL(os.path.join(arg_dir, f"propeller_boundary_{tmp_bnd[0]}.stl"), 1, tmp_bnd[1])

        with open(os.path.join(arg_dir, "propeller.stl"), 'w') as tmp_outfile:
            for tmp_bnd in self.mesh_on_geom_boundaries:
                tmp_file = os.path.join(arg_dir, f"propeller_boundary_{tmp_bnd[0]}.stl")
                with open(tmp_file) as tmp_infile:
                    for line in tmp_infile:
                        tmp_outfile.write(line)

    def is_same_bb(self, arg_bb1, arg_bb2) -> bool:
        is_same = True
        for idx in range(6):
            if abs(arg_bb1[idx] - arg_bb2[idx]) > self.__BB_TOL:
                is_same = False
        return is_same

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
    def hub_radius(self) -> float:
        return self.__cnf["hub_radius"]

    @property
    def blade_offset(self) -> float:
        return self.__cnf["blade_offset"]
