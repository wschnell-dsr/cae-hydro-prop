#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import argparse

os.chdir(os.environ["HYDRO_PROP_ROOT"])
sys.path.append(os.environ["HYDRO_PROP_ROOT"])

sys.argv = ["run_salome_test.py", "--test-dir=testing", "--test-pattern=*_salome_test.py"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-dir", type=str, help="")
    parser.add_argument("--test-pattern", type=str, help="")
    args = parser.parse_args()

    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(args.test_dir, pattern=args.test_pattern, top_level_dir=".")

    unittest.TextTestRunner().run(test_suite)
