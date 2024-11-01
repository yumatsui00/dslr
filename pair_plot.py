import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import utils as ut

ut.Check_args()

path = sys.argv[1]

ut.Check_path(path)

data = pd.read_csv(path)

if not "Hogwarts House" in data.columns:
    ut.Error_exit("There is no Hogwarts House Section")

if "Hogwarts House" in data.columns:
    pair_plot = sns.pairplot(data, hue="Hogwarts House", diag_kind="hist", plot_kws={'alpha': 0.5})
else:
    pair_plot = sns.pairplot(data, diag_kind="hist")

# ペアプロットを表示
plt.show()

#相関がない→