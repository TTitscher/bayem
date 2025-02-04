============================================================
   Derivation of variational Bayesian for nonlinear models
============================================================

The derivation is extracted from two papers

*   Chappell, M. A.; Groves, A. R.; Whitcher, B. \& Woolrich, M. W.
    Variational Bayesian Inference for a Nonlinear Forward Model,
    IEEE Transactions on Signal Processing, 2009, 57, 223-236
    https://ieeexplore.ieee.org/document/4625948
*   Chappell, M. A.; Groves, A. R. \& Woolrich, M. W.
    The FMRIB Variational Bayes Tutorial: Variational Bayesian inference for non-linear forward model,
    https://users.fmrib.ox.ac.uk/~chappell/papers/TR07MC1.pdf

Maximization of free energy
===========================
Free energy:

.. math::
    \require{cancel}
    F &= \int q(\boldsymbol{w})
    \log \,\frac{P(\boldsymbol{y}|\boldsymbol{w})\,P(\boldsymbol{w})}{q(\boldsymbol{w})} d\boldsymbol{w}.\\

Mean field approximation

.. math::
    q(\boldsymbol{w}) &= \prod_{i=1}^m q_{i}(\boldsymbol{w}_i).\\

In the special case of separating between model parameters :math:`\boldsymbol{\theta}` and noise parameters
:math:`\boldsymbol{\Phi}`, the posterior is approximated by the product of two distributions:

.. math::
    q(\boldsymbol{w}) &=q_\theta q_\Phi.\\

Variational inference tries to find the approximate posterior distributions :math:`q_i(w_i)` with :math:`i\epsilon
\left\{\theta, \Phi\right\}` that maximize the free energy :math:`F(q)`. Rewriting the free energy with the mean field
approximation results in:

.. math::
    F &= \int q_{i} \, q_{\cancel{i}} \,
    \log\left[P(\boldsymbol{y}|\boldsymbol{w})\, P(\boldsymbol{w})\right]
    - q_{i} \,q_{\cancel{i}} \, \log[q_{i}]
    - q_{i} \, q_{\cancel{i}} \, \log[q_{\cancel{i}}]
    \;d \boldsymbol{w}.\\

where :math:`q_\cancel{i}` represents the product of all distributions apart from :math:`q_i`.

The function :math:`F=\int f\left(\boldsymbol{w}, q(\boldsymbol{w})\right) \;d\boldsymbol{w}` with :math:`f` given as
the integrand of the the above equations is maximized with respect to a subset of the parameters :math:`\boldsymbol{w}_i`, thus the
function is written in terms of these parameters alone.

.. math::
    F &= \int g\left(\boldsymbol{w}_i, q_{i}(\boldsymbol{w}_i)\right) \;d\boldsymbol{w}_i.\\

with

.. math::
    g\left(\boldsymbol{w}_i, q_{i}(\boldsymbol{w}_i)\right) &=
    \int f\left(\boldsymbol{w}, q(\boldsymbol{w})\right) \;d\boldsymbol{w}_\cancel{i}.\\

From variational calculus, the maximum of F is the solution of the
`Euler-Lagrange equation <https://en.wikipedia.org/wiki/Calculus_of_variations#Euler%E2%80%93Lagrange_equation>`_.

