# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_optimal_dispatch.ipynb.

# %% auto 0
__all__ = ['redistribute_daily_production']

# %% ../../nbs/01_optimal_dispatch.ipynb 2
import pandas as pd

from .data import *

# %% ../../nbs/01_optimal_dispatch.ipynb 15
def redistribute_daily_production(
    df: pd.Series,                 # production data
    daily_distribution: list[str]  # distribution at each our
) -> pd.DataFrame:
    if len(daily_distribution) != 24:
        raise ValueError("Daily distribution needs a value for each hour.")
    
    df_hour = pd.DataFrame(data={"distribution": daily_distribution, "hour": list(range(24))})
    df_hour["distribution"] /= df_hour["distribution"].sum()
    return (
        df
        .to_frame("prod")
        .assign(hour=lambda d: d.index.hour)
        .reset_index()
        .merge(df_hour, how="left", on="hour")
        .set_index("time")
        .groupby(pd.Grouper(freq="1d"), group_keys=False)
        .apply(lambda d: d["distribution"] * d["prod"].sum())
        .to_frame("prod")
    )

