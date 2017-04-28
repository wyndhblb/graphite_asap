import pytz

from graphite_api.render.datalib import TimeSeries

from datetime import datetime

from graphite_asap.functions import ASAP

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest.mock import patch, call, MagicMock
except ImportError:
    from mock import patch, call, MagicMock


class TestCase(unittest.TestCase):
    pass


class TestAsap(TestCase):
    request = {
        'args': ({}, {}),
        'startTime': datetime(1970, 1, 1, 0, 0, 0, 0, pytz.utc),
        'endTime': datetime(1970, 1, 1, 0, 9, 0, 0, pytz.utc),
        'data': [],
    }

    def gen_series_list(self, start=0, use_none=False):

        data = range(start, start + 15)
        if use_none:
            n = [None for d in data]
            data = n

        seriesList = [
            TimeSeries('stuff.things.more.things', start, start + 15, 1, data)
        ]
        for series in seriesList:
            series.pathExpression = series.name
        return seriesList

    def gen_series_list_partial_none(self, start=0):

        data = list(range(start, start + 15))
        data[2] = None
        data[8] = None

        seriesList = [
            TimeSeries('stuff.things.more.things', start, start + 15, 1, data)
        ]
        for series in seriesList:
            series.pathExpression = series.name
        return seriesList

    def test_asap_normal(self):
        series = self.gen_series_list(10)

        def mock_evaluate(reqCtx, tokens, store=None):
            return self.gen_series_list()

        with patch('graphite_asap.functions.evaluateTokens', mock_evaluate):
            smoothed = ASAP(self.request, series, 10)
            should = [
                0.0,
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
                11.0,
                12.75]
            gots = [x for x in smoothed[0]]
            assert(gots == should)

    def test_asap_none(self):
        series = self.gen_series_list(10, True)

        def mock_evaluate(reqCtx, tokens, store=None):
            return self.gen_series_list(10, True)

        with patch('graphite_asap.functions.evaluateTokens', mock_evaluate):
            smooth = ASAP(self.request, series, 10)
            assert(len(smooth) == 1)

    def test_asap_some_none(self):
        series = self.gen_series_list_partial_none(10)

        def mock_evaluate(*args):
            return self.gen_series_list_partial_none(10)

        with patch('graphite_asap.functions.evaluateTokens', mock_evaluate):
            smoothed = ASAP(self.request, series, 10)
            should = [
                10.0,
                11.0,
                0.0,
                13.0,
                14.0,
                15.0,
                16.0,
                17.0,
                0.0,
                19.0,
                20.0,
                21.0,
                22.75]
            gots = [x for x in smoothed[0]]
            assert(gots == should)
