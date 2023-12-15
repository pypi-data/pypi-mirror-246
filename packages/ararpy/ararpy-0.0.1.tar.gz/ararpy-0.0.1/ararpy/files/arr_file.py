#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ==========================================
# Copyright 2023 Yang 
# webarar - arr_file
# ==========================================
#
#
#

# === External imports ===
import os
import pickle
from ararpy.smp import (initial as initial, sample as samples)

Sample = samples.Sample
Info = samples.Info
Table = samples.Table
Plot = samples.Plot
Set = samples.Plot.Set


def to_sample(file_path, sample_name: str = ""):
    """
    file_path: full path of input file
    name： samplename
    return sample instance
    """
    try:
        with open(file_path, 'rb') as f:
            sample = pickle.load(f)
    except (Exception, BaseException):
        raise ValueError(f"Fail to open arr file: {file_path}")
    # Check arr version
    # recalculation will not be applied automatically
    sample = check_version(sample)
    return sample


def save(file_path, sample: Sample):
    """ Save arr project as arr files

    Parameters
    ----------
    file_path : str, filepath
    sample : Sample instance

    Returns
    -------
    str, file name
    """
    file_path = os.path.join(file_path, f"{sample.Info.sample.name}.arr")
    with open(file_path, 'wb') as f:
        f.write(pickle.dumps(sample))
    # with open(file_path, 'w') as f:  # save serialized json data to a readable text
    #     f.write(basic_funcs.getJsonDumps(sample))
    return f"{sample.Info.sample.name}.arr"


def check_version(sample: Sample):
    """

    Parameters
    ----------
    sample

    Returns
    -------

    """
    print(f"Arr Version: {sample.ArrVersion}")
    if sample.ArrVersion != samples.VERSION:
        initial.re_set_smp(sample)
    return sample

