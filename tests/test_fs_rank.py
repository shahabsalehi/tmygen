import pandas as pd
from tmygen.fs_rank import fs_rank_month

def test_fs_simple():
    # build a synthetic dataframe: 2 vars × 2 years × 3 days
    data = {
        "dt": pd.date_range("2000-01-01", periods=3*24, freq="H").tolist() +
              pd.date_range("2001-01-01", periods=3*24, freq="H").tolist(),
    }
    df = pd.DataFrame(data)
    df["temp"] = range(len(df))
    df["dni"] = range(len(df))[::-1]
    df["year"] = df.dt.dt.year
    df["month"] = 1
    df["day"] = df.dt.dt.day

    result = fs_rank_month(df, month=1, weights={"temp": 0.5, "dni": 0.5})
    assert len(result) == 2
    assert result[0].fs_score <= result[1].fs_score
