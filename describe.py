from utils import parser
import sys
import pandas as pd
import utils.math as ft

def describe_data(series):
    count = 0
    total = 0
    minimum = float('inf')
    maximum = float('-inf')
    values = []
    for value in series:
        if pd.notna(value):
            count += 1
            total += value
            values.append(value)
            if value < minimum:
                minimum = value
            if value > maximum:
                maximum = value
    mean = total / count if count > 0 else float('nan')
    sig = 0
    for value in values:
        sig += (value - mean) ** 2
    std = (sig / (count - 1)) ** (1 / 2) if count > 1 else float('nan')
    sorted_values = ft._sort(values)
    q1 = sorted_values[int(0.25 * (count - 1))] if count > 0 else float('nan')
    q2 = sorted_values[int(0.50 * (count - 1))] if count > 0 else float('nan')
    q3 = sorted_values[int(0.75 * (count - 1))] if count > 0 else float('nan')
    return {
        'Count': count,
        'Mean': mean,
        'Std': std,
        'Min': minimum,
        '25%': q1,
        '50%': q2,
        '75%': q3,
        'Max': maximum
    }


def _describe(data):
    num_data = data.select_dtypes(include="number")
    stats = {col: describe_data(num_data[col]) for col in num_data.columns}
    pd.set_option('display.max_rows', None)                  #行の省略をなくす
    pd.set_option('display.max_columns', None)               #列の省略をなくす
    pd.set_option('display.expand_frame_repr', None)         #横長の出力の省略をなくす
    print(pd.DataFrame(stats))


if __name__ == "__main__":
    parser.check_arg_num(2)
    parser.check_path(sys.argv[1])
    data = pd.read_csv(sys.argv[1])
    _describe(data)

