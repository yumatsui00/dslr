#方法１特徴のある教科を抽出して、それらを重みとして計算する
#方法２特徴のあるペアを抽出して、小さな回帰モデルを作成。それらの重みを合計した大きな回帰モデルを作成
#４つの１対多のロジスティック回帰モデルを作成
#Astronomy vs Herbology
#Herbology vs Against the Dark Arts
#Astronomy vs Acient Runes
#Herbology vs Acient Runes
#Against the Dark Arts vs Acient Runes
#Charmsは複数の科目で分離が容易そうだが、線形的な分離の際に教会を分けるのが難しそうなので一旦考慮に入れない
import pandas as pd
import sys
import numpy as np
from utils import math as ft
from utils import parser
from utils import utils as ut
from utils import error as er
from utils.trainer import LogisticRegression, Hogwarts

def split_train_and_test(x, y, test_size=0.3, random_state=None):
    """split data into testdata and traindata randomly"""
    if random_state:
        np.random.seed(random_state) # randomのシード値があったら設定
    p = np.random.permutation(len(x)) # len(x)の長さのインデックス配列をランダムにしたものを生成
    testsize = int(len(x) * test_size)
    x = x.iloc[p].reset_index(drop=True) #シャッフル
    y = y.iloc[p].reset_index(drop=True) #シャッフル

    x_test_data = x[:testsize]
    x_train_data = x[testsize:]

    y_test_data = y[:testsize]
    y_train_data = y[testsize:]
    return x_train_data, y_train_data, x_test_data, y_test_data



def logreg_train(data):
    UsefulData = ['Charms', 'Herbology', 'Defense Against the Dark Arts', 'Flying']
    data = data.dropna(subset=UsefulData).reset_index().drop(columns=['index'])
    dataX = data[UsefulData]
    dataY = data['Hogwarts House']
    X_train, Y_train, X_test, Y_test = split_train_and_test(dataX, dataY, test_size=0.3, random_state=0)

    #今回はクラス分離が目標なので、標準化したあとにもとのサイズに戻す必要はない
    train = Hogwarts(X_train, Y_train)
    test = Hogwarts(X_test, Y_test)

    print(train.x)
    model = LogisticRegression(0.1, 100)
    model.fit(train)

    prediction = model.inspect(test.x)
    print(f"Score : {(len(test.x) - sum(test.y != prediction)) / len(test.x) * 100}%")
    model.save(train)





if __name__ == "__main__":
    parser.check_arg_num(2)
    path = parser.check_path_ok(sys.argv[1])
    data = pd.read_csv(path)
    if not "Hogwarts House" in data.columns:
        er.Error_exit("There is no Hogwarts House Section")
    logreg_train(data)
