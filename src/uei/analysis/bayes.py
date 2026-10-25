"""Bayesian polling average: local-level (random-walk) state-space model.

    x_t = x_{t-1} + eta_t,           eta_t ~ N(0, q)        (daily drift in true margin)
    y_i = x_{t_i} + h_k + eps_i,     eps_i ~ N(0, s_i^2 + tau^2)

s_i^2 is the poll's sampling variance, tau^2 is non-sampling error (frame,
weighting, mode), and h_k is an optional pollster house effect. With Gaussian
assumptions the posterior is computed exactly by a Kalman filter followed by
a Rauch–Tung–Striebel smoother. The prior is centred on a reference margin
(e.g. the previous result) with a wide SD so that polls dominate.

The output is a credible interval for the *polling-average* margin; it does
not include the historical error of polls relative to results.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .averages import primary_versions, sampling_variance_margin


def kalman_trend(polls: pd.DataFrame, prior_mean: float = 0.0, prior_sd: float = 15.0,
                 drift_sd_per_day: float = 0.25, tau: float = 2.0,
                 house: pd.Series | None = None, end=None) -> pd.DataFrame:
    d = primary_versions(polls)
    if d.empty:
        return pd.DataFrame()
    d = d.assign(t=pd.to_datetime(d["end_date"]))
    days = pd.date_range(d["t"].min(), pd.Timestamp(end) if end else d["t"].max(), freq="D")
    n = d["sample_size"].fillna(d["sample_size"].median() if d["sample_size"].notna().any() else 600)
    obs_var = sampling_variance_margin(d["pct_dem"], d["pct_rep"], n) + tau ** 2
    y = d["margin"].astype(float).values
    if house is not None:
        y = y - d["pollster"].map(house).fillna(0.0).values
    by_day = {}
    for t, yi, vi in zip(d["t"], y, obs_var):
        by_day.setdefault(t, []).append((yi, vi))

    q = drift_sd_per_day ** 2
    m, P = prior_mean, prior_sd ** 2
    mf, Pf, mp, Pp = [], [], [], []
    for t in days:
        m_pred, P_pred = m, P + q
        mp.append(m_pred); Pp.append(P_pred)
        m, P = m_pred, P_pred
        for yi, vi in by_day.get(t, []):
            K = P / (P + vi)
            m = m + K * (yi - m)
            P = (1 - K) * P
        mf.append(m); Pf.append(P)
    # RTS smoother
    ms, Ps = mf[:], Pf[:]
    for i in range(len(days) - 2, -1, -1):
        C = Pf[i] / Pp[i + 1]
        ms[i] = mf[i] + C * (ms[i + 1] - mp[i + 1])
        Ps[i] = Pf[i] + C ** 2 * (Ps[i + 1] - Pp[i + 1])
    ms, sd = np.array(ms), np.sqrt(np.array(Ps))
    return pd.DataFrame({"date": days, "mean": ms, "sd": sd,
                         "lo90": ms - 1.645 * sd, "hi90": ms + 1.645 * sd,
                         "filtered": np.array(mf)})
