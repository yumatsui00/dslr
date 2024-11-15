import pandas as pd

def _len(values):
    count = 0
    for _ in values:
        count += 1
    return count

def _sum(values):
    total = 0
    for value in values:
        total += value
    return total

def _mean(values):
    return (_sum(values) / _len(values)) if _len(values) > 0 else float('nan')

def _std(values):
    l = _len(values)
    if l < 0:
        return None
    vairance = _sum((x - _mean(values)) ** 2 for x in values) / l
    return vairance ** 0.5


def _sort(values, order="as", type="list", sort_index=-1):
    if not (order == "as" or order == "des"):
        raise AssertionError("Invalid Order ooption. Order has to be as or des")
    if type == "list":
        items = values
    elif type == "series" or type == "dict":
        items = list(values.items())
        if sort_index == -1:
            sort_index = 1
    else:
        raise AssertionError("Invalid type option. Type can be list, series, or dict")
    n = _len(items)

    if sort_index < 0:
        if order == "as":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if items[j] > items[j + 1]:
                        items[j], items[j + 1] = items[j + 1], items[j]
        elif order == "des":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if items[j] < items[j + 1]:
                        items[j], items[j + 1] = items[j + 1], items[j]
    else:
        if order == "as":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if items[j][sort_index] > items[j + 1][sort_index]:
                        items[j], items[j + 1] = items[j + 1], items[j]
        elif order == "des":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if items[j][sort_index] < items[j + 1][sort_index]:
                        items[j], items[j + 1] = items[j + 1], items[j]

    if type == "series":
        return pd.Series({k: v for k, v in items})
    elif type == "dict":
        return dict(items)
    return items

def _corr(x, y):
    if _len(x) != _len(y):
        raise ValueError("The length of x and y have to be same")
    x_mean = _mean(x)
    y_mean = _mean(y)
    up = _sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(_len(x)))
    bl = _sum((x[i] - x_mean) ** 2 for i in range(_len(x))) ** 0.5
    br = _sum((y[i] - y_mean) ** 2 for i in range(_len(y))) ** 0.5
    return up / (bl * br)
