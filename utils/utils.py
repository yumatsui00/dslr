import sys
import os
import pandas as pd

def _len(values):
    if not values:
        return 0
    count = 0
    for value in values:
        count += 1
    return count

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


def ft_corr(x, y):
	if len(x) != len(y):
		Error_exit("Error occured when calculating corr")
	x_mean = ft_sum(x) / len(x)
	y_mean = ft_sum(y) / len(y)
	up = ft_sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
	bl = ft_sum((x[i] - x_mean) ** 2 for i in range(len(x))) ** 0.5
	br = ft_sum((y[i] - y_mean) ** 2 for i in range(len(x))) ** 0.5
	return up / (bl * br)


#def _select_dtype(df, include=None, exclude=None):
#    """指定されたデータ型を持つ列のみを抽出
#    df: 対象のデータフレーム
#    include: 抽出したいデータ型
#    exclude: 除外したいデータ型"""

#    if include is not None and not isinstance(include, list):
#        include = [include]
#    if exclude is not None and not isinstance(exclude, list):
#        exclude = [exclude]
#    ret = []
#    for col in df.columns:
#        col_type = df[col].dtype.name
#        print(col_type)
#        if include and col_type in include:
#            ret.append(col)
#        elif exclude and col_type in exclude:
#            ret.append(col)
#        elif include is None and exclude is None:
#            ret.append(col)
#    return ret

