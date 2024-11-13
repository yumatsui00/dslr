#KS検定を選んだ理由：今回はデータの基準値もバラバラ（点数の満点も違う）なので、分散をとってもあまり意味ない。科目毎にかなり差が出てしまう
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.stats import ks_2samp
from utils import math as ft
from utils import parser
from utils import utils as ut



def histogram(data):
    if not "Hogwarts House" in data.columns:
        ut.Error_exit("There is no Hogwarts House Section")

    subjects = data.select_dtypes(include='number').columns.drop("Index")

    # サブプロットの設定（科目の数に合わせて行と列を設定）
    num_subjects = len(subjects)
    cols = 3
    rows = (num_subjects // cols + 1)

    fig, axes = plt.subplots(rows, cols, figsize=(10 * cols, 6 * rows))
    fig.canvas.manager.set_window_title("Hogwarts Scores Distribution")
    axes = axes.flatten()  # これにより、axes[i]で各サブプロットにアクセス可能

    # 各科目ごとにヒストグラムを作成
    for i, subject in enumerate(subjects):
        ax = axes[i]
        for house in data["Hogwarts House"].unique(): #ユニークな両名に対してループを回している　
            house_data = data[data["Hogwarts House"] == house][subject].dropna()#寮名に等しいインデックスの中のサブジェクト
            ax.hist(house_data, bins=15, alpha=0.5, label=house)#histgram(ax)に描画する、１５個の区画、５０％の透明度

        # 各サブプロットの設定
        ax.set_title(f"{subject} Scores")
        ax.set_xlabel("Score")
        ax.set_ylabel("Frequency")
        ax.legend()

    # 空のサブプロットがある場合は非表示にする
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(pad=2.0, h_pad=2.5, w_pad=2.5)

    #KS検定を用いたデータ分布が最も均一な科目調査
    #KS検定とは：２つのサンプル分布が同じ分布から取られているかを確認したいときや、理論的な分布に従っているかを確認したいときに利用される

    results = []

    for subject in subjects:
        house_data = []
        for house in data["Hogwarts House"].unique(): #ユニークな値だけで周回する
            scores = data[data["Hogwarts House"] == house][subject].dropna()#寮の名前が一致したデータをすべてscoresに格納
            house_data.append(scores)

        # K-S検定の結果を計算（分布の差異が小さいほど均一）
        ks_stats = []
        for i in range(len(house_data)):
            for j in range(i + 1, len(house_data)):
                ks_stat, _ = ks_2samp(house_data[i], house_data[j])#これ自分で作ったほうがいい？
                ks_stats.append(ks_stat)

        ks_mean = ut.ft_mean(ks_stats)

        # 結果をリストに追加
        results.append({
            "Subject": subject,
            "KS_Mean": ks_mean,
        })

    results_series = pd.Series({result["Subject"]: result["KS_Mean"] for result in results})

    # KS検定の結果から均一性の高い順に表示
    print("KS検定による均一性測定の結果")
    print(ut.ft_sort_values(results_series))

    fig, ax = plt.subplots(figsize=(10, 6))
    results_series_sorted = ut.ft_sort_values(results_series)

    # KS_Meanのヒストグラムを作成
    ax.bar(results_series_sorted.index, results_series_sorted.values, color='skyblue')
    ax.set_title("Uniformity of Subjects based on KS Test")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("KS Mean (Uniformity)")
    #ax.set_xticklabels(results_series_sorted.index, rotation=45, ha="right")

    # レイアウトの調整と表示
    plt.tight_layout(pad=2.0, h_pad=2.5, w_pad=2.5)
    plt.show()


if __name__ == "__main__":
    parser.check_arg_num(2)
    path = parser.check_path_ok(sys.argv[1])
    data = pd.read_csv(path)
    histogram(data)