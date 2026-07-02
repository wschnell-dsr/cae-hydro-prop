#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import math
import salome
import salome_notebook
import SMESH
import SALOMEDS
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder

try:
    from unv2ccx import Converter
except ModuleNotFoundError:
    Converter = None

from typing import TypedDict


class BoatPropConfig(TypedDict):
    diameter = 0.0400        # diameter [m]
    pitch = 0.0310        # pitch [m]
    num_blades = 2  # Anzahl Blätter
    blade_thickness = 0.002  # Blattdicke [mm]
    hub_diameter = 10.0     # Nabendurchmesser [mm]
    hub_length = 15.0       # Nabenlänge [mm]
    skew_angle = 3.0        # Skew-Winkel [Grad]
    rake_angle = 0.0        # Rake-Winkel [Grad]
    bar = 0.5               # Blattflächenverhältnis (BAR)


DEFAULT_CONFIG: BoatPropConfig = {
    "hub_diameter": 0.006,
    "hub_length": 0.015,
    "diameter": 0.0400,
    "pitch": 0.0310,
    "num_blades": 2,
    "blade_thickness": 0.002,
    "skew_angle": 3.0,
    "rake_angle": 0.0,
    "bar": 0.5
}


class Profile:

    def __init__(self):
        pass

    def get(self):
        tmp_points = []
        tmp_points.append((0.000, 0.000))
        tmp_points.append((0.000, 0.015))
        tmp_points.append((0.001, 0.015))
        tmp_points.append((0.001, 0.000))
        return tmp_points


def cylinder_projection(arg_profile, arg_radius):
    tmp_points = []
    for tmp_coords in arg_profile:
        tmp_points


