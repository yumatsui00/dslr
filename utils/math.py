import sys
import os
import pandas as pd

def _sum(values):
    total = 0
    for value in values:
        total += value
    return total

def _mean(values):
    total_sum = _sum(values)
    mean_value = total_sum / len(values)
    return mean_value

def _std(values):
    if len(values) == 0:
            return None
    mean = _mean(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance ** 0.5

def ft_sort(values):
    n = len(values)
    for i in range(n):
        for j in range(0, n-i-1):
            if values[j] > values[j + 1]:
                # 隣り合う要素を入れ替え
                values[j], values[j + 1] = values[j + 1], values[j]
    return values

def ft_sort_values(series):
	items = list(series.items())
	n = len(items)
	for i in range(n):
		for j in range(0, n - i - 1):
			if items[j][1] > items[j + 1][1]:
				items[j], items[j + 1] = items[j + 1], items[j]
	sorted_series = pd.Series({k: v for k, v in items})
	return sorted_series

def ft_sort_corrs(corrs):
    items = list(corrs.items())
    n = len(items)

    for i in range(n):
        for j in range(0, n - i - 1):
            # 降順に並べ替え（大きいものが先）
            if items[j][1] < items[j + 1][1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items


def ft_corr(x, y):
	if len(x) != len(y):
		Error_exit("Error occured when calculating corr")
	x_mean = ft_sum(x) / len(x)
	y_mean = ft_sum(y) / len(y)
	up = ft_sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
	bl = ft_sum((x[i] - x_mean) ** 2 for i in range(len(x))) ** 0.5
	br = ft_sum((y[i] - y_mean) ** 2 for i in range(len(x))) ** 0.5
	return up / (bl * br)
