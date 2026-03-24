import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import poisson, norm
import plotly.graph_objects as go
from plotly.subplots import make_subplots

base = Path('.')
metrics_path = base / 'poisson_w1_metrics.csv'
if not metrics_path.exists():
    raise FileNotFoundError('poisson_w1_metrics.csv not found. Run poisson_w1_final.py first.')

metrics = pd.read_csv(metrics_path)

# Figure 1: W1 and relative W1 vs lambda
fig1 = make_subplots(rows=1, cols=2, subplot_titles=['Absolute W1', 'Relative W1'])
fig1.add_trace(go.Scatter(x=metrics['lambda'], y=metrics['W1'], mode='lines', name='W1'), row=1, col=1)
fig1.add_trace(go.Scatter(x=metrics['lambda'], y=metrics['W1_rel_sd'], mode='lines', name='W1/sqrt(lambda)'), row=1, col=2)
fig1.update_xaxes(title_text='lambda', row=1, col=1)
fig1.update_yaxes(title_text='W1', row=1, col=1)
fig1.update_xaxes(title_text='lambda', row=1, col=2)
fig1.update_yaxes(title_text='rel W1', row=1, col=2)
fig1.update_layout(
    title='Wasserstein errors vs lambda (1-100)',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
)
fig1.write_image('poisson_w1_error_plots_clean.png')
with open('poisson_w1_error_plots_clean.png.meta.json', 'w') as f:
    json.dump({
        'caption': 'Wasserstein error plots',
        'description': 'Two-panel line chart of absolute and relative Wasserstein errors against lambda.'
    }, f)

# Figure 2: Poisson vs Gaussian examples
rng = np.random.default_rng(20260324)
example_lams = [5, 20, 50]
fig2 = make_subplots(rows=1, cols=3, subplot_titles=[f'lambda={lam}' for lam in example_lams])
for j, lam in enumerate(example_lams, start=1):
    s = rng.poisson(lam, size=50000)
    bins = np.arange(s.min()-0.5, s.max()+1.5, 1)
    fig2.add_trace(
        go.Histogram(
            x=s,
            xbins=dict(start=bins[0], end=bins[-1], size=1),
            histnorm='probability density',
            name=f'Poisson {lam}',
            opacity=0.55,
            showlegend=(j == 1)
        ),
        row=1, col=j
    )
    x = np.linspace(max(0, lam - 4*np.sqrt(lam)), lam + 4*np.sqrt(lam), 400)
    fig2.add_trace(
        go.Scatter(x=x, y=norm.pdf(x, lam, np.sqrt(lam)), mode='lines', name='Gaussian', showlegend=(j == 1)),
        row=1, col=j
    )
    fig2.update_xaxes(title_text='count', row=1, col=j)
fig2.update_yaxes(title_text='density', row=1, col=1)
fig2.update_layout(
    title='Poisson and Gaussian shapes (5,20,50)',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
    barmode='overlay'
)
fig2.write_image('poisson_w1_shape_examples_clean.png')
with open('poisson_w1_shape_examples_clean.png.meta.json', 'w') as f:
    json.dump({
        'caption': 'Poisson Gaussian shape examples',
        'description': 'Three-panel chart comparing Poisson histograms with matching Gaussian densities for lambda 5, 20, and 50.'
    }, f)

# Figure 3: LLN and CLT supplementary figure
lam = 20
sample = rng.poisson(lam, size=5000)
cum_mean = np.cumsum(sample) / np.arange(1, len(sample) + 1)
reps = 6000
n = 200
means = rng.poisson(lam, size=(reps, n)).mean(axis=1)
z = np.sqrt(n) * (means - lam) / np.sqrt(lam)

fig3 = make_subplots(rows=1, cols=2, subplot_titles=['LLN', 'CLT'])
fig3.add_trace(go.Scatter(x=np.arange(1, len(cum_mean)+1), y=cum_mean, mode='lines', name='sample mean'), row=1, col=1)
fig3.add_trace(go.Scatter(x=[1, len(cum_mean)], y=[lam, lam], mode='lines', name='true mean'), row=1, col=1)
fig3.add_trace(go.Histogram(x=z, histnorm='probability density', nbinsx=50, name='z scores', opacity=0.6), row=1, col=2)
xx = np.linspace(-4, 4, 400)
fig3.add_trace(go.Scatter(x=xx, y=norm.pdf(xx), mode='lines', name='N(0,1)'), row=1, col=2)
fig3.update_xaxes(title_text='n', row=1, col=1)
fig3.update_yaxes(title_text='mean', row=1, col=1)
fig3.update_xaxes(title_text='z score', row=1, col=2)
fig3.update_yaxes(title_text='density', row=1, col=2)
fig3.update_layout(
    title='LLN and CLT checks for Poisson data',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
    barmode='overlay'
)
fig3.write_image('poisson_w1_lln_clt_clean.png')
with open('poisson_w1_lln_clt_clean.png.meta.json', 'w') as f:
    json.dump({
        'caption': 'LLN and CLT figure',
        'description': 'Two-panel figure showing convergence of the sample mean and a histogram of standardized sample means versus the standard normal density.'
    }, f)
