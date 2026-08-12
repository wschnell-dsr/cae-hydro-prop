# -*- coding: utf-8 -*-
import math
import numpy
from enum import IntEnum

from salome.geom import geomBuilder
from typing import Any, Optional, Tuple, TypedDict, TypeAlias, Union

from .profile import Profile, ProfileFactory, ProfileCnfVariant


class SkewCnf(TypedDict):
    exponent: float
    skew_max: float


class RakeCnf(TypedDict):
    exponent: float
    rake_max: float


class ChordDistributionType(IntEnum):
    LINEAR = 0
    ELLIPTIC = 1


class ChordCnf(TypedDict):
    chord_type: str


class ChordLinearCnf(ChordCnf):
    chord_hub: float
    chord_tip: float


class ChordEllipticCnf(ChordCnf):
    chord_hub: float
    chord_tip: float


ChordCnfVariant: TypeAlias = Union[None, ChordCnf, ChordLinearCnf, ChordEllipticCnf]


class PitchDistributionType(IntEnum):
    LINEAR = 0
    QUADRATIC = 1
    EXPONENTIAL = 2


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


PitchCnfVariant: TypeAlias = Union[None, PitchCnf, PitchLinearCnf, PitchQuadraticCnf, PitchExponentialCnf]


class BladeCnf(TypedDict):
    key: str
    profile_pnts: int
    radius_hub: float
    radius_tip: float
    radius_pnts: int
    radius_eps: float
    profile_cnf: ProfileCnfVariant
    pitch_cnf: PitchCnfVariant
    chord_cnf: ChordCnfVariant
    skew_cnf: SkewCnf
    rake_cnf: RakeCnf


