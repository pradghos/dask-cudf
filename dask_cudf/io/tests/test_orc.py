import os

import dask_cudf
import dask.dataframe as dd
import cudf

import pytest

# import pyarrow.orc as orc

cur_dir = os.path.dirname(__file__)
sample_orc = os.path.join(cur_dir, "sample.orc")


def test_read_orc_defaults():
    df1 = cudf.read_orc(sample_orc)
    df2 = dask_cudf.read_orc(sample_orc)
    df2.head().to_pandas()
    dd.assert_eq(df1, df2, check_index=False)


# engine pyarrow fails
# https://github.com/rapidsai/cudf/issues/1595
@pytest.mark.parametrize("engine", ["cudf"])
@pytest.mark.parametrize("columns", [["time", "date"], ["time"]])
def test_read_orc_cols(engine, columns):
    df1 = cudf.read_orc(sample_orc, engine=engine, columns=columns)

    df2 = dask_cudf.read_orc(sample_orc, engine=engine, columns=columns)

    dd.assert_eq(df1, df2, check_index=False)