.. math::
    \frac{\partial}{\partial q_i(\boldsymbol{w}_i)} \left[
    g\left(\boldsymbol{w}_i, q_{i}(\boldsymbol{w}_i), q'_{i}(\boldsymbol{w}_i)\right)
    \right]-
    \frac{d}{d\boldsymbol{w}_i}\left\{
    \frac{\partial}{\partial q'_i(\boldsymbol{w}_i)}\left[g(
    \boldsymbol{w}_i, q_{i}(\boldsymbol{w}_i), q'_{i}(\boldsymbol{w}_i))
    \right]
    \right\}&=0.\\


The second term vanishes, since :math:`g` does not depend on :math:`q'_i(\boldsymbol{w}_i)`. Substituting the first
term using the mean field approximation of F yields

.. math::
    0&= \frac{\partial }{\partial q_i} \left[ \int
    q_{i} \, q_{\cancel{i}} \,
    \log\left[P(\boldsymbol{y}|\boldsymbol{w})\, P(\boldsymbol{w})\right]
    - q_{i} \,q_{\cancel{i}} \, \log[q_{i}]
    - q_{i} \, q_{\cancel{i}} \, \log[q_{\cancel{i}}]
    \;d \boldsymbol{w}_{\!\cancel{i}}
    \right]\\
    &= \int  q_{\cancel{i}}\log[P(\boldsymbol{y}|\boldsymbol{w})\,P(\boldsymbol{w})] -
    (q_{\cancel{i}} \,
    \log[q_{i}] + \frac{q_{i} \, q_{\cancel{i}}}{q_{i}}) - q_{\cancel{i}} \,\log[q_{\cancel{i}}] \;
    d\boldsymbol{w}_{\!\cancel{i}}.\\

With the property of a density function to integrate to one, it follows:

.. math::
    0&= \int q_{\cancel{i}}\log[P(\boldsymbol{y}|\boldsymbol{w}) P(\boldsymbol{w})]d\boldsymbol{w}_{\cancel{i}}
    -  \log[q_{i}] - 1 - \int q_{\cancel{i}}\log[q_{\cancel{i}}]d\boldsymbol{w}_{\!\cancel{i}}.\\

Moving the second term to the other side of the equation and realizing that the latter two terms do not depend
on :math:`q_{i}`

.. math::
    \log[q_i] & = \int q_{\cancel{i}}\log[P(\boldsymbol{y}|\boldsymbol{w}) P(\boldsymbol{w})]
    d\boldsymbol{w}_{\!\cancel{i}} + \mathrm{const} \\
    \log[q_{i}] & \propto \int q_{\cancel{i}}\log[P(\boldsymbol{y}|\boldsymbol{w}) P(\boldsymbol{w})]
    d\boldsymbol{w}_{\!\cancel{i}}

which is identical to eq.(5) in Chappels paper.

Log Posterior
=============
The log-posterior :math:`L` in the above integrand is given using Bayes theorem and the assumption of parameter
and noise prior being uncorrelated by:

.. math::
    L = & \;\log[P(\boldsymbol{y}|\boldsymbol{\theta},\Phi] +\log[P(\boldsymbol{\theta})] +\log[P(\Phi)] +
    \color{red}{-[log(P(\boldsymbol{y}))]} \\[3mm]
    = & \;\log[P(\boldsymbol{y}|\boldsymbol{\theta},\Phi]+\log[\mathcal{N}(\boldsymbol{\theta};\boldsymbol{m_0},
    \Lambda_0^{-1})]+\log[\Gamma(\Phi;s_0,c_0)] + \color{red}{-[log(P(\boldsymbol{y}))]}\\[2mm]
    = &  \left(-\frac{N}{2}\log[2\pi]\right) + \frac{N}{2}\log[\Phi] - \frac{1}{2} \Phi
    \boldsymbol{k}^T\boldsymbol{k} \\
    & + (-\frac{1}{2}\log[(2\pi)^p \, \mathrm{det}(\Lambda_0^{-1})]) -\frac{1}{2} (\boldsymbol{\theta}-\boldsymbol{m}_0)^T
    \, \Lambda_0 \,(\boldsymbol{\theta}-\boldsymbol{m}_0) \\
    & + (\log[1/\Gamma(c_0)]-c_0\log[s_0]) + (c_0-1)\log[\Phi] -\frac{1}{s_0} \Phi \\[2mm]
    & + \color{red}{-[log(P(\boldsymbol{y}))]}.\\

.. math::
    \color{red}{\text{Since in the free energy equation the evidence is not included, this part is neglected in the further derivation.}}

Adding all terms not dependent on :math:`\boldsymbol{\theta}` and :math:`\boldsymbol{\Phi}`
[marked with ()] to a constant gives

.. math::
    L = \frac{N}{2}\log[\Phi] - \frac{1}{2} \Phi \boldsymbol{k}^T\boldsymbol{k} -\frac{1}{2}
    (\boldsymbol{\theta}-\boldsymbol{m}_0)^T \, \Lambda_0 \,(\boldsymbol{\theta}-\boldsymbol{m}_0)  + (c_0-1)
    \log[\Phi] -\frac{1}{s_0} \Phi + \mathrm{const} \lbrace \boldsymbol{\theta},\Phi \rbrace

similar to eq.(16) in Chappels paper, with

.. math::
    \color{red}{\mathrm{const} \lbrace \boldsymbol{\theta},\Phi \rbrace = -\frac{N}{2}\log[2\pi] -\frac{1}{2}\log[(2\pi)^p] -\frac{1}{2} \log[\mathrm{det}(\Lambda_0^{-1})] + \log[1/\Gamma(c_0)]-c_0\log[s_0]}

Update equations
================
Substituting :math:`L` into the update equations results in the update equations:

.. math::
    \log[q_{\theta}] & \propto &  \int q_{\Phi} L \, d\Phi  \\
    \log[\mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},\Lambda^{-1})] & \propto & \int L \, \Gamma(\Phi;s,c)
    \, d\Phi

.. math::
    \log[q_{\Phi}] & \propto &  \int q_{\theta} L \, d\boldsymbol{\theta}  \\
    \log[\mathrm{\Gamma}(\Phi;s,c)] & \propto & \int L \, \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},
    \Lambda^{-1})\,d\boldsymbol{\theta}

Update equations for parameters :math:`\boldsymbol{\theta}`
-----------------------------------------------------------
Left hand side of the equation:

.. math::
    \log[q_{\theta}]  = &\log[\mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},\Lambda^{-1})] \\
    = & -\frac{1}{2} (\boldsymbol{\theta}-\boldsymbol{m})^T \, \Lambda \,(\boldsymbol{\theta}-\boldsymbol{m}) +
    \mathrm{const}\lbrace \boldsymbol{\theta} \rbrace \\
    = &  -\frac{1}{2} [\boldsymbol{\theta}^T \Lambda \boldsymbol{\theta} - \boldsymbol{\theta}^T \Lambda
    \boldsymbol{m} - \boldsymbol{m}^T \Lambda \boldsymbol{\theta}+ \boldsymbol{m}^T \Lambda \boldsymbol{m} ]  +
    \mathrm{const}\lbrace \boldsymbol{\theta} \rbrace \\
    = & -\frac{1}{2} [\boldsymbol{\theta}^T \Lambda \boldsymbol{\theta} - \boldsymbol{\theta}^T \Lambda
    \boldsymbol{m} - \boldsymbol{m}^T \Lambda \boldsymbol{\theta}]  + \mathrm{const}\lbrace \boldsymbol{\theta}
    \rbrace\\

