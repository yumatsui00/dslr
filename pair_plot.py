import seaborn as sns
import sys
import pandas as pd
import matplotlib.pyplot as plt
import utils.parser as parser



def pair_plot(data):
    if "Hogwarts House" in data.columns:
        sns.pairplot(data, hue="Hogwarts House", diag_kind="hist", plot_kws={'alpha': 0.5})
    else:
        sns.pairplot(data, diag_kind="hist")

    # ペアプロットを表示
    plt.show()


if __name__ == "__main__":
    parser.check_arg_num(2)
    parser.check_path(sys.argv[1])
    data = pd.read_csv(sys.argv[1])
    pair_plot(data)
