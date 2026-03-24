# Approximation gaussienne d’une loi de Poisson : quand est-elle valable ?

## 1. Problem 
We study when the Gaussian distribution $N(\lambda,\lambda)$ becomes a practically useful approximation to the Poisson distribution $\mathrm{Poisson}(\lambda)$.

This final version uses only the 1-Wasserstein distance as the quantitative criterion.

## 2. Theory 
Let \(X_1,\dots,X_n\) be i.i.d. Poisson random variables with parameter \(\lambda\). Then the sum of independent Poisson random variables is still Poisson:
\[
S_n=\sum_{i=1}^n X_i \sim \mathrm{Poisson}(n\lambda).
\]

If \(X_i\sim \mathrm{Poisson}(\lambda)\), then each variable has mean and variance equal to \(\lambda\). Therefore,
\[
\mathbb{E}[S_n]=n\lambda,
\qquad
\mathrm{Var}(S_n)=n\lambda.
\]

By the central limit theorem,
\[
\frac{S_n-n\lambda}{\sqrt{n\lambda}} \Rightarrow N(0,1).
\]

Equivalently, for the sample mean
\[
\overline X_n=\frac1n\sum_{i=1}^n X_i,
\]
we have
\[
\frac{\sqrt{n}\,(\overline X_n-\lambda)}{\sqrt{\lambda}} \Rightarrow N(0,1).
\]

This gives the theoretical basis for Gaussian approximation: when the mean parameter becomes large, the Poisson law gradually takes a bell-shaped form and is well approximated by the Gaussian law \(N(\lambda,\lambda)\).

In other words, Poisson\((\lambda)\) and \(N(\lambda,\lambda)\) have the same mean and the same variance, and the CLT explains why their shapes become closer when \(\lambda\) increases.

A useful refinement is given by Berry--Esseen type bounds. In general, Berry--Esseen tells us that the error of Gaussian approximation for standardized sums decreases at rate \(O(n^{-1/2})\).

In the Poisson setting, this suggests that after standardization the approximation error should improve at a rate of order \(\lambda^{-1/2}\). Therefore, the approximation is not expected to be very accurate for small \(\lambda\), but should improve steadily as \(\lambda\) grows.

To quantify the discrepancy between \(P(\lambda)\) and \(N(\lambda,\lambda)\), we use the 1-Wasserstein distance
\[
W_1(P,Q)=\int_{\mathbb R}|F_P(x)-F_Q(x)|\,dx,
\]
where \(F_P\) and \(F_Q\) are the cumulative distribution functions of the two laws.

This metric is particularly convenient here because it compares a discrete distribution and a continuous distribution directly through their CDFs, without forcing them into the same density representation.

Now let
\[
X_\lambda\sim \mathrm{Poisson}(\lambda),
\qquad
Z_\lambda\sim N(\lambda,\lambda).
\]
Define the standardized variables
\[
Y_\lambda=\frac{X_\lambda-\lambda}{\sqrt{\lambda}},
\qquad
G=\frac{Z_\lambda-\lambda}{\sqrt{\lambda}}\sim N(0,1).
\]

Then the CLT suggests that \(Y_\lambda\) converges in distribution to \(G\) as \(\lambda\to\infty\).

Moreover, Wasserstein distance scales linearly under affine transformations, so
\[
W_1(X_\lambda,Z_\lambda)=\sqrt{\lambda}\,W_1(Y_\lambda,G).
\]

This identity is important for interpretation. It shows that the **absolute** Wasserstein distance on the original count scale does not need to go to zero, because the natural fluctuation scale itself is \(\sqrt{\lambda}\).

What should become small is the discrepancy **relative** to that natural scale. For this reason, in addition to the raw distance, we also study the normalized quantity

\[
W_1^{(\mathrm{rel})}(\lambda)=
\frac{W_1(\mathrm{Poisson}(\lambda),N(\lambda,\lambda))}{\sqrt{\lambda}}.
\]

This normalized criterion is more meaningful for practical interpretation: it measures how large the approximation error is compared with the typical spread of the distribution itself.

In summary, the theory gives a coherent picture: the sum of Poisson variables remains Poisson, the CLT explains why Gaussian shape emerges for large \(\lambda\), Berry--Esseen predicts an error of order \(\lambda^{-1/2}\) after normalization, and Wasserstein distance provides a natural way to quantify this convergence.



## 3. Wasserstein distance 
We use the 1-Wasserstein distance

$$
W_1(P,Q)=\int_{\mathbb{R}} |F_P(x)-F_Q(x)|\,dx,
$$

where $F_P$ and $F_Q$ are the cumulative distribution functions of the two laws.



This metric is convenient here because it directly compares a discrete law and a continuous law through their CDFs.
。

## 4. Simulation
For each $\lambda\in\{1,2,\dots,100\}$, we compute the exact Poisson CDF and the matching Gaussian CDF on a dense grid, then approximate

$$
W_1\bigl(\mathrm{Poisson}(\lambda),N(\lambda,\lambda)\bigr)
$$

numerically.



Because the natural spread of both laws is of order $\sqrt{\lambda}$, we also consider the normalized quantity

$$
W_1^{(\mathrm{rel})}(\lambda)=\frac{W_1(\mathrm{Poisson}(\lambda),N(\lambda,\lambda))}{\sqrt{\lambda}}.
$$



## 5. Results
The absolute Wasserstein distance stays near 0.30 over the range $\lambda\in[1,100]$, so a fixed threshold such as $W_1<0.25$ is not informative in this experiment.



For example, the computed values are about 0.3134 at $\lambda=1$, 0.2991 at $\lambda=10$, 0.2983 at $\lambda=20$, 0.2980 at $\lambda=50$, and 0.2978 at $\lambda=100$.


By contrast, the normalized quantity decreases clearly with $\lambda$.


In our computation, $W_1/\sqrt{\lambda}<0.10$ first occurs at $\lambda=9$, and $W_1/\sqrt{\lambda}<0.05$ first occurs at $\lambda=36$.



## 6. Practical rule 
A clean W1-only rule is the following.



In words, the Gaussian approximation becomes visually and quantitatively reasonable around $\lambda \approx 9$, and more convincingly accurate around $\lambda \approx 36$.

## 7. ML application
Poisson models appear naturally in count modeling problems such as topic-model word counts, click counts, and rare-event logs.



When expected counts are large, replacing a Poisson law by a Gaussian surrogate can simplify approximate inference and downstream optimization.

When counts are small, however, the discrete and skewed nature of the Poisson law remains important, so Gaussian surrogates should be used with caution.



## 8. Reproducibility
The accompanying Python script computes the Wasserstein distance table, the normalized Wasserstein table, and the threshold summary.

