#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" """

import logging
import logging.config
import unittest
import matplotlib.pyplot as plt

from typing import List

from hydro_prop.meshing.profile import ProfileFactory, ProfileCnfVariant, ProfileType

# pyright#: reportAttributeAccessIssue=false
# pyright#: reportUnknownMemberType=false
# pyright#: reportUnknownVariableType=false
# pyright#: reportUnknownArgumentType=false
LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": 0,
    "formatters": {"standard": {"format": "%(asctime)s %(module)s %(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s"}},
    "handlers": {"default": {"level": "INFO", "formatter": "standard", "class": "logging.StreamHandler"}},
    "loggers": {
        "": {"handlers": ["default"], "level": "DEBUG"},
        "matplotlib": {"handlers": ["default"], "level": "INFO"},
        "hydro_prop.meshing.profile": {"handlers": ["default"], "level": "DEBUG", "propagate": False}
    },
}


class TestProfile(unittest.TestCase):
    NPOINTS: int = 200
    TEST_PROFILE_CNFS: List[ProfileCnfVariant] = [
        {
            "key": "NACA 0008",
            "profile_type": ProfileType.NACA.name,
            "profile_code": "0008"
        },
        {
            "key": "MIXED_ZERO_PARABOLIC",
            "profile_type": ProfileType.MIXED.name,
            "mixed_cnf":
            {
                "camber_line_cnf": {
                    "camber_line_type": "ZERO"
                },
                "thickness_distribution_cnf": {
                    "thickness_distribution_type": "PARABOLIC",
                    "max_thickness": 0.08
                },
            }
        },
        {
            "key": "MIXED_PARABOLIC_ELLIPTIC",
            "profile_type": ProfileType.MIXED.name,
            "mixed_cnf":
            {
                "camber_line_cnf": {
                    "camber_line_type": "PARABOLIC",
                    "camber": 1.0
                },
                "thickness_distribution_cnf": {
                    "thickness_distribution_type": "ELLIPTIC",
                    "max_thickness": 0.08
                },
            }
        }
    ]

    def test_profile_plot(self):
        logging.config.dictConfig(LOGGER_CONFIG)
        logging.info("")
        tmp_factory = ProfileFactory()
        tmp_profiles = {}

        plt.clf()
        tmp_idx = 1
        for tmp_cnf in self.TEST_PROFILE_CNFS:

            try:
                tmp_profiles[tmp_cnf["key"]] = tmp_factory.create(tmp_cnf)
                tmp_profiles[tmp_cnf["key"]].calc_norm_x_distribution(self.NPOINTS)
                (x_upper, y_upper), (x_lower, y_lower) = tmp_profiles[tmp_cnf["key"]].profile_line(1.0, 1.0, 0.0, (1.0, 0.0))
                (x_camber, y_camber) = tmp_profiles[tmp_cnf["key"]].camber_line(1.0, 0.0, (1.0, 0.0))
            except Exception:
                logging.exception("Exception")

            plt.subplot(len(self.TEST_PROFILE_CNFS), 1, tmp_idx)
            plt.title(f"{tmp_cnf["key"]}")
            plt.plot(x_upper, y_upper, '-', label="Upper line", color="blue")
            plt.plot(x_camber, y_camber, '-', label="Camber line", color="red")
            plt.plot(x_lower, y_lower, '-', label="Lower line", color="green")
            plt.ylabel("y")
            plt.xlabel("x")
            plt.grid(True)
            plt.legend()
            tmp_idx += 1
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    unittest.main()
