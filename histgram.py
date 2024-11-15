import utils.parser as parser
import utils.math as ft
import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

def histogram(data):
    if not "Hogwarts House" in data.columns:
        parser.Error_exit("There is no Hogwarts House Section")

    subjects = data.select_dtypes(include="number").columns.drop("Index")

    subjects_count = ft._len(subjects)
    cols = 3
    rows = (subjects_count // cols + 1)

    fig, axes= plt.subplots(rows, cols, figsize=(10 * cols, 6 * rows))
    fig.canvas.manager.set_window_title("Hogwarts Score Distribution")
    axes = axes.flatten()

    for i, subject in enumerate(subjects):
        ax = axes[i]
        for house in data["Hogwarts House"].unique():
            house_data = data[data["Hogwarts House"] == house][subject].dropna()
            ax.hist(house_data, bins=15, alpha=0.5, label=house)
        ax.set_title(f"{subject} Scores")
        ax.set_xlabel("Score")
        ax.set_ylabel("Frequency")
        ax.legend()

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(pad=2.0, h_pad=2.5, w_pad=2.5)
    #plt.show()

    results = []
    for subject in subjects:
        house_data = []
        for house in data["Hogwarts House"].unique():
            scores = data[data["Hogwarts House"] == house][subject].dropna()
            house_data.append(scores)
        ks = []
        for i in range(ft._len(house)):
            for j in range(i + 1, ft._len(house_data)):
                stat, _ = ks_2samp(house_data[i], house_data[j])
                ks.append(stat)
        ks_mean = ft._mean(ks)
        results.append({
            "Subject": subject,
            "KS_mean": ks_mean,
        })

    res_ser = pd.Series({result["Subject"]: result["KS_mean"] for result in results})
    print("KS検定による均一性評価")
    sorted_res_ser = ft._sort(res_ser, type="series", sort_index=1)
    print(sorted_res_ser)

    plt.show()



if __name__ == "__main__":
    parser.check_arg_num(2)
    parser = parser.check_path(sys.argv[1])
    data = pd.read_csv(sys.argv[1])
    histogram(data)
