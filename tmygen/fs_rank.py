from __future__ import annotations

import pandas as pd
import numpy as np
from dataclasses import dataclass

__all__ = ["fs_rank_month", "FSResult"]


@dataclass(slots=True)
class FSResult:
    """Holds FS statistics for one (month, year) candidate."""
    month: int
    year: int
    fs_score: float      # weighted Σ FS across variables
    daily_mean: pd.DataFrame  # (n_days × vars) daily means


def _fs_distance(sample: np.ndarray, reference: np.ndarray) -> float:
    """
    Finkelstein–Schafer distance between two CDFs (ref §3.3 of paper).
    Both arrays must be 1-D, equal length, *already sorted*.
    """
    cdf_s = np.linspace(1 / len(sample), 1, len(sample))
    cdf_r = np.linspace(1 / len(reference), 1, len(reference))
    return np.abs(cdf_s - cdf_r).max()


def fs_rank_month(df_hourly: pd.DataFrame,
                  month: int,
                  weights: dict[str, float],
                  group_col: str = "year") -> list[FSResult]:
    """
    Computes FS score for *every* year of a given calendar month.

    Parameters
    ----------
    df_hourly: DataFrame with 'year', 'month', 'day' columns plus variables.
    month:     1–12 calendar month to process.
    weights:   mapping {variable: weight}. Must sum to 1.0.
    group_col: column that identifies individual years (default 'year').

    Returns
    -------
    list[FSResult], sorted by ascending fs_score (best first).
    """
    # 1. daily means -------------------------------------------
    vars_ = list(weights)
    daily = (df_hourly.query("month == @month")
                        .groupby([group_col, "day"])[vars_]
                        .mean()
                        .reset_index())

    # 2. reference CDF built from *all* years’ daily means -----
    ref_sorted = {v: np.sort(daily[v].values) for v in vars_}

    results: list[FSResult] = []
    for yr, grp in daily.groupby(group_col, sort=True):
        # grp is n_day × vars
        score = 0.0
        for v, w in weights.items():
            dist = _fs_distance(np.sort(grp[v].values), ref_sorted[v])
            score += w * dist
        results.append(FSResult(month, int(yr), score, grp.set_index("day")))

    return sorted(results, key=lambda r: r.fs_score)
