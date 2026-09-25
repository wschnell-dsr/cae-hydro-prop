# -*- coding: utf-8 -*-
import math
import numpy
import os
import pandas

from scipy.interpolate import CubicSpline
from enum import IntEnum

from salome.geom import geomBuilder
from typing import Any, List, Optional, Tuple, TypedDict, TypeAlias, Union

from .profile import Profile, ProfileFactory, ProfileCnfVariant


class RotationDirection(IntEnum):
    LEFT = -1
    RIGHT = 1


class SkewCnf(TypedDict):
    exponent: float
    skew_max: float


class RakeCnf(TypedDict):
    exponent: float
    rake_max: float


class ChordDistributionType(IntEnum):
    LINEAR = 0
    ELLIPTIC = 1
    LINEAR_TABULATED = 2
    CUBIC_SPLINE_TABULATED = 3


class ChordCnf(TypedDict):
    chord_type: str


class ChordLinearCnf(ChordCnf):
    chord_hub: float
    chord_tip: float


class ChordEllipticCnf(ChordCnf):
    chord_hub: float
    chord_tip: float


class ChordLinearTabulatedCnf(ChordCnf):
    radius: List[float]
    chord: List[float]


class ChordCubicSplineTabulatedCnf(ChordCnf):
    radius: List[float]
    chord: List[float]


ChordCnfVariant: TypeAlias = Union[None, ChordCnf, ChordLinearCnf, ChordEllipticCnf, ChordLinearTabulatedCnf, ChordCubicSplineTabulatedCnf]


class PitchDistributionType(IntEnum):
    LINEAR = 0
    QUADRATIC = 1
    EXPONENTIAL = 2
    LINEAR_TABULATED = 3
    CUBIC_SPLINE_TABULATED = 4


class PitchCnf(TypedDict):
    pitch_type: str


class PitchLinearCnf(PitchCnf):
    pitch_hub: float
    pitch_tip: float


class PitchQuadraticCnf(PitchCnf):
    pitch_hub: float
    pitch_tip: float


class PitchExponentialCnf(PitchCnf):
    pitch_hub: float
    pitch_tip: float


class PitchLinearTabulatedCnf(ChordCnf):
    radius: List[float]
    pitch: List[float]


class PitchCubicSplineTabulatedCnf(ChordCnf):
    radius: List[float]
    pitch: List[float]


PitchCnfVariant: TypeAlias = Union[None, PitchCnf, PitchLinearCnf, PitchQuadraticCnf, PitchExponentialCnf, PitchLinearTabulatedCnf, PitchCubicSplineTabulatedCnf]


class ThicknessDistributionCnf(TypedDict):
    radius: List[float]
    thickness: List[float]


class BladeCnf(TypedDict):
    key: str
    debug: bool
    eps: float
    rotation_direction: str
    profile_pnts: int
    radius_hub: float
    radius_tip: float
    radius_pnts: int
    radius_eps: float
    profile_cnf: ProfileCnfVariant
    pitch_cnf: PitchCnfVariant
    thickness_distribution_cnf: ThicknessDistributionCnf
    chord_center: float
    chord_cnf: ChordCnfVariant
    skew_cnf: SkewCnf
    rake_cnf: RakeCnf


