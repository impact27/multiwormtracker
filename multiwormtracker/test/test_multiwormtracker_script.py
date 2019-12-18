#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2019 Quentin Peter

This file is part of multiwormtracker.

multiwormtracker is distributed under CC BY-NC-SA version 4.0. You should have
recieved a copy of the licence along with multiwormtracker. If not, see
https://creativecommons.org/licenses/by-nc-sa/4.0/.
"""
import os
import json
import multiprocessing as mp
import pytest
import shutil
import filecmp

from multiwormtracker.multiwormtracker_script import (
    run_tracker, print_example_frame, print_images)


def test_run_tracker(tmpdir):
    """Test if we can recreate the output."""
    test_folder = os.path.dirname(__file__)
    test_output_folder = os.path.join(test_folder, 'test_output')
    with open(os.path.join(test_output_folder, 'settings.json')) as f:
        settings = json.load(f)
    os.chdir(test_folder)
    queue = mp.Queue()
    if not os.path.exists("test_output_tmp"):
        os.mkdir("test_output_tmp")
    try:
        settings['save_as'] = "test_output_tmp"
        settings["stdout prefix"] = "[1]"
        print_data, results = run_tracker(settings, queue)
        print_example_frame(settings, *print_data)
        print_images(settings, results)

        dircomp = filecmp.dircmp(
            'test_output', 'test_output_tmp',
            ignore=filecmp.DEFAULT_IGNORES + ['.DS_Store']
            )

        # Assert all the files in test_output are in test_output_tmp
        assert not dircomp.left_only

    finally:
        shutil.rmtree("test_output_tmp")


if __name__ == "__main__":
    pytest.main()
