#!/usr/bin/env pythonG
# -*- coding: utf-8 -*-
"""
Automated tests for all defined adjoint sources. Essentially just checks
that they all work and do something.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2015
:license:
    BSD 3-Clause ("BSD New" or "BSD Simplified")
"""
from __future__ import absolute_import, division, print_function

import numpy as np
import pytest

import pyadjoint


@pytest.fixture(params=list(pyadjoint.AdjointSource._ad_srcs.keys()))
def adj_src(request):
    """
    Fixture returning the name of all adjoint sources.
    """
    return request.param


def test_normal_adjoint_source_calculation(adj_src):
    """
    Make sure everything at least runs. Executed for every adjoint source type.
    """

    obs, syn = pyadjoint.utils.get_example_data()
    obs = obs.select(component="Z")[0]
    syn = syn.select(component="Z")[0]
    # start, end = pyadjoint.utils.EXAMPLE_DATA_PDIFF

    window = [[2076., 2418.0]]

    if adj_src == "waveform_misfit":
        config = pyadjoint.ConfigWaveForm(min_period=30.0,
                                          max_period=75.0,
                                          taper_type='hann',
                                          taper_percentage=0.3)

    if adj_src == "cc_traveltime_misfit":
        config = pyadjoint.ConfigCrossCorrelation(min_period=30.0,
                                                  max_period=75.0,
                                                  taper_type='hann',
                                                  taper_percentage=0.3,
                                                  measure_type='dt',
                                                  dt_sigma_min=1.0,
                                                  dlna_sigma_min=0.5)

    if adj_src == "multitaper_misfit":
        config = pyadjoint.ConfigMultiTaper(min_period=30.0,
                                            max_period=75.0,
                                            lnpt=15,
                                            transfunc_waterlevel=1.0E-10,
                                            water_threshold=0.02,
                                            ipower_costaper=10,
                                            min_cycle_in_window=3,
                                            taper_percentage=0.3,
                                            taper_type='hann',
                                            mt_nw=4,
                                            num_taper=5,
                                            dt_fac=2.0,
                                            phase_step=1.5,
                                            err_fac=2.5,
                                            dt_max_scale=3.5,
                                            measure_type='dt',
                                            dt_sigma_min=1.0,
                                            dlna_sigma_min=0.5,
                                            use_cc_error=False,
                                            use_mt_error=False)

    a_src = pyadjoint.calculate_adjoint_source(adj_src_type=adj_src,
                                               observed=obs,
                                               synthetic=syn,
                                               config=config,
                                               window=window,
                                               adjoint_src=True,
                                               plot=False)

    assert a_src.adjoint_source.any()
    assert a_src.misfit >= 0.0

    assert isinstance(a_src.adjoint_source, np.ndarray)


def test_no_adjoint_src_calculation_is_honored(adj_src):
    """
    If no adjoint source is requested, it should not be returned/calculated.
    """
    obs, syn = pyadjoint.utils.get_example_data()
    obs = obs.select(component="Z")[0]
    syn = syn.select(component="Z")[0]
    window = [[2076., 2418.0]]

    if adj_src == "waveform_misfit":
        config = pyadjoint.ConfigWaveForm(min_period=30.0,
                                          max_period=75.0,
                                          taper_type='hann',
                                          taper_percentage=0.3)

    if adj_src == "cc_traveltime_misfit":
        config = pyadjoint.ConfigCrossCorrelation(min_period=30.0,
                                                  max_period=75.0,
                                                  taper_type='hann',
                                                  taper_percentage=0.3,
                                                  measure_type='dt',
                                                  dt_sigma_min=1.0,
                                                  dlna_sigma_min=0.5)

    if adj_src == "multitaper_misfit":
        config = pyadjoint.ConfigMultiTaper(min_period=30.0,
                                            max_period=75.0,
                                            lnpt=15,
                                            transfunc_waterlevel=1.0E-10,
                                            water_threshold=0.02,
                                            ipower_costaper=10,
                                            min_cycle_in_window=3,
                                            taper_percentage=0.3,
                                            taper_type='hann',
                                            mt_nw=4,
                                            num_taper=5,
                                            dt_fac=2.0,
                                            phase_step=1.5,
                                            err_fac=2.5,
                                            dt_max_scale=3.5,
                                            measure_type='dt',
                                            dt_sigma_min=1.0,
                                            dlna_sigma_min=0.5,
                                            use_cc_error=False,
                                            use_mt_error=False)

    a_src = pyadjoint.calculate_adjoint_source(
        adj_src_type=adj_src, observed=obs,
        synthetic=syn, config=config, window=window,
        adjoint_src=False, plot=False)
    assert a_src.adjoint_source is None

    # But the misfit should nonetheless be identical as if the adjoint
    # source would have been calculated.

    # assert a_src.misfit == pyadjoint.calculate_adjoint_source(
    #    adj_src_type=adj_src, observed=obs,
    #    synthetic=syn, config=config, window=window,
    #    adjoint_src=True, plot=False).misfit

    # pyadjoint.calculate_adjoint_source(
    # adj_src, obs, syn, 20, 100, start, end, adjoint_src=True).misfit
