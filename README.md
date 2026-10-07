# EEG-LGM within-family scaling-law fits

Reproduces the log-linear scaling-exponent estimates reported in Figure 2
and the main text of:

> Yu Z, Wang C. "The Non-Universal Scaling Law and Untapped
> Psychiatric-Diagnostic Value of EEG Large General Models." npj Digital
> Medicine (under revision, 2026).

## What this does

For the three model families where the primary source published its own
raw (parameter-count, performance) data points — **LaBraM** (TUAB, 3
sizes), **EEGPT** (Wang et al., NeurIPS 2024; BCIC-2A, 8 sizes, Table 6
of the original paper), and **Uni-NTFM** (TUAB, 11 sizes, pre-peak
10.3-808.2M range) — this script independently fits

&#x20;   performance = a \* ln(params\_in\_millions) + b


by ordinary least squares (`scipy.stats.linregress` on `ln(params)`),
and reports the slope and R² exactly as cited in Figure 2's panel
titles and in the manuscript text.

For **CoMET** and **PRiSE-EEG**, no raw per-point data was available
from either primary source — only their own already-published fitted
equations. Those two are *not* re-estimated here; the script states this
explicitly and reproduces them only as transcribed constants, to avoid
implying an independent fit that does not exist.

## Data provenance

All (parameter, performance) pairs are hand-extracted from the cited
primary papers and verified against them (see the manuscript's Table S2
/ Supplementary Data for full source attribution).

The EEGPT series is the model's own internal scaling ablation (Table 6 of
the NeurIPS 2024 paper): BCIC-2A, 8 sizes from 0.4M to 101M parameters.

## Run

```
pip install -r requirements.txt
python scaling\_fit.py
```

No other dependencies. Output reproduces the slope/R² values quoted in
the manuscript (Figure 2 panels A-C and Section "Scaling Law in EEG
Field").

