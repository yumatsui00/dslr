import pandas as pd
import sys
import numpy as np
import math
import utils.parser as parser
import utils.math as ft
from utils.trainer import LogisticRegression, Hogwarts
from itertools import combinations

def split_train_and_test(x, y, test_size=0.3, random_state=None):
    if random_state:
        np.random.seed(random_state)
    p = np.random.permutation(ft._len(x.index))
    testsize = int(ft._len(x.index) * test_size)
    x = x.iloc[p].reset_index(drop=True) #シャッフル
    y = y.iloc[p].reset_index(drop=True) #シャッフル

    x_test_data = x[:testsize]
    x_train_data = x[testsize:]

    y_test_data = y[:testsize]
    y_train_data = y[testsize:]
    return x_train_data, y_train_data, x_test_data, y_test_data


def logreg_traina(data, features):
    UsefulData = features
    #print(features)
    data = data.dropna(subset=UsefulData).reset_index().drop(columns=['index'])
    dataX = data[UsefulData]
    dataY = data['Hogwarts House']
    X_train, Y_train, X_test, Y_test = split_train_and_test(dataX, dataY, test_size=0.3)

    # Xデータの標準化と、平均値、標準偏差の保持
    train = Hogwarts(X_train, Y_train)
    test = Hogwarts(X_test, Y_test)

    if len(test.x) == 0:
        return 0
    model = LogisticRegression()
    model.fit(train)

    prediction = model.predict(test.x)
    #print(f"Score : {(len(test.x) - sum(test.y != prediction)) / len(test.x) * 100}%")
    return (len(test.x) - sum(test.y != prediction)) / len(test.x) * 100



if __name__ == "__main__":
    parser.check_arg_num(2)
    parser.check_path(sys.argv[1])
    data = pd.read_csv(sys.argv[1])
    if not "Hogwarts House" in data.columns:
        parser.Error_exit("There is no Hogwarts House Section")
    all_features = ["Herbology","Divination","Muggle Studies","Ancient Runes","Charms","Flying"]
    scores = []
    best_score = 0
    best_features = []
    #for r in range(1, len(all_features) + 1):
    #    for features in combinations(all_features, r):
    #        if len(features) < 4:
    #            continue

    #        res = []
    #        for i in range(5):
    #            ans = logreg_traina(data, list(features))
    #            if ans < 97 or math.isnan(ans):
    #                break
    #            res.append(ans)
    #        if ft._mean(res) < 98 or math.isnan(ft._mean(res)):
    #            continue
    #        score = ft._mean(res)
    #        print(f"Features: {features}, Score: {score}%")

    #        # 最高スコアを更新
    #        if score > best_score:
    #            best_score = score
    #            best_features = features
    #print(f"Best Features: {best_features}, Best Score: {best_score}%")

    res = []
    for i in range(20):
        res.append(logreg_traina(data, all_features))
    print(f"Final Score : {ft._mean(res)}%")


    #Features: ('Arithmancy', 'Herbology', 'Defense Against the Dark Arts', 'Ancient Runes'), Score: 98.73015873015873%
    #Features: ('Astronomy', 'Defense Against the Dark Arts', 'Ancient Runes', 'Charms'), Score: 98.55555555555556%
    #Features: ('Herbology', 'Defense Against the Dark Arts', 'Divination', 'Ancient Runes'), Score: 98.58769931662871%
    #Features: ('Herbology', 'Defense Against the Dark Arts', 'Muggle Studies', 'Potions'), Score: 98.54875283446711%
    #Features: ('Defense Against the Dark Arts', 'Divination', 'Ancient Runes', 'Care of Magical Creatures'), Score: 98.63013698630137%

    #Features: ('Astronomy', 'Defense Against the Dark Arts', 'Divination', 'Ancient Runes', 'Flying'), Score: 98.58769931662871%
    #Features: ('Herbology', 'Defense Against the Dark Arts', 'Muggle Studies', 'Ancient Runes', 'Flying'), Score: 98.5909090909091%
    #Features: ('Herbology', 'Defense Against the Dark Arts', 'Muggle Studies', 'Ancient Runes', 'Flying'), Score: 98.5909090909091%
    #Features: ('Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'Charms', 'Flying'), Score: 98.63013698630138%
    #Features: ('Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'Flying'), Score: 98.52380952380953%
#    Features: ('Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'Charms', 'Flying'), Score: 98.66666666666666%
#Best Features: ('Herbology', 'Divination', 'Muggle Studies', 'Ancient Runes', 'Charms', 'Flying'), Best Score: 98.7214611872146