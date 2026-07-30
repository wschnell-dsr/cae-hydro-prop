# -*- coding: utf-8 -*-
from enum import IntEnum
from typing import Any, TypedDict, Literal, Optional, Union
from salome.smesh import smeshBuilder


class NetGenFineness(IntEnum):
    COARSE = 1
    MODERATE = 2
    FINE = 3
    VERY_FINE = 4
    CUSTOM = 5


class MeshParameters(TypedDict):
    algorithm: Union[str, smeshBuilder.NETGEN_1D2D3D, smeshBuilder.GMSH]
    min_size: float
    max_size: float

    fineness: Optional[NetGenFineness]
    optimize: Optional[Union[str, bool]]
    second_order: Optional[Union[str, bool]]


def create_mesh(
    arg_smesh: smeshBuilder,
    arg_geometry,
    arg_key: str,
    arg_params: MeshParameters,
) -> Any:
    """
    """
    # Mesh erstellen
    mesh = arg_smesh.Mesh(arg_geometry, arg_key)
    mesh_builder: Optional[Union[smeshBuilder.NETGEN_1D2D3D, smeshBuilder.GMSH]] = None
    if isinstance(arg_params["algorithm"], str):
        if arg_params["algorithm"] == "NETGEN_1D2D3D":
            mesh_builder = smeshBuilder.NETGEN_1D2D3D
        elif arg_params["algorithm"] == "GMSH":
            mesh_builder = smeshBuilder.GMSH
    else:
        mesh_builder = arg_params["algorithm"]
    tmp_algo = mesh.Tetrahedron(algo=mesh_builder)

    # Gemeinsame Parameter setzen
    params = tmp_algo.Parameters()
    params.SetMinSize(arg_params["min_size"])
    params.SetMaxSize(arg_params["max_size"])
    if arg_params["algorithm"] == smeshBuilder.NETGEN_1D2D3D:
        if arg_params["fineness"] is not None and arg_params["fineness"] != "None":
            params.SetFineness(arg_params["fineness"])
        if arg_params["optimize"] is not None and arg_params["optimize"] != "None":
            params.SetSecondOrder(arg_params["optimize"])
        if arg_params["second_order"] is not None and arg_params["second_order"] != "None":
            params.SetOptimize(arg_params["second_order"])
    elif arg_params["algorithm"] == smeshBuilder.GMSH:
        pass

    return mesh
