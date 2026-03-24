import numpy as np
import pandas as pd
from scipy.stats import poisson, norm

# Reproducible random seed
rng = np.random.default_rng(20260324)

# Lambda grid
lambdas = np.arange(1, 101)
rows = []

for lam in lambdas:
    # Dense grid used to compare Poisson and Gaussian CDFs
    x_max = int(np.ceil(lam + 8 * np.sqrt(lam) + 20))
    x = np.linspace(-1, x_max, 6000)

    # Exact Poisson CDF and matching Gaussian CDF
    F_p = poisson.cdf(np.floor(x), lam)
    F_n = norm.cdf(x, loc=lam, scale=np.sqrt(lam))

    # 1-Wasserstein distance in one dimension
    W1 = np.trapz(np.abs(F_p - F_n), x)

    # Relative Wasserstein distance using the natural scale sqrt(lambda)
    W1_rel_sd = W1 / np.sqrt(lam)

    rows.append([lam, W1, W1_rel_sd])

# Save the main metrics table
metrics = pd.DataFrame(rows, columns=['lambda', 'W1', 'W1_rel_sd'])
metrics.to_csv('poisson_w1_metrics.csv', index=False)

# Practical thresholds based only on relative Wasserstein distance
thresholds = []
for threshold in [0.10, 0.05]:
    valid = metrics.loc[metrics['W1_rel_sd'] < threshold, 'lambda']
    first_lambda = int(valid.iloc[0]) if len(valid) else None
    thresholds.append(['W1_rel_sd', threshold, first_lambda])

thresholds = pd.DataFrame(
    thresholds,
    columns=['metric', 'threshold', 'first_lambda_below_threshold']
)
thresholds.to_csv('poisson_w1_thresholds.csv', index=False)

# Selected lambda values for discussion in the report
selected = metrics[metrics['lambda'].isin([1, 2, 5, 10, 20, 30, 50, 100])]
selected.to_csv('poisson_w1_selected.csv', index=False)

# Optional LLN / CLT simulation files for supplementary illustration
lam = 20
sample = rng.poisson(lam, size=5000)
cum_mean = np.cumsum(sample) / np.arange(1, len(sample) + 1)
pd.DataFrame({'n': np.arange(1, len(sample) + 1), 'cum_mean': cum_mean}).to_csv('lln_path.csv', index=False)

n = 200
reps = 6000
means = rng.poisson(lam, size=(reps, n)).mean(axis=1)
z = np.sqrt(n) * (means - lam) / np.sqrt(lam)
pd.DataFrame({'z': z}).to_csv('clt_zscores.csv', index=False)
