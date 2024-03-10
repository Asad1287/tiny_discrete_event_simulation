import heapq
from datetime import datetime, timedelta
from scipy import stats
import numpy as np


class Distribution:
    def __init__(self, dist_type: str, **kwargs):
        self.dist_type = dist_type
        self.dist_params = kwargs
        self.distribution = self.create_distribution()

    def create_distribution(self):
        if self.dist_type == "Exponential":
            return stats.expon(scale=self.dist_params["mean"])
        elif self.dist_type == "Normal":
            return stats.norm(loc=self.dist_params["mean"], scale=self.dist_params["std_dev"])
        else:
            raise ValueError(f"Unsupported distribution type: {self.dist_type}")

    def generate(self, n=1):
        return self.distribution.rvs(size=n)