class BoatProp:
    __config: BoatPropConfig

    def __init__(self, arg_config: BoatPropConfig):
        salome.salome_init()
        self.__config = arg_config
        self.notebook = salome_notebook.NoteBook()
        self.notebook.set("hub_diameter", self.__config["hub_diameter"])
        self.notebook.set("hub_radius", "hub_diameter/2")
        self.notebook.set("hub_length", self.__config["hub_length"])

        self.geompy = geomBuilder.New()
        self.smesh = smeshBuilder.New()

    def generate_geom(self):

        OO = self.geompy.MakeVertex(0, 0, 0)
        OX = self.geompy.MakeVectorDXDYDZ(1, 0, 0)
        OY = self.geompy.MakeVectorDXDYDZ(0, 1, 0)
        OZ = self.geompy.MakeVectorDXDYDZ(0, 0, 1)
        self.geompy.addToStudy(OO, 'OO')
        self.geompy.addToStudy(OX, 'OX')
        self.geompy.addToStudy(OY, 'OY')
        self.geompy.addToStudy(OZ, 'OZ')

        self.hub = self.geompy.MakeCylinder(
            self.geompy.MakeVertex(0, 0, 0),
            self.geompy.MakeVectorDXDYDZ(0, 0, 1),
            "hub_radius",
            "hub_length"
        )
        self.geompy.addToStudy(self.hub, 'hub')
        '''
        self.vt_in_center = self.geompy.MakeVertex(0, 0, "thickness")
        self.vt_out_center = self.geompy.MakeVertex(0, 0, 0)
        self.vt_in_radius = self.geompy.MakeVertex("bottom_radius", 0, "thickness")
        self.vt_out_radius = self.geompy.MakeVertex("bottom_radius", 0, 0)
        self.vt_in_top = self.geompy.MakeVertex("outer_in_radius", 0, "top")
        self.vt_out_top = self.geompy.MakeVertex("outer_radius", 0, "top")
        self.vt_arc_center = self.geompy.MakeVertex("bottom_radius", 0, "top")
        self.geompy.addToStudy(self.vt_in_center, 'vt_in_center')
        self.geompy.addToStudy(self.vt_out_center, 'vt_out_center')

        self.ln_bot = self.geompy.MakeLineTwoPnt(self.vt_out_center, self.vt_out_radius)
        self.ln_out_arc = self.geompy.MakeArcCenter(
            self.vt_arc_center, self.vt_out_radius, self.vt_out_top, False)
        self.ln_top = self.geompy.MakeLineTwoPnt(self.vt_out_top, self.vt_in_top)
        self.ln_in_arc = self.geompy.MakeArcCenter(self.vt_arc_center, self.vt_in_radius, self.vt_in_top, False)
        self.ln_in = self.geompy.MakeLineTwoPnt(self.vt_in_radius, self.vt_in_center)
        self.ln_cen = self.geompy.MakeLineTwoPnt(self.vt_out_center, self.vt_in_center)
        self.geompy.addToStudy(self.ln_bot, 'ln_bot')
        self.geompy.addToStudy(self.ln_out_arc, 'ln_out_arc')
        self.geompy.addToStudy(self.ln_top, 'ln_top')
        self.geompy.addToStudy(self.ln_in_arc, 'ln_in_arc')
        self.geompy.addToStudy(self.ln_in, 'ln_in')
        self.geompy.addToStudy(self.ln_cen, 'ln_cen')

        self.wire = self.geompy.MakeWire([self.ln_bot, self.ln_out_arc, self.ln_top, self.ln_in_arc, self.ln_in, self.ln_cen], 1e-07)
        self.face = self.geompy.MakeFaceWires([self.wire], 1)
        self.solid = self.geompy.MakeRevolution(self.face, OZ, 360*math.pi/180.0)

        self.geompy.addToStudy(self.wire, 'wire')
        self.geompy.addToStudy(self.face, 'face')
        self.geompy.addToStudy(self.solid, 'solid')

        self.boundary_ids = {
            "inside": [],
            "outside": [],
            "bottom_inside": [],
            "bottom_outside": [],
            "rim": [],
        }
        self.boundary_pts_ids = []
        self.boundary_grps = {}
        self.boundary_pts = {}
        self.all_faces = self.geompy.ExtractShapes(self.solid, self.geompy.ShapeType["FACE"], True)
        for tmp_face in self.all_faces:
            if self.geompy.MinDistanceComponents(tmp_face, self.vt_out_center)[0] < 1e-5:
                self.boundary_ids["bottom_outside"].append(tmp_face)
            elif self.geompy.MinDistanceComponents(tmp_face, self.vt_in_center)[0] < 1e-5:
                self.boundary_ids["bottom_inside"].append(tmp_face)
            elif self.geompy.MinDistanceComponents(tmp_face, self.vt_in_top)[0] < 1e-5 and \
                    self.geompy.MinDistanceComponents(tmp_face, self.vt_out_top)[0] < 1e-5:
                self.boundary_ids["rim"].append(tmp_face)
            elif self.geompy.MinDistanceComponents(tmp_face, self.vt_arc_center)[0] - self.notebook.get("bowl_radius") < 1e-5:
                self.boundary_ids["inside"].append(tmp_face)
            elif self.geompy.MinDistanceComponents(tmp_face, self.vt_arc_center)[0] - self.notebook.get("top") < 1e-5:
                self.boundary_ids["outside"].append(tmp_face)

        self.boundary_grps["bottom_outside"] = self.geompy.CreateGroup(self.solid, self.geompy.ShapeType["FACE"])
        self.geompy.UnionList(self.boundary_grps["bottom_outside"], self.boundary_ids["bottom_outside"])
        self.geompy.addToStudyInFather(self.solid, self.boundary_grps["bottom_outside"], "bottom_outside")
        self.boundary_grps["bottom_outside"].SetColor(SALOMEDS.Color(1, 0, 0))

        self.boundary_grps["bottom_inside"] = self.geompy.CreateGroup(self.solid, self.geompy.ShapeType["FACE"])
        self.geompy.UnionList(self.boundary_grps["bottom_inside"], self.boundary_ids["bottom_inside"])
        self.geompy.addToStudyInFather(self.solid, self.boundary_grps["bottom_inside"], "bottom_inside")
        self.boundary_grps["bottom_inside"].SetColor(SALOMEDS.Color(0, 1, 0))

        self.boundary_grps["rim"] = self.geompy.CreateGroup(self.solid, self.geompy.ShapeType["FACE"])
        self.geompy.UnionList(self.boundary_grps["rim"], self.boundary_ids["rim"])
        self.geompy.addToStudyInFather(self.solid, self.boundary_grps["rim"], "rim")
        self.boundary_grps["rim"].SetColor(SALOMEDS.Color(0, 0, 1))

        self.boundary_grps["inside"] = self.geompy.CreateGroup(self.solid, self.geompy.ShapeType["FACE"])
        self.geompy.UnionList(self.boundary_grps["inside"], self.boundary_ids["inside"])
        self.geompy.addToStudyInFather(self.solid, self.boundary_grps["inside"], "inside")
        self.boundary_grps["inside"].SetColor(SALOMEDS.Color(0, 1, 1))

        self.boundary_grps["outside"] = self.geompy.CreateGroup(self.solid, self.geompy.ShapeType["FACE"])
        self.geompy.UnionList(self.boundary_grps["outside"], self.boundary_ids["outside"])
        self.geompy.addToStudyInFather(self.solid, self.boundary_grps["outside"], "outside")
        self.boundary_grps["outside"].SetColor(SALOMEDS.Color(0, 1, 1))
        '''

    def generate_mesh(self):
        pass
        '''
        self.mesh = self.smesh.Mesh(self.solid, 'mesh')
        NETGEN_1D_2D_3D = self.mesh.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
        NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
        NETGEN_3D_Parameters_1.SetMaxSize(0.025)
        NETGEN_3D_Parameters_1.SetMinSize(0.00005)
        NETGEN_3D_Parameters_1.SetSecondOrder(0)
        NETGEN_3D_Parameters_1.SetOptimize(1)
        NETGEN_3D_Parameters_1.SetFineness(3)
        NETGEN_3D_Parameters_1.SetChordalError(-1)
        NETGEN_3D_Parameters_1.SetChordalErrorEnabled(0)
        NETGEN_3D_Parameters_1.SetUseSurfaceCurvature(1)
        NETGEN_3D_Parameters_1.SetFuseEdges(1)
        NETGEN_3D_Parameters_1.SetQuadAllowed(0)
        NETGEN_3D_Parameters_1.SetCheckChartBoundary(0)
        self.smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN_3D_Parameters_1')
        isDone = self.mesh.Compute()

        if isDone:
            self.boundary_face_mesh_grp = {}
            self.boundary_point_mesh_grp = {}
            for tmp_boundary_key in self.boundary_grps:
                self.boundary_face_mesh_grp[tmp_boundary_key] = self.mesh.GroupOnGeom(self.boundary_grps[tmp_boundary_key], tmp_boundary_key, SMESH.FACE)
                tmp_criteria = [self.smesh.GetCriterion(SMESH.NODE, SMESH.FT_BelongToGeom, SMESH.FT_Undefined, self.boundary_grps[tmp_boundary_key])]
                tmp_filter = self.smesh.GetFilterFromCriteria(tmp_criteria)
                tmp_filter.SetMesh(self.mesh.GetMesh())
                self.boundary_point_mesh_grp[tmp_boundary_key] = self.mesh.GroupOnFilter(SMESH.NODE, tmp_boundary_key, tmp_filter)

            all_faces = self.mesh.GetElementsByType(SMESH.FACE)
            for tmp_face in all_faces:
                tmp_is_no_boundary = True
                for tmp_keys in self.boundary_ids:
                    if tmp_face in self.boundary_ids[tmp_keys]:
                        tmp_is_no_boundary = False
                    if tmp_is_no_boundary:
                        self.mesh.RemoveElements([tmp_face])
                        # alle 1D-Elemente (Kanten) holen

            all_edges = self.mesh.GetElementsByType(SMESH.EDGE)
            # boundary_ids: dict mit Listen/Sets von element-IDs (wie in deinem Beispiel)
            # mache daraus eine Menge zur schnellen Abfrage
            boundary_edge_ids = set()
            for k, v in self.boundary_ids.items():
                boundary_edge_ids.update(v)

            # Elemente sammeln, die NICHT in boundary sind
            to_remove = [eid for eid in all_edges if eid not in boundary_edge_ids]

            # einmalig entfernen (wenn Liste nicht leer)
            if to_remove:
                self.mesh.RemoveElements(to_remove)
        '''

    def export_to_unv(self, arg_file: str) -> str:
        pass
        '''
        try:
            unv_file_name = arg_file+".unv"
            self.mesh.ExportUNV(unv_file_name, 0)
            return unv_file_name
        except Exception:
            logging.exception('ExportUNV() failed.')
            return ""
        '''

    def export_to_med(self, arg_file: str) -> str:
        pass
        '''
        try:
            med_file_name = arg_file+".med"
            self.mesh.ExportMED(med_file_name, 0)
            return med_file_name
            pass
        except Exception:
            logging.exception('ExportMED() failed.')
            return ""
        '''

    def export_to_inp(self, arg_file: str) -> str:
        pass
        '''
        unv_file = self.export_to_unv(arg_file)
        if Converter is not None:
            tmp_converter = Converter(unv_file)
            tmp_converter.run()
            return tmp_converter.inp_file_name
        else:
            return ""
        '''


if __name__ == "__main__":

    tmp_boat_prop = BoatProp(DEFAULT_CONFIG)
    tmp_boat_prop.generate_geom()
    #tmp_boat_prop.generate_mesh()
