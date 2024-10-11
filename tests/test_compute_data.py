"""Tests for statistics functions within the Compute Data layer."""
import math

import numpy as np
import numpy.testing as npt
from unittest.mock import Mock

def test_compute_data_mock_source():
    from inflammation.compute_data import analyse_data
    data_source = Mock()
    data_source.load_inflammation_data.return_value = [[[0, 2, 0]],
                                                       [[0, 1, 0]]]

    result = analyse_data(data_source)
    npt.assert_array_almost_equal(result, [0, math.sqrt(0.25), 0])
