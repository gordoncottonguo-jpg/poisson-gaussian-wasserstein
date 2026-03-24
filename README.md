# poisson-gaussian-wasserstein
Poisson to Gaussian approximation using Wasserstein distance
# Poisson Gaussian Approximation with Wasserstein Distance

## Project overview
This repository studies when the Gaussian distribution \(N(\lambda,\lambda)\) becomes a practical approximation to the Poisson distribution \(\mathrm{Poisson}(\lambda)\).



The project uses only the 1-Wasserstein distance as the quantitative criterion.



## Research question
For which values of \(\lambda\) is the approximation

\[
\mathrm{Poisson}(\lambda) \approx N(\lambda,\lambda)
\]

practically acceptable?



## Method
The project combines:
- theoretical motivation from the central limit theorem,
- numerical computation of the 1-Wasserstein distance,
- a normalized criterion based on \(W_1 / \sqrt{\lambda}\),
- reproducible Python code, tables, and figures.


## Main rule of thumb
Based on the current computation:
- rough approximation: \(\lambda \ge 9\),
- good approximation: \(\lambda \ge 36\).



## Repository structure
```text
poisson-gaussian-wasserstein/
├── README.md
├── report/
│   └── poisson_w1_final_report.md
├── code/
│   ├── poisson_w1_final.py
│   └── poisson_w1_make_figures.py
├── data/
│   ├── poisson_w1_metrics.csv
│   ├── poisson_w1_thresholds.csv
│   └── poisson_w1_selected.csv
└── figures/
    ├── poisson_w1_error_plots.png
    ├── poisson_w1_shape_examples.png
    └── poisson_w1_lln_clt.png