class Blade:
    __cnf: BladeCnf
    __factory: ProfileFactory
    __profile: Profile
    __radii: Optional[numpy.ndarray]
    __pitch: Optional[numpy.ndarray]
    __chord: Optional[numpy.ndarray]
    __EPS_X: float = 0.005
    blade: Any

    def __init__(self, arg_cnf: BladeCnf, arg_geompy: geomBuilder, arg_ref_pnt: Any, arg_ref_axis: Any):
        self.geompy = arg_geompy
        self.__cnf = arg_cnf
        self.__factory = ProfileFactory()
        self.__profile = self.__factory.create(self.__cnf["profile_cnf"])
        self.__profile.calc_norm_x_distribution(self.profile_pnts)
        self.__radii = None
        self.__pitch = None
        self.__chord = None
        self.blade = None
        self.__radii = None

        if self.pitch_type == PitchDistributionType.LINEAR.name:
            self.__radii = numpy.linspace(self.radius_hub, self.radius_tip, self.radius_pnts)
            self.__pitch = numpy.interp(self.__radii,  [self.radius_hub, self.radius_tip], [self.pitch_hub, self.pitch_tip])
        elif self.pitch_type == PitchDistributionType.QUADRATIC.name:
            self.__radii = self.radius_hub + numpy.square(numpy.linspace(0, (self.radius_tip - self.radius_hub)**0.5, self.radius_pnts))
            tmp_k = (self.pitch_tip - self.pitch_hub) / (self.radius_tip - self.radius_hub)**2
            self.__pitch = self.pitch_hub + tmp_k * numpy.square(self.__radii - self.radius_hub)
        elif self.pitch_type == PitchDistributionType.EXPONENTIAL.name:
            tmp_k = math.log(self.pitch_tip/self.pitch_hub) / (self.radius_tip - self.radius_hub)
            self.__radii = self.radius_hub + (self.radius_tip - self.radius_hub) * numpy.log((numpy.exp(numpy.linspace(0.0, 1.0, self.radius_pnts))))
            self.__pitch = self.pitch_hub * numpy.exp(tmp_k * (self.__radii - self.radius_hub))
            print(self.__radii)
            print(self.__pitch)

        if self.chord_type == ChordDistributionType.LINEAR.name:
            self.__chord = numpy.interp(self.__radii,  [self.radius_hub, self.radius_tip], [self.chord_hub, self.chord_tip])
        elif self.chord_type == ChordDistributionType.ELLIPTIC.name:
            self.__chord = self.chord_hub * numpy.sqrt(1.0 - self.__radii / self.radius_tip + self.chord_tip)

        path_pnts = []
        profile_wires = []
        for ridx in range(len(self.__radii)):
            (x_upper_z, y_upper_z), (x_lower_z, y_lower_z) = self.__profile.profile_line(self.__chord[ridx], self.__pitch[ridx])
            (x_upper, y_upper, z_upper) = self.cylinder_projection(self.__radii[ridx], x_upper_z, y_upper_z)
            (x_lower, y_lower, z_lower) = self.cylinder_projection(self.__radii[ridx], x_lower_z, y_lower_z)

            line_upper_pnts = []
            line_lower_pnts = []
            for tmp_idx in range(self.profile_pnts):
                line_upper_pnts.append(
                    self.geompy.MakeVertexWithRef(arg_ref_pnt, x_upper[tmp_idx], y_upper[tmp_idx], z_upper[tmp_idx])
                )
                line_lower_pnts.append(
                    self.geompy.MakeVertexWithRef(arg_ref_pnt, x_lower[tmp_idx], y_lower[tmp_idx], z_lower[tmp_idx])
                )

            upper_wire = self.geompy.MakeInterpol(line_upper_pnts, False)
            lower_wire = self.geompy.MakeInterpol(line_lower_pnts, False)

            profile_wire = self.geompy.MakeWire([upper_wire, lower_wire], True)
            path_pnts.append(self.geompy.MakeVertexWithRef(arg_ref_pnt, x_upper[0], y_upper[0], z_upper[0]))
            profile_wires.append(profile_wire)

        path = self.geompy.MakePolyline(path_pnts)
        pipe_shell = self.geompy.MakePipeWithDifferentSections(profile_wires, path_pnts, path, False, False, False)

        pipe_shell_bbox = self.geompy.BoundingBox(pipe_shell, True)
        ccut = self.geompy.MakeTranslationVectorDistance(
            self.geompy.MakeCutList(
                self.geompy.MakeCylinder(arg_ref_pnt, arg_ref_axis, self.radius_tip-self.radius_eps, pipe_shell_bbox[1]-pipe_shell_bbox[0]+self.__EPS_X),
                [self.geompy.MakeCylinder(arg_ref_pnt, arg_ref_axis, self.radius_hub+self.radius_eps, pipe_shell_bbox[1]-pipe_shell_bbox[0]+self.__EPS_X)],
                True
            ), arg_ref_axis, -self.__EPS_X/2.0
        )
        part = self.geompy.MakePartition([ccut], [pipe_shell], [], [], self.geompy.ShapeType["SOLID"], 0, [], 0)
        solids = self.geompy.ExtractShapes(part, self.geompy.ShapeType["SOLID"], True)

        for solid in solids:
            solid_bbox = self.geompy.BoundingBox(solid, True)
            if (
                (pipe_shell_bbox[0] - solid_bbox[0]) < self.__EPS_X and
                (pipe_shell_bbox[1] - solid_bbox[1]) < self.__EPS_X and
                (pipe_shell_bbox[2] - solid_bbox[2]) < self.__EPS_X and
                (pipe_shell_bbox[3] - solid_bbox[3]) < self.__EPS_X and
                (pipe_shell_bbox[4] - solid_bbox[4]) < self.__EPS_X and
                (pipe_shell_bbox[5] - solid_bbox[5]) < self.__EPS_X
            ):
                self.blade = solid

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
    def chord_hub(self) -> float:
        return self.__cnf["chord_cnf"]["chord_hub"]

    @property
    def chord_tip(self) -> float:
        return self.__cnf["chord_cnf"]["chord_tip"]

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
        theta_rad = arg_y / arg_r
        tmp_skew_dx = arg_r * numpy.sin(numpy.deg2rad(self.get_skew(arg_r)))
        tmp_rake = numpy.deg2rad(self.get_rake(arg_r))
        x = arg_x + tmp_skew_dx
        y = numpy.sin(theta_rad + tmp_rake) * arg_r
        z = numpy.cos(theta_rad + tmp_rake) * arg_r
        return (x, y, z)




