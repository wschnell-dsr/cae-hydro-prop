#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import IntEnum
from typing import TypedDict, TypeAlias, Union

from .naca import NACAProfileVariant, NACAFactory
from .mixed import MixedProfile, MixedProfileCnf


ProfileVariant: TypeAlias = Union[None, NACAProfileVariant]


class ProfileType(IntEnum):
    NACA = 1
    MIXED = 2


class ProfileCnf(TypedDict):
    key: str
    profile_type: str


class NACACnf(ProfileCnf):
    profile_code: str


class MixedCnf(ProfileCnf):
    mixed_cnf: MixedProfileCnf


ProfileCnfVariant: TypeAlias = Union[NACACnf]


class ProfileFactory:

    def create(self, arg_cnf: ProfileCnfVariant) -> ProfileVariant:
        if arg_cnf["profile_type"] == ProfileType.NACA.name:
            tmp_naca_factory = NACAFactory()
            return tmp_naca_factory.create(arg_cnf["profile_code"])
        elif arg_cnf["profile_type"] == ProfileType.MIXED.name:
            return MixedProfile(arg_cnf["mixed_cnf"])
        else:
            return None
