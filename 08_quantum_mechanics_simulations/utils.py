import numpy as np
from numpy import random as rnd
from matplotlib import pyplot as plt
from scipy.fft import fft, ifft
from scipy.integrate import ode
from scipy.optimize import bisect
from tqdm import autonotebook as tqdm


def random_potential(df, num_bins, rise, decay, min_val):
    x = np.linspace(0, 1, num_bins)
    before_x = np.linspace(-1, x[0] - (x[1] - x[0]), num_bins)
    after_x = np.linspace(x[-1] + x[1] - x[0], 2, num_bins)

    mu = rnd.standard_t(df)
    sigma = rnd.chisquare(df)
    y = (
        rnd.normal(mu, sigma, size=num_bins)
        * np.exp(-x * decay * num_bins)
        * (x ** rise)
    )

    yb = np.real(ifft(y))
    yb = yb - yb[0]
    if np.abs(yb.min()) < np.abs(yb.max()):
        yb = -yb
    yb = min_val * yb / np.abs(yb.min())

    return (
        np.r_[before_x, x, after_x],
        np.r_[np.zeros_like(before_x), yb, np.zeros_like(after_x)],
    )


def numerov(x, v, energy):
    g = energy - v
    dx = x[1] - x[0]
    psi = np.zeros_like(x)
    psi[1] = 1e-2
    for k in range(1, x.shape[0] - 1):
        k_plus = 1 + 1.0 / 12.0 * dx * dx * g[k + 1]
        k_zero = 1 - 5.0 / 12.0 * dx * dx * g[k]
        k_minus = 1 + 1.0 / 12.0 * dx * dx * g[k - 1]
        psi[k + 1] = (2 * psi[k] * k_zero - psi[k - 1] * k_minus) / k_plus
    return psi


def refine_energy(x, v, e0, e1):
    def last_wave_function_point(energy):
        psi = numerov(x, v, energy)
        return psi[-1]

    return bisect(last_wave_function_point, e0, e1)


def find_energies(x, v, grid_size=100):
    last_energy = v.min()
    last_psi = numerov(x, v, last_energy)
    for energy in np.linspace(v.min() + 1e-15, 0, grid_size):
        psi = numerov(x, v, energy)
        if psi[-1] * last_psi[-1] < 0:
            final_energy = refine_energy(x, v, last_energy, energy)
            yield final_energy, numerov(x, v, final_energy)
        last_energy = energy
        last_psi = psi