similar to eq.(B2) in Chappell.

.. math::
    \int q_{\Phi} L \, d\Phi  = & \int L \, \Gamma(\Phi;s,c) \, d\Phi \\
    = & -\frac{1}{2} \boldsymbol{k}^T\boldsymbol{k} \int \Phi \, \Gamma(\Phi;s,c) \, d\Phi -\frac{1}{2}
    (\boldsymbol{\theta}-\boldsymbol{m}_0)^T \, \Lambda_0 \,(\boldsymbol{\theta}-\boldsymbol{m}_0) \int \Gamma(\Phi;s,c) \,
    d\Phi \\
    &  +  \int \mathrm{const}\lbrace \boldsymbol{\theta} \rbrace(\Phi) \, \Gamma(\Phi;s,c) \, d\Phi \\
    = & -\frac{1}{2} \boldsymbol{k}^T\boldsymbol{k} \, sc -\frac{1}{2}  (\boldsymbol{\theta}-\boldsymbol{m}_0)^T \,
    \Lambda_0 \,(\boldsymbol{\theta}-\boldsymbol{m}_0)
    + \mathrm{const}\lbrace \boldsymbol{\theta} \rbrace,\\

where a Taylor expansion in :math:`\boldsymbol{k}` can be used:

.. math::
    \boldsymbol{k}(\boldsymbol{\theta}) \approx \boldsymbol{k}(\boldsymbol{m}) + \boldsymbol{J}_k \,
    (\boldsymbol{\theta}-\boldsymbol{m}) = \boldsymbol{k}_{m} + \boldsymbol{J}_k \,
    (\boldsymbol{\theta}-\boldsymbol{m}).

This results in:

.. math::
    = & -\frac{1}{2} (\boldsymbol{k}_{m} + \boldsymbol{J}_k \, (\boldsymbol{\theta}-\boldsymbol{m}))^T
    (\boldsymbol{k}_{m} + \boldsymbol{J}_k \, (\boldsymbol{\theta}-\boldsymbol{m})) \, sc
    -\frac{1}{2}(\boldsymbol{\theta}-\boldsymbol{m}_0)^T \, \Lambda_0 \,(\boldsymbol{\theta}-\boldsymbol{m}_0)\\
    &+\mathrm{const}\lbrace \boldsymbol{\theta} \rbrace \\
    = & -\frac{1}{2} [sc(\boldsymbol{k}_m^T \boldsymbol{J}_k (\boldsymbol{\theta}-\boldsymbol{m}) + (\boldsymbol{\theta}-\boldsymbol{m})^T \boldsymbol{J}_k^T \boldsymbol{k}_m
    +(\boldsymbol{\theta}-\boldsymbol{m})^T \boldsymbol{J}_k^T \boldsymbol{J}_k (\boldsymbol{\theta}-\boldsymbol{m})) \\
    & + \boldsymbol{\theta}^T \Lambda_0 \boldsymbol{\theta} - \boldsymbol{m}_0^T \Lambda_0 \boldsymbol{\theta} - \boldsymbol{\theta}^T \Lambda_0 \boldsymbol{m}_0]
    +\mathrm{const}\lbrace \boldsymbol{\theta} \rbrace \\
    = & -\frac{1}{2} [sc(\boldsymbol{k}_m^T \boldsymbol{J}_k \boldsymbol{\theta} + \boldsymbol{\theta}^T \boldsymbol{J}_k^T \boldsymbol{k}_m +
    \boldsymbol{\theta}^T \boldsymbol{J}_k^T \boldsymbol{J}_k \boldsymbol{\theta} - \boldsymbol{m}^T \boldsymbol{J}_k^T \boldsymbol{J}_k \boldsymbol{\theta}
    - \boldsymbol{\theta}^T \boldsymbol{J}_k^T \boldsymbol{J}_k \boldsymbol{m})\\
    & + \boldsymbol{\theta}^T \Lambda_0 \boldsymbol{\theta} - \boldsymbol{m}_0^T \Lambda_0 \boldsymbol{\theta} - \boldsymbol{\theta}^T \Lambda_0 \boldsymbol{m}_0]
    +\mathrm{const}\lbrace \boldsymbol{\theta} \rbrace \\
    = & -\frac{1}{2} [\boldsymbol{\theta}^T (\Lambda_0 + sc\,\boldsymbol{J}_k^T \boldsymbol{J}_k) \boldsymbol{\theta}
    - \boldsymbol{\theta}^T (\Lambda_0 \boldsymbol{m}_0 - sc \, \boldsymbol{J}_k^T\boldsymbol{k}_m + sc\,
    \boldsymbol{J}_k^T \boldsymbol{J}_k \boldsymbol{m}) \\
    &- (\boldsymbol{m}_0^T \Lambda_0 - sc\,\boldsymbol{k}(m)^T\boldsymbol{J}_k
    + sc\, \boldsymbol{m}^T\boldsymbol{J}_k^T\boldsymbol{J}_k) \boldsymbol{\theta}] + \mathrm{const}\lbrace \boldsymbol{\theta} \rbrace\\
    = & -\frac{1}{2} [\boldsymbol{\theta}^T (\Lambda_0 + sc\,\boldsymbol{J}_k^T \boldsymbol{J}_k) \boldsymbol{\theta}
    - \boldsymbol{\theta}^T (\Lambda_0 \boldsymbol{m}_0 + sc \, \boldsymbol{J}_k^T(-\boldsymbol{k}_m +\boldsymbol{J}_k \boldsymbol{m}))\\
    &- (\boldsymbol{m}_0^T \Lambda_0 + sc\,(-\boldsymbol{k}_m^T + \boldsymbol{m}^T\boldsymbol{J}_k^T)
    \boldsymbol{J}_k) \boldsymbol{\theta}]
    + \mathrm{const}\lbrace \boldsymbol{\theta} \rbrace.

