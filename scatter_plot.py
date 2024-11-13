import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.stats import ks_2samp
from utils import math as ft
from utils import parser
from utils import utils as ut
from itertools import combinations


def scatterplot(data):
    if not "Hogwarts House" in data.columns:
        ut.Error_exit("There is no Hogwarts House Section")

    subjects = data.select_dtypes(include="number").columns.drop("Index")

    #相関係数の計算
    corrs = {}

    for subject_x, subject_y in combinations(subjects, 2):
        subject_data = data[[subject_x, subject_y]].dropna()
        x = subject_data[subject_x].tolist()
        y = subject_data[subject_y].tolist()
        cor = ut.ft_corr(x, y)
        corrs[(subject_x, subject_y)] = cor

    sorted_corrs = ut.ft_sort_corrs(corrs)
    top_3_pairs = sorted_corrs[:3]
    middle_index = len(corrs) // 2 - 1
    middle_3_pairs = sorted_corrs[middle_index:middle_index + 3]
    bottom_3_pairs = sorted_corrs[-3:]

    # サブプロットの設定
    fig, axes = plt.subplots(3, 3, figsize=(18, 10))
    fig.suptitle("Scatter Plots of Top 3, 3 in the middle, and Bottom 3 Correlated Feature Pairs")

    # 上位3つの散布図
    for i, (subjects_pair, corr_value) in enumerate(top_3_pairs):
        subject_x, subject_y = subjects_pair
        ax = axes[0, i]
        ax.scatter(data[subject_x], data[subject_y], alpha=0.6, color="skyblue")
        ax.set_title(f"{subject_x} vs {subject_y} (Corr: {corr_value:.2f})")
        ax.set_xlabel(subject_x)
        ax.set_ylabel(subject_y)
        ax.grid(True)

    #真ん中３つの分散図
    for i, (subjects_pair, corr_value) in enumerate(middle_3_pairs):
        subject_x, subject_y = subjects_pair
        ax = axes[1, i]
        ax.scatter(data[subject_x], data[subject_y], alpha=0.6, color="mediumseagreen")
        ax.set_title(f"{subject_x} vs {subject_y} (Corr: {corr_value:.2f})")
        ax.set_xlabel(subject_x)
        ax.set_ylabel(subject_y)
        ax.grid(True)

    # 下位3つの散布図
    for i, (subjects_pair, corr_value) in enumerate(bottom_3_pairs):
        subject_x, subject_y = subjects_pair
        ax = axes[2, i]
        ax.scatter(data[subject_x], data[subject_y], alpha=0.6, color="salmon")
        ax.set_title(f"{subject_x} vs {subject_y} (Corr: {corr_value:.2f})")
        ax.set_xlabel(subject_x)
        ax.set_ylabel(subject_y)
        ax.grid(True)

    # レイアウトの調整と表示
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()



if __name__ == "__main__":
    parser.check_arg_num(2)
    path = parser.check_path_ok(sys.argv[1])
    data = pd.read_csv(path)
    scatterplot(data)