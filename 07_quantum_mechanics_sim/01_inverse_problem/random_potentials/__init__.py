import numpy as np
from numpy import random as rnd
from typing import NamedTuple, Dict, Any
from scipy.fft import ifft


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


class PotentialFactory(NamedTuple):
    x_min: float
    x_max: float
    well_depth: float
    well_raise: float
    well_decay: float
    num_spatial_bins: int = 1000
    num_momentum_bins: int = 100
    x_well: float = 0.0
    well_width: float = 1.0

    @property
    def x(self):
        return np.linspace(self.x_min, self.x_max, self.num_spatial_bins)

    @property
    def p(self):
        left_p = -self.num_momentum_bins // 2
        right_p = self.num_momentum_bins - left_p
        return np.arange(-left_p, right_p)

    @property
    def cosines(self):
        normalized_x = (self.x - self.x_well) / self.well_width
        return np.cos(2 * np.pi * normalized_x[:, None] * self.p[None, :])

    def get_random_fourier_coefficients(self):
        modulation = np.exp(-self.p * self.well_decay) * (self.p ** self.well_raise)
        return modulation  # rnd.normal(0, 1, self.num_momentum_bins)

    def get_random_potential(self):
        potential = np.zeros_like(self.x)
        mid_potential = self.cosines @ self.get_random_fourier_coefficients()
        mid_mask = (self.x > self.x_well) & (self.x <= self.x_well + self.well_width)
        potential[mid_mask] = mid_potential[mid_mask]
        return potential
