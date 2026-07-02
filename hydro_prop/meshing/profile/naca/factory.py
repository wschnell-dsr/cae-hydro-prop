#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .base import NACAProfile, NACASeries, profile_code_series
from .naca_4 import NACA4Profile
from .naca_5 import NACA5Profile
from .naca_6 import NACA6Profile

from typing import TypeAlias
from typing import Any, Dict, Union


NACAProfileVariant: TypeAlias = Union[None, NACAProfile, NACA4Profile, NACA5Profile, NACA6Profile]

NACA_FACTORY_MAP: Dict[NACASeries, Any] = {
    NACASeries.NACA_4: NACA4Profile,
    NACASeries.NACA_5: NACA5Profile,
    NACASeries.NACA_6: NACA6Profile
}


class NACAFactory:

    def create(self, arg_profile_code: str) -> NACAProfileVariant:
        tmp_naca_series = profile_code_series(arg_profile_code)
        if tmp_naca_series == NACASeries.UNKNOWN:
            return None
        return NACA_FACTORY_MAP[tmp_naca_series](arg_profile_code)
