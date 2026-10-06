#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

os.chdir(os.environ["HYDRO_PROP_ROOT"])
sys.path.append(os.environ["HYDRO_PROP_ROOT"])

sys.argv = ["run_salome_propeller_test.py", "--study=run/study_creator_1", "--mesh=mesh_p10_c7"]

if __name__ == "__main__":

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("testing", pattern="*propeller_salome_test.py", top_level_dir=".")

    unittest.TextTestRunner().run(test_suite)
