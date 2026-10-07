#!/usr/bin/env python3
"""
scaling_fit.py — reproduces the within-family log-linear scaling-exponent
estimates reported in Figure 2 and the Abstract of:
  Yu Z, Wang C. "The Non-Universal Scaling Law and Untapped
  Psychiatric-Diagnostic Value of EEG Large General Models." npj Digital
  Medicine (under revision, 2026).

For the three families where we extracted the family's own raw
(parameter-count, performance) pairs from the primary paper
(LaBraM, EEGPT-internal, Uni-NTFM), this script fits
    performance = a * ln(params_in_millions) + b
by ordinary least squares (scipy.stats.linregress on ln(params)) and
reports the slope "a" and R^2, exactly as cited in the Figure 2 panel
titles and in the Methods/Results text.

For CoMET and PRiSE-EEG, no raw per-point data was available from the
primary source — only the family's own already-published fitted
equation. Those two slopes are therefore NOT re-estimated here; they
are reproduced as directly transcribed constants from the cited papers,
and this script says so explicitly rather than presenting them as an
independent fit.

Run:  python scaling_fit.py
Needs: numpy, scipy (pip install numpy scipy)
"""
from scipy.stats import linregress
import numpy as np

# ---- Family A: LaBraM (Jiang et al., ICLR 2024), 3 released sizes ----
# TUAB Balanced Accuracy vs. parameter count (millions), as reported in
# the LaBraM paper.
labram_params_M = [5.8, 46, 369]
labram_tuab_bacc = [0.8140, 0.8226, 0.8258]

# ---- Family B: EEGPT internal ablation (Wang et al., NeurIPS 2024) ----
# BCIC-2A Balanced Accuracy across the model's own 8 internal size
# variants (0.4-101 M parameters; Table 6 of the EEGPT paper)
eegpt_params_M = [0.4, 0.5, 1.6, 6.4, 19, 25, 76, 101]
eegpt_bciciv2a_bacc = [0.4919, 0.5003, 0.5158, 0.5418, 0.5453, 0.5648,
                       0.5447, 0.5846]

# ---- Family C: Uni-NTFM (fixed 10,000h pretraining), 11 sizes ----
# TUAB Balanced Accuracy (%) vs. parameter count (millions)
untfm_params_M = [10.3, 48.3, 108.8, 203.2, 299.9, 392.4, 496.3, 600.3,
                  704.2, 808.2, 912.2]
untfm_tuab_bacc_pct = [61.32, 61.79, 62.68, 63.05, 63.72, 64.83, 65.57,
                        66.01, 66.34, 66.29, 65.98]
# Uni-NTFM is non-monotonic past 808.2M (overfitting/capacity-mismatch
# past the peak) -- the log-linear fit below uses only the pre-peak,
# monotonic-regime points (<=808.2M), consistent with how the slope is
# described in the main text.
_peak_idx = untfm_params_M.index(808.2) + 1
untfm_fit_params_M = untfm_params_M[:_peak_idx]
untfm_fit_bacc_pct = untfm_tuab_bacc_pct[:_peak_idx]


def fit_log_linear(params_M, performance, label, performance_is_pct=False):
    x = np.log(params_M)
    y = np.array(performance, dtype=float)
    if performance_is_pct:
        y = y / 100.0
    res = linregress(x, y)
    print(f"{label}:")
    print(f"    n = {len(params_M)} points, param range "
          f"{min(params_M):.1f}-{max(params_M):.1f} M")
    print(f"    slope (per ln(M))      = {res.slope:.4f}")
    print(f"    intercept              = {res.intercept:.4f}")
    print(f"    R^2                    = {res.rvalue**2:.3f}")
    print()
    return res.slope, res.rvalue**2


def main():
    print("=" * 70)
    print("Within-family log-linear scaling fits (independently computed "
          "in this script)")
    print("=" * 70)
    fit_log_linear(labram_params_M, labram_tuab_bacc, "LaBraM (TUAB, 3 sizes)")
    fit_log_linear(eegpt_params_M, eegpt_bciciv2a_bacc,
                   "EEGPT internal (BCIC-2A, 8 sizes)")
    fit_log_linear(untfm_fit_params_M, untfm_fit_bacc_pct,
                   "Uni-NTFM (TUAB, pre-peak monotonic regime, "
                   f"{len(untfm_fit_params_M)} of 11 sizes)",
                   performance_is_pct=True)

    print("=" * 70)
    print("CoMET and PRiSE-EEG: NOT independently fit here. No raw "
          "per-point data was available from the primary source for "
          "either model -- only the family's own already-published "
          "fitted equation. Reproduced as transcribed constants:")
    print("=" * 70)
    print("  CoMET  (Yue et al.): BAcc = 0.013 * ln(params_M) + 0.568, "
          "R^2 = 0.949  [as reported in the original paper]")
    print("  PRiSE-EEG (Li et al.): BAcc = 0.010 * ln(params_M) + 0.699, "
          "R^2 = 0.940  [as reported in the original paper]")


if __name__ == "__main__":
    main()