Compare to the left hand side while omitting the terms constant in :math:`\boldsymbol{\theta}` gives:

.. math::
    -\frac{1}{2} [\boldsymbol{\theta}^T \Lambda \boldsymbol{\theta} - \boldsymbol{\theta}^T \Lambda \boldsymbol{m} - \boldsymbol{m}^T \Lambda \boldsymbol{\theta}]
    & \propto & -\frac{1}{2} [\boldsymbol{\theta}^T (\Lambda_0 + sc\,\boldsymbol{J}_k^T \boldsymbol{J}_k) \boldsymbol{\theta} \\
    & & - \boldsymbol{\theta}^T (\Lambda_0 \boldsymbol{m}_0 + sc \, \boldsymbol{J}_k^T(-\boldsymbol{k}_m + \boldsymbol{J}_k \boldsymbol{m})) \\
    & & - (\boldsymbol{m}_0^T \Lambda_0 + sc\,(-\boldsymbol{k}_m^T + \boldsymbol{m}^T\boldsymbol{J}_k^T)
    \boldsymbol{J}_k) \boldsymbol{\theta}].

resulting in the update equations

.. math::
    \Lambda & =& \Lambda_0 +  sc\,\boldsymbol{J}_k^T \boldsymbol{J}_k \\
    \Lambda \boldsymbol{m} &=& \Lambda_0 \boldsymbol{m}_0 + sc \, \boldsymbol{J}_k^T(-\boldsymbol{k}_m +
    \boldsymbol{J}_k \boldsymbol{m}).

similar to Chappell eq. 19/20 with :math:`\boldsymbol{J}=-\boldsymbol{J}_k` (no iteration required)

Update equations noise :math:`\Phi`
-----------------------------------
Left hand side

.. math::
    \log[q_{\Phi}] & = &\log[\Gamma(\Phi;s,c)] \\
    & = & (c-1)\log[\Phi] - \frac{\Phi}{s} + \mathrm{const} \lbrace \Phi \rbrace\\

see Chappell eq.(B9).

.. math::
    \int q_{\theta} L \, d\boldsymbol{\theta}  = & \int L \, \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},
    \Lambda^{-1})\, d\boldsymbol{\theta} \\
    = & -\frac{1}{2} \Phi \int  \boldsymbol{k}^T \boldsymbol{k} \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},
    \Lambda^{-1})\, d\boldsymbol{\theta} \\
    & + ( \frac{N}{2}\log[\Phi] + (c_0-1)\log[\Phi]-\frac{\Phi}{s_0} )\int \mathcal{N}(\boldsymbol{\theta};
    \boldsymbol{m},\Lambda^{-1})\, d\boldsymbol{\theta} \\
    & + \mathrm{const}\lbrace \boldsymbol{\Phi} \rbrace\\


use Taylor expansion and eq B12 Chappell, :math:`(\boldsymbol{\theta}-\boldsymbol{m})`-terms integrate to zero.

.. math::
    \int  \boldsymbol{k}^T \boldsymbol{k} \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},\Lambda^{-1})\,
    d\boldsymbol{\theta}
    = & \int (\boldsymbol{k}_m + \boldsymbol{J}_k \, (\boldsymbol{\theta}- \boldsymbol{m}))^T (\boldsymbol{k}_m +
    \boldsymbol{J}_k \, (\boldsymbol{\theta}- \boldsymbol{m})) \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},
    \Lambda^{-1})\, d\boldsymbol{\theta} \\
    = &\, \boldsymbol{k}_m^T \boldsymbol{k}_m \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},\Lambda^{-1})\,
    d\boldsymbol{\theta} \\
    & + \int \cancel{(\boldsymbol{k}_m^T\boldsymbol{J}_k(\boldsymbol{\theta}-\boldsymbol{m})} + \cancel{
    (\boldsymbol{J}_k(\boldsymbol{\theta}-\boldsymbol{m}))^T\boldsymbol{k}_m )}  \mathcal{N}(\boldsymbol{\theta};
    \boldsymbol{m},\Lambda^{-1})\, d\boldsymbol{\theta} \\
    & + \underbrace{\int (\boldsymbol{\theta}-\boldsymbol{m})^T \boldsymbol{J}_k^T\boldsymbol{J}_k
    (\boldsymbol{\theta}-\boldsymbol{m}) \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m},\Lambda^{-1})\,
    d\boldsymbol{\theta}}_{\mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^T \boldsymbol{J}_k)}.\\

Compare to the left hand side while omitting the terms constant in :math:`\Phi` and noting that the integration over the (normal)
density function is one results in:

