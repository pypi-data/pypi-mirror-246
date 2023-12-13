"""Test NaN handling."""

import numpy as np
import pytest
import xarray as xr
import pint

ureg = pint.UnitRegistry()


@pytest.xfail
def test_assign_nan(opulent_ds):
    da = opulent_ds["CO2"]
    da.pr.loc[{"area": "COL"}] = np.nan


@pytest.xfail
def test_assign_nan_numpy():
    ar = [1.0, 2.0] * ureg.meter
    ar[0] = np.array([np.nan])


@pytest.xfail
def test_assign_nan_xarray():
    da = (
        xr.DataArray(
            [[1.0, 2.0], [3.0, 4.0]], coords={"a": ["a", "b"], "b": ["c", "d"]}
        )
        * ureg.meter
    )
    da.loc[{"a": "b"}] = np.nan
