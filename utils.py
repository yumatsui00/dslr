import sys
import os
import pandas as pd

def ft_sum(values):
    total = 0
    for value in values:
        total += value
    return total

def ft_mean(values):
    if not values:
        return None
    total_sum = ft_sum(values)
    mean_value = total_sum / len(values)
    return mean_value

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

def Error_exit(message):
    print(f"ERROR: {message}")
    print("Usage: python describe.py <data_path>")
    sys.exit(1)

def Check_args():
    # 引数の確認
	if len(sys.argv) < 2:
		Error_exit("Too Few Args")
	elif len(sys.argv) > 2:
		Error_exit("Too Many Args")

def Check_path(path):
	if not os.path.exists(path):
		Error_exit(f"{path} doesn't exist")
	elif not os.access(path, os.R_OK):
		Error_exit("Permission denied")

def ft_corr(x, y):
	if len(x) != len(y):
		Error_exit("Error occured when calculating corr")
	x_mean = ft_sum(x) / len(x)
	y_mean = ft_sum(y) / len(y)
	up = ft_sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
	bl = ft_sum((x[i] - x_mean) ** 2 for i in range(len(x))) ** 0.5
	br = ft_sum((y[i] - y_mean) ** 2 for i in range(len(x))) ** 0.5
	return up / (bl * br)