.. math::
    (c-1)\log[\Phi] - \frac{\Phi}{s}  \propto & \frac{N}{2}\log[\Phi] + (c_0-1)
    \log[\Phi]-\frac{\Phi}{s_0} -\frac{1}{2}\Phi(\boldsymbol{k}_m^T \boldsymbol{k}_m +
    \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^T \boldsymbol{J}_k)) \\
    \propto &  (\frac{N}{2}+ c_0-1 )\log[\Phi] - \Phi (\frac{1}{s_0} + \frac{1}{2}(\boldsymbol{k}_m^T 
    \boldsymbol{k}_m + \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^T \boldsymbol{J}_k))).\\

.. math::
    c \cancel{-1} &=& \frac{N}{2} + c_0 \cancel{-1} \\
    \frac{1}{s} &=& \frac{1}{s_0} + \frac{1}{2}(\boldsymbol{k}_m^T \boldsymbol{k}_m + \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^T \boldsymbol{J}_k))

similar to Chappell eq. 21/22 with :math:`\boldsymbol{J}=-\boldsymbol{J}_k`

Summary of equations to solve
=============================

.. math::
    \Lambda & =& \Lambda_0 +  sc\,\boldsymbol{J}_k^T \boldsymbol{J}_k \\
    \Lambda \boldsymbol{m} &=& \Lambda_0 \boldsymbol{m}_0 + sc \, \boldsymbol{J}_k^T(-\boldsymbol{k}_m + \boldsymbol{J}_k \boldsymbol{m})\\
    c &=& \frac{N}{2} + c_0  \\
    \frac{1}{s} &=& \frac{1}{s_0} + \frac{1}{2}(\boldsymbol{k}_m^T \boldsymbol{k}_m + \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^T \boldsymbol{J}_k))

reduces to two equations for :math:`\boldsymbol{m}` and :math:`s` by inserting eq 1 and 3 into 2 and 4

.. math::
    (\Lambda_0 +  s (\frac{N}{2} + c_0 ) \,\boldsymbol{J}_k^T \boldsymbol{J}_k)\boldsymbol{m} &=& \Lambda_0 \boldsymbol{m}_0 + s (\frac{N}{2} + c_0 ) \, \boldsymbol{J}_k^T(-\boldsymbol{k}_m + \boldsymbol{J}_k \boldsymbol{m}) \Rightarrow \boldsymbol{m} = f_1(\boldsymbol{m},s)\\
    \frac{1}{s} &=& \frac{1}{s_0} + \frac{1}{2}(\boldsymbol{k}_m^T \boldsymbol{k}_m + \mathrm{tr}((\Lambda_0 +  s (\frac{N}{2} + c_0)\,\boldsymbol{J}_k^T \boldsymbol{J}_k)^{-1}\boldsymbol{J}_k^T \boldsymbol{J}_k))  \Rightarrow s = f_2(\boldsymbol{m},s)

e.g. using fixed point iteration until parameter converged.

Additional convergence check via :math:`F`
==========================================
"Convergence [...] guarantee no longer holds [...]. A typical consequence is that VB algorithm cycles through a limited set of solutions without settling on asingle set of values." Chappell sec B

Monitoring free-energy for that case (**notation to be improved**)

.. math::
    F =& \int q_{\theta} \, q_{\Phi}\log \,\frac{P(\boldsymbol{y}|\boldsymbol{w})\,P(\boldsymbol{w})}{q_{\theta} \, q_{\Phi}} dw  \\
    =& \int q_{\theta} \, q_{\Phi} \,\log[P(\boldsymbol{y}|\boldsymbol{\theta},\Phi)\,P(\boldsymbol{\theta},\Phi)] - q_{\theta} \, q_{\Phi} \,\log[q_{\theta}] - q_{\theta} \, q_{\Phi} \,\log[q_{\Phi}] d\boldsymbol{\theta}d\Phi \\
    = & \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \, \Gamma(\Phi;s,c) L d\Phi d\boldsymbol{\theta} -\int \mathcal{N}(\boldsymbol{\theta}) \Gamma(\Phi;s,c)\log[\mathcal{N}(\boldsymbol{\theta})] d\Phi d\boldsymbol{\theta}\\
    & - \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \, \Gamma(\Phi;s,c)\log[\Gamma(\Phi;s,c)] d\Phi d\boldsymbol{\theta}

term 1:

