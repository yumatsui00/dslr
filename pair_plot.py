import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import sys
from utils import math as ft
from utils import parser
from utils import utils as ut
from utils import error as er


def pair_plot(data):
    if not "Hogwarts House" in data.columns:
        er.Error_exit("There is no Hogwarts House Section")

    if "Hogwarts House" in data.columns:
        pair_plot = sns.pairplot(data, hue="Hogwarts House", diag_kind="hist", plot_kws={'alpha': 0.5})
    else:
        pair_plot = sns.pairplot(data, diag_kind="hist")

    # ペアプロットを表示
    plt.show()

if __name__ == "__main__":
    parser.check_arg_num(2)
    path = parser.check_path_ok(sys.argv[1])
    data = pd.read_csv(path)
    pair_plot(data)