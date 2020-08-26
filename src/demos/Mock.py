import random
import numpy as np


def get_workload_trend(num_days):
    x = list(np.arange(0, num_days, .5))
    y = [random.randint(100, 150) for i in x]
    return (x, y)


def get_workload_pred(num_days):
    x = list(np.arange(0, num_days, .5))
    y = [random.randint(100, 150) for i in x]
    return x, y


def get_appointments(num_days):
    x = list(np.arange(0, num_days, .5))
    y = [random.randint(100, 130) for i in x]
    return (x, y)