.. math::
    1 = &  \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1})\, \Gamma(\Phi;s,c) L \;d\Phi
    \;d\boldsymbol{\theta}   \\
    & \color{blue}{\text{with substituting the definition of the log posterior $L$ WITHOUT evidence part}}\\
    = & (\frac{N}{2}+(c_0-1)) \int\log[\Phi] \, \Gamma(\Phi;s,c)\, d\Phi \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \,   d\boldsymbol{\theta}\\
    & - \frac{1}{2} \int \Phi \boldsymbol{k}^T\boldsymbol{k} \, \Gamma(\Phi;s,c)\,\mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \, d\Phi \,   d\boldsymbol{\theta}  \\
    & -\frac{1}{2} \int (\boldsymbol{\theta}-\boldsymbol{m}_0)^T \Lambda_0 (\boldsymbol{\theta}-\boldsymbol{m}_0)
    \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \,   d\boldsymbol{\theta} \, \int \Gamma(\Phi;s,c)
    \, d\Phi   \\
    & -\frac{1}{s_0} \int \Phi \, \Gamma(\Phi;s,c) \, d\Phi \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \, d\boldsymbol{\theta}  \\
    & + \color{red}{[-\frac{N}{2}\log[2\pi] -\frac{1}{2}\log[(2\pi)^p] -\frac{1}{2} \log[\mathrm{det}(\Lambda_0^{-1})] + \log[1/\Gamma(c_0)]-c_0\log[s_0]]} \int \Gamma(\Phi;s,c) \, \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \, d\boldsymbol{\theta}\, d\Phi \\
    = &  (\frac{N}{2}+c_0-1)(\log[s]+\psi(c)) \text{    [see derivation in appendix ??]}\\
    & - \frac{1}{2} \int \Phi \, \Gamma(\Phi;s,c)\,d\Phi \int \boldsymbol{k}^T\boldsymbol{k}\,\mathcal{N} d\boldsymbol{\theta} \text{    [see above]}\\
    & -\frac{1}{2} ((\boldsymbol{m}-\boldsymbol{m}_0)^T\Lambda_0(\boldsymbol{m}-\boldsymbol{m}_0)+\mathrm{tr}(\Lambda^{-1}\Lambda_0)) \text{    [see derivation 1 in appendix]}\\
    & - \frac{sc}{s_0}\\
    & \color{red}{-\frac{N}{2}\log[2\pi] -\frac{1}{2}\log[(2\pi)^p] -\frac{1}{2} \log[\mathrm{det}(\Lambda_0^{-1})] + \log[1/\Gamma(c_0)]-c_0\log[s_0]}\\
    = &  (\frac{N}{2}+c_0-1)(log[s]+\psi(c)) - \frac{1}{2} sc (\boldsymbol{k}_m^T\boldsymbol{k}_m + \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^{T}\boldsymbol{J}_k)) -\frac{1}{2} ((\boldsymbol{m}-\boldsymbol{m}_0)^T\Lambda_0(\boldsymbol{m}-\boldsymbol{m}_0)\\
    & +\mathrm{tr}(\Lambda^{-1}\Lambda_0))  - \frac{sc}{s_0} \\
    & \color{red}{-\frac{N}{2}\log[2\pi] -\frac{1}{2}\log[(2\pi)^p] -\frac{1}{2} \log[\mathrm{det}(\Lambda_0^{-1})] + \log[1/\Gamma(c_0)]-c_0\log[s_0]}

term 2:

.. math::
    2 = & -\int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1})\Gamma(\Phi;s,c)\log[\mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1})(\boldsymbol{\theta})] d\Phi d\boldsymbol{\theta}\\
    = & - \int \Gamma(\Phi;s,c) \, d\Phi \, \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \,\log[\mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1})] d\boldsymbol{\theta} \\
    & \color{blue}{\text{with }\log[\mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1})] =} \color{red}{-\frac{1}{2}log((2\pi)^p)} \color{blue}{- \frac{1}{2}\log[det \Lambda^{-1}] - \frac{1}{2}(\boldsymbol{\theta} -
    \boldsymbol{m})^T \Lambda (\boldsymbol{\theta} - \boldsymbol{m})}\\
    = & - \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \, ({\color{red}{-\frac{1}{2}log((2\pi)^p)}} - \frac{1}{2}\log[det \Lambda^{-1}] - \frac{1}{2}(\boldsymbol{\theta} -
    \boldsymbol{m})^T \Lambda (\boldsymbol{\theta} - \boldsymbol{m}))  d\boldsymbol{\theta} \\
    = & {\color{red}{\frac{1}{2}log((2\pi)^p)}} + \frac{1}{2}\log[det \Lambda^{-1}] + \frac{1}{2}\mathrm{tr}(\Lambda^{-1}\Lambda) \\
    = & {\color{red}{\frac{1}{2}log((2\pi)^p)}} + \frac{1}{2}\log[det \Lambda^{-1}] +  \frac{1}{2} n_{param}\\
    = & - \frac{1}{2}\log[det \Lambda] + \color{red}{\frac{1}{2} n_{param} + \frac{1}{2}log((2\pi)^p)}

term 3:

.. math::
    3 = &  - \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1})(\boldsymbol{\theta}) \Gamma(\Phi;s,c)\,\log[\Gamma(\Phi;s,c)] d\Phi d\boldsymbol{\theta}\\
    = & - \int \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \, d\boldsymbol{\theta} \, \int \Gamma(\Phi;s,c) \,\log[\Gamma(\Phi;s,c)] d\Phi \\
    & \color{blue}{\text{with }\log[\Gamma(\Phi;s,c)] = \log[1/\Gamma_c] - c\log[s] + (c-1)\log[\Phi] - \frac{\Phi}{s} }\\
    = & - \int \Gamma(\Phi;s,c) \, (\log[1/\Gamma_c] - c\log[s] + (c-1)\log[\Phi] - \frac{\Phi}{s})  d\Phi \\
    = &  - \int \Gamma(\Phi;s,c) \, (\log[1/\Gamma_c] - c\log[s]) d\Phi - \int \Gamma(\Phi;s,c) \,((c-1)\log[\Phi] - \frac{\Phi}{s})
    d\Phi \\
    = & - (\log[1/\Gamma_c] - c\log[s]) + \frac{1}{s}\int \Phi \, \Gamma \, d\Phi - (c-1) \int \log[\Phi] \, \Gamma
    \, d\Phi \\
    = & - (\log[1/\Gamma_c] - c\log[s]) + \frac{\cancel{s}c}{\cancel{s}} - (c-1)(\log[s]+\psi(c)) \\
    = & +\log[\Gamma_c] + c\log[s]) + \frac{\cancel{s}c}{\cancel{s}} - (c-1)(\log[s]+\psi(c))

