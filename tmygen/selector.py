from __future__ import annotations
import pandas as pd
from pathlib import Path
from .fs_rank import fs_rank_month, FSResult
from .smoother import smooth_month_edges

__all__ = ["generate_tmy"]


def _load_weights(path: Path | str) -> dict[int, dict[str, float]]:
    """Reads a 12×N CSV (month 1…12 as index) into {month: {var: wt}}."""
    df = pd.read_csv(path, index_col=0)
    return {int(m): df.loc[int(m)].to_dict() for m in df.index}


def generate_tmy(weather_csv: Path | str,
                 weight_csv: Path | str,
                 top_k: int = 1,
                 tie_break_var: str | None = "windspeed") -> pd.DataFrame:
    """
    End-to-end generator: pick months, stitch, smooth.

    Parameters
    ----------
    weather_csv : path to 30-year hourly weather file.
    weight_csv  : 12×N weight-factor table.
    top_k       : keep k best FS months before tie-break.
    tie_break_var: if given, choose among ties by min σ of that variable.

    Returns
    -------
    DataFrame of hourly weather for the new TMY.
    """
    w = pd.read_csv(weather_csv, parse_dates=["dt"])
    w["year"] = w.dt.dt.year
    w["month"] = w.dt.dt.month
    w["day"] = w.dt.dt.day

    weights = _load_weights(weight_csv)

    chosen: list[FSResult] = []
    for m in range(1, 13):
        ranked = fs_rank_month(w, m, weights[m])[:top_k]
        if len(ranked) > 1 and tie_break_var:
            ranked.sort(
                key=lambda r: r.daily_mean[tie_break_var].std())
        chosen.append(ranked[0])

    # Concatenate hourly records in calendar order ---------------
    out_parts = []
    for r in chosen:
        subset = w.query("year == @r.year and month == @r.month").copy()
        out_parts.append(subset)

    df = pd.concat(out_parts, ignore_index=True)
    df = smooth_month_edges(df)
    return df
