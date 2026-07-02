#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import IntEnum
from typing import TypedDict, TypeAlias, Union

from .naca import NACAProfileVariant, NACAFactory


ProfileVariant: TypeAlias = Union[None, NACAProfileVariant]


class ProfileType(IntEnum):
    NACA = 1


class ProfileCnf(TypedDict):
    key: str
    profile_type: ProfileType


class NACACnf(ProfileCnf):
    profile_code: str


ProfileCnfVariant: TypeAlias = Union[NACACnf]


class ProfileFactory:

    def create(self, arg_cnf: ProfileCnfVariant) -> ProfileVariant:
        if arg_cnf["profile_type"] == ProfileType.NACA:
            tmp_naca_factory = NACAFactory()
            return tmp_naca_factory.create(arg_cnf["profile_code"])
        else:
            return None