.. math::
    F =& (\frac{N}{2}+c_0-1)(\log[s]+\psi(c)) - \frac{1}{2} \color{green}{sc} (\boldsymbol{k}_m^T\boldsymbol{k}_m +
    \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^{T}\boldsymbol{J}_k)) \\
    & -\frac{1}{2} ((\boldsymbol{m}-\boldsymbol{m}_0)^T\Lambda_0(\boldsymbol{m}-\boldsymbol{m}_0) +\mathrm{tr}(\Lambda^{-1}\Lambda_0))  - \frac{sc}{s_0} \\
    & \color{green}{- \frac{1}{2}\log[det \Lambda]} \\
    &  \color{green}{ +\log[\Gamma_c] + c\log[s] + \frac{\cancel{s}c}{\cancel{s}} - (c-1)(\log[s]+\psi(c)) }\\
    & \color{red}{-\frac{N}{2}\log[2\pi] \cancel{-\frac{1}{2}\log[(2\pi)^p]} +\frac{1}{2} \log[\mathrm{det}(\Lambda_0)] + \log[1/\Gamma(c_0)]-c_0\log[s_0] + \frac{1}{2} n_{param} + \cancel{\frac{1}{2}log((2\pi)^p)}}

not the same as in Chappell eq 23.


Free energy equation check
----------------------------

Proof free energy equation by comparing derivation to :math:`F` with respect of :math:`s, c, \boldsymbol{m}, \Lambda` with update equations:

**derivation with respect to** :math:`s`:

.. math::
    0 = & \frac{\partial F}{\partial s} \\
    0 = & (\frac{N}{2}-c_0-1)\frac{1}{s} - \frac{1}{2}c(\boldsymbol{k}_m^T\boldsymbol{k}_m +
    \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^{T}\boldsymbol{J}_k)) - \frac{c}{s_0} + \frac{c}{s} - (c-1)\frac{1}{s}\\
    (\frac{N}{2}-c_0-1)\frac{1}{s} + \frac{c}{s} - (c-1)\frac{1}{s} = & \frac{c}{s_0} + \frac{1}{2}c(\boldsymbol{k}_m^T\boldsymbol{k}_m +
    \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^{T}\boldsymbol{J}_k))\\
    (\frac{N}{2}-c_0-1+c-c+1)\frac{1}{s} = & c\left( \frac{1}{s_0} + \frac{1}{2}(\boldsymbol{k}_m^T\boldsymbol{k}_m +
    \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^{T}\boldsymbol{J}_k))\right)\\
    (\frac{N}{2}-c_0)\frac{1}{s} = & c\left( \frac{1}{s_0} + \frac{1}{2}(\boldsymbol{k}_m^T\boldsymbol{k}_m +
    \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^{T}\boldsymbol{J}_k))\right)

which is identical to the two update equations:

.. math::
    c &=& \frac{N}{2} + c_0  \\
    \frac{1}{s} &=& \frac{1}{s_0} + \frac{1}{2}(\boldsymbol{k}_m^T \boldsymbol{k}_m + \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^T \boldsymbol{J}_k))

**derivation with respect to** :math:`\Lambda`

.. math::
    0 = & \frac{\partial F}{\partial \Lambda} \\
    0 = & -\frac{1}{2}sc\frac{\partial \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^{T}\boldsymbol{J}_k))}{\partial \Lambda} - \frac{1}{2}\frac{\partial\mathrm{tr}(\Lambda^{-1}\Lambda_0)}{\partial \Lambda} - \frac{\partial\log[\det\Lambda]}{\partial \Lambda}\\
    0 = & -sc (-\Lambda^{-T}(\boldsymbol{J}_k^{T}\boldsymbol{J}_k)^T\Lambda^{-T}) + \Lambda^{-T}\Lambda_0^T \Lambda^{-T} - \frac{1}{\det\Lambda}det\Lambda \Lambda^{-T}\\
    0 = & sc \, \Lambda^{-T}(\boldsymbol{J}_k^{T}\boldsymbol{J}_k)^T\Lambda^{-T}{\color{blue}\Lambda^T} + \Lambda^{-T}\Lambda_0^T \Lambda^{-T}{\color{blue}\Lambda^T} - \Lambda^{-T}{\color{blue}\Lambda^T} \\
    \boldsymbol{1} = & \Lambda^{-T}(sc (\boldsymbol{J}_k^{T}\boldsymbol{J}_k)^T + \Lambda_0^T)