class Blade:
    __cnf: BladeCnf
    __factory: ProfileFactory
    __profile: Profile
    __radii: Optional[numpy.ndarray]
    __pitch: Optional[numpy.ndarray]
    __pitch_angle: Optional[numpy.ndarray]
    __chord: Optional[numpy.ndarray]
    __thickness: Optional[numpy.ndarray]
    blade: Any

    def __init__(self, arg_cnf: BladeCnf, arg_geompy: geomBuilder, arg_ref_pnt: Any, arg_ref_axis: Any):
        self.geompy = arg_geompy
        self.__ref_pnt = arg_ref_pnt
        self.__ref_axis = arg_ref_axis
        self.__cnf = arg_cnf
        self.__factory = ProfileFactory()
        self.__profile = self.__factory.create(self.__cnf["profile_cnf"])
        self.__profile.calc_norm_x_distribution(self.profile_pnts)
        self.__radii = None
        self.__pitch = None
        self.__pitch_angle = None
        self.__chord = None
        self.__thickness = None
        self.blade = None
        self.blade_shell = None
        self.__radii = numpy.linspace(self.radius_hub, self.radius_tip, self.radius_pnts)

        if self.pitch_type == PitchDistributionType.LINEAR.name:
            self.__pitch = numpy.interp(self.__radii,  [self.radius_hub, self.radius_tip], [self.pitch_hub, self.pitch_tip])
        elif self.pitch_type == PitchDistributionType.QUADRATIC.name:
            tmp_k = (self.pitch_tip - self.pitch_hub) / (self.radius_tip - self.radius_hub)**2
            self.__pitch = self.pitch_hub + tmp_k * numpy.square(self.__radii - self.radius_hub)
        elif self.pitch_type == PitchDistributionType.EXPONENTIAL.name:
            tmp_k = math.log(self.pitch_tip/self.pitch_hub) / (self.radius_tip - self.radius_hub)
            self.__pitch = self.pitch_hub * numpy.exp(tmp_k * (self.__radii - self.radius_hub))
        elif self.pitch_type == PitchDistributionType.LINEAR_TABULATED.name:
            self.__pitch = numpy.interp(self.__radii,  self.__cnf["pitch_cnf"]["radius"], self.__cnf["pitch_cnf"]["pitch"])
        elif self.pitch_type == PitchDistributionType.CUBIC_SPLINE_TABULATED.name:
            tmp_p = CubicSpline(self.__cnf["pitch_cnf"]["radius"], self.__cnf["pitch_cnf"]["pitch"])
            self.__pitch = tmp_p(self.__radii)
        self.__pitch_angle = 90.0 - numpy.degrees(numpy.arctan2(self.__pitch, (2.0*self.__radii*numpy.pi)))

        if self.chord_type == ChordDistributionType.LINEAR.name:
            self.__chord = numpy.interp(self.__radii,  [self.radius_hub, self.radius_tip], [self.chord_hub, self.chord_tip])
        elif self.chord_type == ChordDistributionType.ELLIPTIC.name:
            self.__chord = self.chord_hub * numpy.sqrt(1.0 - self.__radii / self.radius_tip + self.chord_tip)
        elif self.chord_type == ChordDistributionType.LINEAR_TABULATED.name:
            self.__chord = numpy.interp(self.__radii,  self.__cnf["chord_cnf"]["radius"], self.__cnf["chord_cnf"]["chord"])
        elif self.chord_type == ChordDistributionType.CUBIC_SPLINE_TABULATED.name:
            tmp_cs = CubicSpline(self.__cnf["chord_cnf"]["radius"], self.__cnf["chord_cnf"]["chord"])
            self.__chord = tmp_cs(self.__radii)
        self.__thickness = numpy.interp(self.__radii,  self.__cnf["thickness_distribution_cnf"]["radius"], self.__cnf["thickness_distribution_cnf"]["thickness"])

    def export_info(self, arg_dir: str):
        # export geo data to file
        blade_df = pandas.DataFrame({
            "r [m]": self.__radii,
            "r/R []": self.__radii/self.__radii[-1],
            "c [m]": self.__chord,
            "c/D []": 0.5*self.__chord/self.__radii[-1],
            "p [m]": self.__pitch,
            "p/D []": 0.5*self.__pitch/self.__radii[-1],
            "p [deg]": 90.0 - self.__pitch_angle,
            "rake[deg]": self.get_rake(self.__radii),
            "skew[deg]": self.get_skew(self.__radii),
        })
        blade_df.to_csv(os.path.join(arg_dir, "blade.csv"))

        (x_upper, y_upper), (x_lower, y_lower) = self.__profile.norm_profile_line()
        (x_camber, y_camber) = self.__profile.norm_camber_line()
        profile_df = pandas.DataFrame({
            "x": x_camber,
            "c": y_camber,
            "yu": y_upper,
            "yl": y_lower,
        })
        profile_df.to_csv(os.path.join(arg_dir, "profile.csv"))

    def gen_blade(self):
        self.gen_shell()
        if self.blade_shell is not None:
            self.gen_solid()

    def gen_shell(self):
        try:
            path_pnts = []
            profile_wires = []
            for ridx in range(len(self.__radii)):
                (x_upper_z, y_upper_z), (x_lower_z, y_lower_z) = self.__profile.profile_line(
                    self.__chord[ridx], self.__thickness[ridx], self.__pitch_angle[ridx], (self.chord_center * self.__chord[ridx], 0.0)
                )
                (x_upper, y_upper, z_upper) = self.cylinder_projection(self.__radii[ridx], x_upper_z - self.chord_center * self.__chord[ridx], y_upper_z)
                (x_lower, y_lower, z_lower) = self.cylinder_projection(self.__radii[ridx], x_lower_z - self.chord_center * self.__chord[ridx], y_lower_z)

                line_upper_pnts = []
                line_lower_pnts = []
                for tmp_idx in range(self.profile_pnts):
                    line_upper_pnts.append(
                        self.geompy.MakeVertexWithRef(self.__ref_pnt, x_upper[tmp_idx], y_upper[tmp_idx], z_upper[tmp_idx])
                    )
                    line_lower_pnts.append(
                        self.geompy.MakeVertexWithRef(self.__ref_pnt, x_lower[tmp_idx], y_lower[tmp_idx], z_lower[tmp_idx])
                    )

                upper_wire = self.geompy.MakeInterpol(line_upper_pnts, False)
                lower_wire = self.geompy.MakeInterpol(line_lower_pnts, False)

                profile_wire = self.geompy.MakeWire([upper_wire, lower_wire], True)
                path_pnts.append(self.geompy.MakeVertexWithRef(self.__ref_pnt, x_upper[0], y_upper[0], z_upper[0]))
                profile_wires.append(profile_wire)
                if self.debug:
                    self.geompy.addToStudy(profile_wire, self.key+"_profile_wire_"+str(ridx))

            path = self.geompy.MakePolyline(path_pnts)
            if self.debug:
                self.geompy.addToStudy(path, self.key+"_path")
            self.blade_shell = self.geompy.MakePipeWithDifferentSections(profile_wires, path_pnts, path, False, False, False)
            if self.debug:
                self.geompy.addToStudy(self.blade_shell, self.key+"_blade_shell")
        except Exception as e:
            print(e)

    def gen_solid(self):
        try:
            pipe_shell_bbox = self.geompy.MakeBoundingBox(self.blade_shell, True)
            if self.debug:
                self.geompy.addToStudy(pipe_shell_bbox, self.key+"_pipe_shell_bbox")

            pipe_shell_bbox = self.geompy.BoundingBox(self.blade_shell, True)
            ccut = self.geompy.MakeTranslationVectorDistance(
                self.geompy.MakeCutList(
                    self.geompy.MakeCylinder(self.__ref_pnt, self.__ref_axis, self.radius_tip-self.radius_eps, pipe_shell_bbox[1]-pipe_shell_bbox[0]+2.0*self.eps),
                    [self.geompy.MakeCylinder(self.__ref_pnt, self.__ref_axis, self.radius_hub+self.radius_eps, pipe_shell_bbox[1]-pipe_shell_bbox[0]+2.0*self.eps)],
                    True
                ), self.__ref_axis, -self.eps
            )
            if self.debug:
                self.geompy.addToStudy(ccut, self.key+"_ccut")
            part = self.geompy.MakePartition([ccut], [self.blade_shell], [], [], self.geompy.ShapeType["SOLID"], 0, [], 0)
            if self.debug:
                self.geompy.addToStudy(part, self.key+"_part")
            solids = self.geompy.ExtractShapes(part, self.geompy.ShapeType["SOLID"], True)

            for solid in solids:
                solid_bbox = self.geompy.BoundingBox(solid, True)
                if (
                    abs(pipe_shell_bbox[0] - solid_bbox[0]) < self.eps and
                    abs(pipe_shell_bbox[1] - solid_bbox[1]) < self.eps and
                    abs(pipe_shell_bbox[2] - solid_bbox[2]) < self.eps and
                    abs(pipe_shell_bbox[3] - solid_bbox[3]) < self.eps and
                    abs(pipe_shell_bbox[4] - solid_bbox[4]) < self.eps and
                    abs(pipe_shell_bbox[5] - solid_bbox[5]) < self.eps
                ):
                    self.blade = solid
        except Exception as e:
            print(e)

    @property
    def key(self) -> str:
        return self.__cnf["key"]

    @property
    def debug(self) -> bool:
        return self.__cnf["debug"]

    @property
    def eps(self) -> float:
        return self.__cnf["eps"]

    @property
    def rotation_direction(self) -> float:
        for tmp_dir in RotationDirection:
            if self.__cnf["rotation_direction"] == tmp_dir.name:
                return float(tmp_dir.value)

    @property
    def profile_pnts(self) -> int:
        return self.__cnf["profile_pnts"]

    @property
    def radius_hub(self) -> float:
        return self.__cnf["radius_hub"]

    @property
    def radius_tip(self) -> float:
        return self.__cnf["radius_tip"]

    @property
    def radius_eps(self) -> float:
        return self.__cnf["radius_eps"]

    @property
    def radius_pnts(self) -> int:
        return self.__cnf["radius_pnts"]

    @property
    def chord_type(self) -> ChordDistributionType:
        return self.__cnf["chord_cnf"]["chord_type"]

    @property
    def chord_center(self) -> float:
        return self.__cnf["chord_center"]

    @property
    def chord_hub(self) -> float:
        if self.chord_type in [ChordDistributionType.LINEAR.name, ChordDistributionType.ELLIPTIC.name]:
            return self.__cnf["chord_cnf"]["chord_hub"]
        else:
            return numpy.interp([self.radius_hub],  self.__cnf["chord_cnf"]["radius"], self.__cnf["chord_cnf"]["chord"])[0]

    @property
    def chord_tip(self) -> float:
        if self.chord_type in [ChordDistributionType.LINEAR.name, ChordDistributionType.ELLIPTIC.name]:
            return self.__cnf["chord_cnf"]["chord_tip"]
        else:
            return numpy.interp([self.radius_tip],  self.__cnf["chord_cnf"]["radius"], self.__cnf["chord_cnf"]["chord"])[0]

    @property
    def pitch_type(self) -> str:
        return self.__cnf["pitch_cnf"]["pitch_type"]

    @property
    def pitch_hub(self) -> float:
        return self.__cnf["pitch_cnf"]["pitch_hub"]

    @property
    def pitch_tip(self) -> float:
        return self.__cnf["pitch_cnf"]["pitch_tip"]

    @property
    def skew_exp(self) -> float:
        return self.__cnf["skew_cnf"]["exponent"]

    @property
    def skew_max(self) -> float:
        return self.__cnf["skew_cnf"]["skew_max"]

    @property
    def rake_exp(self) -> float:
        return self.__cnf["rake_cnf"]["exponent"]

    @property
    def rake_max(self) -> float:
        return self.__cnf["rake_cnf"]["rake_max"]

    def get_skew(self, arg_r: numpy.ndarray) -> numpy.ndarray:
        tmp_skew = self.skew_max * numpy.power((arg_r-self.radius_hub)/(self.radius_tip-self.radius_hub), self.skew_exp)
        return tmp_skew

    def get_rake(self, arg_r: numpy.ndarray) -> numpy.ndarray:
        tmp_rake = self.rake_max * numpy.power((arg_r-self.radius_hub)/(self.radius_tip-self.radius_hub), self.rake_exp)
        return tmp_rake

    def cylinder_projection(self, arg_r: float, arg_x: numpy.ndarray, arg_y: numpy.ndarray) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
        theta_rad = self.rotation_direction * arg_y / arg_r
        tmp_skew_dx = arg_r * numpy.sin(numpy.deg2rad(self.get_skew(arg_r)))
        tmp_rake = numpy.deg2rad(self.get_rake(arg_r))
        x = arg_x + tmp_skew_dx
        y = numpy.sin(theta_rad + tmp_rake) * arg_r
        z = numpy.cos(theta_rad + tmp_rake) * arg_r
        return (x, y, z)
