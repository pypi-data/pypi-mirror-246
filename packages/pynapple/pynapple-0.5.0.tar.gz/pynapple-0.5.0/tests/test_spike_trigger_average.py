# -*- coding: utf-8 -*-
# @Author: gviejo
# @Date:   2022-08-29 17:27:02
# @Last Modified by:   Guillaume Viejo
# @Last Modified time: 2023-12-12 18:10:30
#!/usr/bin/env python

"""Tests of spike trigger average for `pynapple` package."""

import pynapple as nap
import numpy as np
import pandas as pd
import pytest
# from matplotlib.pyplot import *


def test_compute_spike_trigger_average():
    ep = nap.IntervalSet(0, 100)
    feature = nap.Tsd(
        t=np.arange(0, 101, 0.01), d=np.zeros(int(101 / 0.01)), time_support=ep
    )
    t1 = np.arange(1, 100)
    x = np.arange(100, 10000, 100)
    feature[x] = 1.0
    spikes = nap.TsGroup(
        {0: nap.Ts(t1), 1: nap.Ts(t1 - 0.1), 2: nap.Ts(t1 + 0.2)}, time_support=ep
    )

    sta = nap.compute_event_trigger_average(spikes, feature, 0.2, (0.6, 0.6), ep)

    output = np.zeros((7, 3))
    output[3, 0] = 0.05
    output[4, 1] = 0.05
    output[2, 2] = 0.05

    assert isinstance(sta, nap.TsdFrame)
    assert sta.shape == output.shape
    np.testing.assert_array_almost_equal(sta, output)

    feature = nap.TsdFrame(
        t=feature.index.values, d=feature.values[:,None], time_support=ep
    )
    sta = nap.compute_event_trigger_average(spikes, feature, 0.2, (0.6, 0.6), ep)
    np.testing.assert_array_almost_equal(sta, output)

def test_compute_spike_trigger_average_add_nan():
    ep = nap.IntervalSet(0, 110)
    feature = nap.Tsd(
        t=np.arange(0, 110, 0.01), d=np.zeros(int(110 / 0.01)), time_support=ep
    )
    t1 = np.arange(1, 100)
    x = np.arange(100, 10000, 100)
    feature[x] = 1.0
    spikes = nap.TsGroup(
        {0: nap.Ts(t1), 1: nap.Ts(t1 - 0.1), 2: nap.Ts(t1 + 0.2)}, time_support=ep
    )

    feature[-1001:] = np.nan

    sta = nap.compute_event_trigger_average(spikes, feature, 0.2, (0.6, 0.6), ep)

    output = np.zeros((7, 3))
    output[3, 0] = 0.05
    output[4, 1] = 0.05
    output[2, 2] = 0.05

    assert isinstance(sta, nap.TsdFrame)
    assert sta.shape == output.shape
    np.testing.assert_array_almost_equal(sta, output)

def test_compute_spike_trigger_average_raise_error():
    ep = nap.IntervalSet(0, 101)
    feature = nap.Tsd(
        t=np.arange(0, 101, 0.01), d=np.zeros(int(101 / 0.01)), time_support=ep
    )
    t1 = np.arange(1, 101) + 0.01
    x = np.arange(100, 10000, 100)+1
    feature[x] = 1.0    

    with pytest.raises(Exception) as e_info:
        nap.compute_event_trigger_average(feature, feature, 0.1, (0.5, 0.5), ep)
    assert str(e_info.value) == "group should be a TsGroup."

    feature = nap.TsdFrame(
        t=np.arange(0, 101, 0.01), d=np.random.rand(int(101 / 0.01), 3), time_support=ep
    )
    spikes = nap.TsGroup(
        {0: nap.Ts(t1), 1: nap.Ts(t1 - 0.1), 2: nap.Ts(t1 + 0.2)}, time_support=ep
    )
    with pytest.raises(Exception) as e_info:
        nap.compute_event_trigger_average(spikes, feature, 0.1, (0.5, 0.5), ep)
    assert str(e_info.value) == "Feature should be a Tsd or a TsdFrame with one column"

    


def test_compute_spike_trigger_average_time_unit():
    ep = nap.IntervalSet(0, 100)
    feature = pd.Series(index=np.arange(0, 101, 0.01), data=np.zeros(int(101 / 0.01)))
    t1 = np.arange(1, 100)
    feature.loc[t1] = 1.0
    spikes = nap.TsGroup(
        {0: nap.Ts(t1), 1: nap.Ts(t1 - 0.1), 2: nap.Ts(t1 + 0.2)}, time_support=ep
    )

    feature = nap.Tsd(feature, time_support=ep)

    sta = nap.compute_event_trigger_average(spikes, feature, 0.2, (0.6, 0.6), ep)

    output = np.zeros((7, 3))
    output[3, 0] = 0.05
    output[4, 1] = 0.05
    output[2, 2] = 0.05

    binsize = 0.2
    windowsize = np.array([0.6, 0.6])

    for tu, fa in zip(["s", "ms", "us"], [1, 1e3, 1e6]):
        sta = nap.compute_event_trigger_average(
            spikes, feature, binsize * fa, tuple(windowsize * fa), ep, time_unit=tu
        )
        assert isinstance(sta, nap.TsdFrame)
        assert sta.shape == output.shape
        np.testing.assert_array_almost_equal(sta.values, output)


def test_compute_spike_trigger_average_multiple_epochs():
    ep = nap.IntervalSet(0, 101)
    feature = pd.Series(index=np.arange(0, 101, 0.01), data=np.zeros(int(101 / 0.01)))
    t1 = np.arange(1, 101)
    feature.loc[t1] = 1.0
    spikes = nap.TsGroup({0: nap.Ts(t1)}, time_support=ep)

    ep2 = nap.IntervalSet(start=[0, 40], end=[10, 60])

    feature = nap.Tsd(feature, time_support=ep)

    sta = nap.compute_event_trigger_average(spikes, feature, 0.1, (0.5, 0.5), ep2)

    output = np.zeros(int((0.5 / 0.1) * 2 + 1))
    count = spikes[0].count(0.1, ep2).values
    feat = feature.bin_average(0.1, ep2).values
    output[5] = np.dot(count, feat)/count.sum()

    assert isinstance(sta, nap.TsdFrame)
    np.testing.assert_array_almost_equal(sta.values.flatten(), output)