using (https://www.ics.uci.edu/~welling/teaching/KernelsICS273B/MatrixCookBook.pdf):

.. math::
    \frac{\partial}{\partial \boldsymbol{X}}\mathrm{tr}(\boldsymbol{A}\boldsymbol{X}^{-1}\boldsymbol{B}) =& -\boldsymbol{X}^{-T} \boldsymbol{A}^{T} \boldsymbol{B}^{T} \boldsymbol{X}^{-T}  \\
    \frac{\partial}{\partial \boldsymbol{X}}\det\boldsymbol{X} = & det\boldsymbol{X} (\boldsymbol{X}^{-T})

which leads to update equation 1:

.. math::
    \Lambda^T =& sc (\boldsymbol{J}_k^{T}\boldsymbol{J}_k)^T + \Lambda_0^T \\
    \Lambda =& sc (\boldsymbol{J}_k^{T}\boldsymbol{J}_k) + \Lambda_0


**derivation with respect to** :math:`\boldsymbol{m}`

.. math::
    0 = & \frac{\partial F}{\partial \boldsymbol{m}} \\
    0 = & -\frac{1}{2} \frac{\partial (\boldsymbol{m}-\boldsymbol{m}_0)^T \Lambda_0 (\boldsymbol{m}-\boldsymbol{m}_0)}{\partial \boldsymbol{m}} - \frac{1}{2} sc \left[ \frac{\boldsymbol{k}_m^T \boldsymbol{k}}{\partial \boldsymbol{m}} + \frac{\partial \mathrm{tr}(\Lambda^{-1}\boldsymbol{J}_k^T\boldsymbol{J}_k)}{\partial \boldsymbol{m}} \right]\\
    0 = & -\frac{1}{2} (\Lambda_0+\Lambda_0^T) (\boldsymbol{m}-\boldsymbol{m}_0) -\frac{1}{2} sc \left[(-\boldsymbol{J}_k^T \boldsymbol{k}_m - \boldsymbol{k}_m^T \boldsymbol{J}_k) + 0\right] \\
    0 = & -\Lambda_0 \boldsymbol{m} + \Lambda_0 \boldsymbol{m}_0 + sc \boldsymbol{J}_k^T \boldsymbol{k}_m \\
    \Lambda_0 \boldsymbol{m} = & \Lambda_0 \boldsymbol{m}_0 + sc \boldsymbol{J}_k^T \boldsymbol{k}_m

with:

.. math::
    \frac{\partial \boldsymbol{k}_m}{\partial \boldsymbol{m}} = & \frac{\partial \boldsymbol{J}_k (\boldsymbol{\theta}-\boldsymbol{m})}{\partial \boldsymbol{m}} = -\boldsymbol{J}_k\\
    \frac{\partial \boldsymbol{J}_k}{\partial \boldsymbol{m}} = & 0 \\
    \frac{\partial}{\partial \boldsymbol{X}} ( \boldsymbol{X}\boldsymbol{b}+\boldsymbol{c})^T \boldsymbol{D} ( \boldsymbol{X}\boldsymbol{b}+\boldsymbol{c}) =  & (\boldsymbol{D}+\boldsymbol{D}^T) (\boldsymbol{X}\boldsymbol{b}+\boldsymbol{c})\boldsymbol{b}^T

inserting :math:`\Lambda_0 = \Lambda -sc \boldsymbol{J}_k^T\boldsymbol{J}_k` on the left side leads to the second update equation!

Appendix
=========
Derivation 1
------------

.. math::
    \left(\boldsymbol{\theta}-\boldsymbol{m}_0\right)^T\boldsymbol{\Lambda}_0
    \left(\boldsymbol{\theta}-\boldsymbol{m}_0\right)
    &=
    \left(\boldsymbol{\theta}-\boldsymbol{m}+(\boldsymbol{m}-\boldsymbol{m}_0)\right)^T\boldsymbol{\Lambda}_0
    \left(\boldsymbol{\theta}-\boldsymbol{m}+(\boldsymbol{m}-\boldsymbol{m}_0)\right)\\
    &=
    \left(\boldsymbol{\theta}-\boldsymbol{m}\right)^T\boldsymbol{\Lambda}_0
    \left(\boldsymbol{\theta}-\boldsymbol{m}\right)
    +
    \left(\boldsymbol{m}-\boldsymbol{m}_0\right)^T\boldsymbol{\Lambda}_0
    \left(\boldsymbol{m}-\boldsymbol{m}_0\right)\\
    &+
    \left(\boldsymbol{m}-\boldsymbol{m}_0\right)^T\boldsymbol{\Lambda}_0\left(\boldsymbol{\theta}-\boldsymbol{m}\right)
    + \left(\boldsymbol{\theta}-\boldsymbol{m}\right)^T\boldsymbol{\Lambda}_0
    \left(\boldsymbol{m}-\boldsymbol{m}_0\right)\\

As a consequence, the following equation holds:

.. math::
    \int (\boldsymbol{\theta}-\boldsymbol{m}_0)^T \Lambda_0 (\boldsymbol{\theta}-\boldsymbol{m}_0)
    \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1}) \,   d\boldsymbol{\theta}
    =
    (\boldsymbol{m}-\boldsymbol{m}_0)^T\Lambda_0(\boldsymbol{m}-\boldsymbol{m}_0)+\mathrm{tr}(\Lambda^{-1}\Lambda_0).

Note that the terms  :math:`\left(\boldsymbol{\theta}-\boldsymbol{m}\right) \mathcal{N}(\boldsymbol{\theta};
\boldsymbol{m}, \Lambda^{-1})` vanish due to the definition of the mean, and equation B12 in Chappel is used to
resolve the remaining integral.

Derivation 2 of B12
---------------------

.. math::
    \int (\boldsymbol{\theta}-\boldsymbol{m})^T\boldsymbol{U}(\boldsymbol{\theta}-\boldsymbol{m}) \, \mathcal{N}(\boldsymbol{\theta};\boldsymbol{m}, \Lambda^{-1})\,d\boldsymbol{\theta} =??? \mathrm{tr}(\Lambda^{-1}\boldsymbol{U}) \\


Derivation 3
------------

.. math::
    \int \log[\Phi] \, \Gamma(\Phi;s,c)\,d\Phi =??? log[s] + \psi(c) \\
