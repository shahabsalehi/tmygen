import pandas as pd
import numpy as np

__all__ = ["smooth_month_edges"]


def smooth_month_edges(df: pd.DataFrame,
                       hours: int = 8,
                       var_cols: list[str] | None = None) -> pd.DataFrame:
    """
    Linear ramp on each variable across +/- `hours` from month edge,
    per ISO 15927-4 §6.5. Works in-place & returns df for chaining.
    """
    if var_cols is None:
        var_cols = [c for c in df.columns
                    if c not in ("dt", "year", "month", "day", "hour")]

    # create boolean mask rows that are within `hours` of a month edge
    mask = (df.dt.dt.hour < hours) | (df.dt.dt.hour >= 24 - hours)

    for v in var_cols:
        # forward edge:  last `hours` of month i  ➔ ramp to first value of month i+1
        idx_fwd = mask & (df.dt.dt.hour >= 24 - hours)
        df.loc[idx_fwd, v] = np.linspace(
            df.loc[idx_fwd, v].iloc[0],
            df.loc[idx_fwd, v].iloc[-1],
            idx_fwd.sum()
        )
        # backward edge: first `hours` of month i+1 ➔ ramp from last of month i
        idx_bwd = mask & (df.dt.dt.hour < hours)
        df.loc[idx_bwd, v] = np.linspace(
            df.loc[idx_bwd, v].iloc[0],
            df.loc[idx_bwd, v].iloc[-1],
            idx_bwd.sum()
        )
    return df
