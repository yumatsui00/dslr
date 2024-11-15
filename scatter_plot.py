import utils.parser as parser
import utils.math as ft
import sys
import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt

def scatterplot(data):
    if not "Hogwarts House" in data.columns:
        parser.Error_exit("There is no Hogwarts House Section")

    subjects = data.select_dtypes(include="number").columns.drop("Index")
    corrs = {}

    for subject_x, subject_y in combinations(subjects, 2):
        subject_data = data[[subject_x, subject_y]].dropna()
        x = subject_data[subject_x].tolist()
        y = subject_data[subject_y].tolist()
        #print(subject_data)
        corr = ft._corr(x, y)
        corrs[(subject_x, subject_y)] = corr

    sorted_corrs = list(ft._sort(corrs, order="des", type="dict").items())
    top3pairs = sorted_corrs[:3]
    middle_index = len(corrs) // 2 - 1
    middle3pairs = sorted_corrs[middle_index:middle_index + 3]
    bottom3pairs = sorted_corrs[-3:]

    fig, axes = plt.subplots(3, 3, figsize=(18, 10))
    fig.suptitle("Scatter Plots of Top 3, 3 in the middle, and Bottom 3 Correlated Feature Pairs")

    for i, (subjects_pair, corr_value) in enumerate(top3pairs):
        subject_x, subject_y = subjects_pair
        ax = axes[0, i]
        ax.scatter(data[subject_x], data[subject_y], alpha=0.6, color="skyblue")
        ax.set_title(f"{subject_x} vs {subject_y} (Corr: {corr_value:.2f})")
        ax.set_xlabel(subject_x)
        ax.set_ylabel(subject_y)
        ax.grid(True)

    #真ん中３つの分散図
    for i, (subjects_pair, corr_value) in enumerate(middle3pairs):
        subject_x, subject_y = subjects_pair
        ax = axes[1, i]
        ax.scatter(data[subject_x], data[subject_y], alpha=0.6, color="mediumseagreen")
        ax.set_title(f"{subject_x} vs {subject_y} (Corr: {corr_value:.2f})")
        ax.set_xlabel(subject_x)
        ax.set_ylabel(subject_y)
        ax.grid(True)

    # 下位3つの散布図
    for i, (subjects_pair, corr_value) in enumerate(bottom3pairs):
        subject_x, subject_y = subjects_pair
        ax = axes[2, i]
        ax.scatter(data[subject_x], data[subject_y], alpha=0.6, color="salmon")
        ax.set_title(f"{subject_x} vs {subject_y} (Corr: {corr_value:.2f})")
        ax.set_xlabel(subject_x)
        ax.set_ylabel(subject_y)
        ax.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    parser.check_arg_num(2)
    parser.check_path(sys.argv[1])
    data = pd.read_csv(sys.argv[1])
    scatterplot(data)
