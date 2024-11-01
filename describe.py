import pandas as pd
import sys
import utils as ut



def calc_stats(series):
    count = 0
    total = 0
    min = float('inf')
    max = float('-inf')
    values = []
    for value in series:
        if pd.notna(value):
            count += 1
            total += value
            values.append(value)
            if value < min:
                min = value
            if value > max:
                max = value
    #mean
    mean = total / count if count > 0 else float('nan')
    #std
    sig = 0
    for value in values:
        sig += (value - mean) ** 2
    std = (sig / (count - 1)) ** (1 / 2) if count > 1 else float('nan')

    sorted_values = ut.ft_sort(values)
    q1 = values[int(0.25 * (count - 1))] if count > 0 else float('nan')
    q2 = values[int(0.50 * (count - 1))] if count > 0 else float('nan')
    q3 = values[int(0.75 * (count - 1))] if count > 0 else float('nan')
    return {
        'Count': count,
        'Mean': mean,
        'Std': std,
        'Min': min,
        '25%': q1,
        '50%': q2,
        '75%': q3,
        'Max': max
	}


ut.Check_args
# データパスを取得
path = sys.argv[1]

ut.Check_path(path)

data = pd.read_csv(path)
num_data = data.select_dtypes(include="number") #これ使っていいの？？計算はしてないけど数値だけ抜き出し

stats = {column: calc_stats(num_data[column]) for column in num_data.columns}

# 省略を避ける設定
pd.set_option('display.max_rows', None)     # 行の省略をなくす
pd.set_option('display.max_columns', None)  # 列の省略をなくす
pd.set_option('display.expand_frame_repr', False)  # 横長の出力を省略せずに表示

print(pd.DataFrame(stats))
