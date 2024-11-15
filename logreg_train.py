import pandas as pd
import sys
import numpy as np
import utils.parser as parser
import utils.math as ft
from utils.trainer import LogisticRegression, Hogwarts

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


def logreg_train(data):
    UsefulData = ["Herbology","Divination","Muggle Studies","Ancient Runes","Charms","Flying"]
    data = data.dropna(subset=UsefulData).reset_index().drop(columns=['index'])
    dataX = data[UsefulData]
    dataY = data['Hogwarts House']
    X_train, Y_train, X_test, Y_test = split_train_and_test(dataX, dataY, test_size=0.3, random_state=4)

    # Xデータの標準化と、平均値、標準偏差の保持
    train = Hogwarts(X_train, Y_train)
    test = Hogwarts(X_test, Y_test)

    model = LogisticRegression()
    model.fit(train)

    prediction = model.predict(test.x)
    print(f"Score : {(len(test.x) - sum(test.y != prediction)) / len(test.x) * 100}%")
    model.save(train)





if __name__ == "__main__":
    parser.check_arg_num(2)
    parser.check_path(sys.argv[1])
    data = pd.read_csv(sys.argv[1])
    if not "Hogwarts House" in data.columns:
        parser.Error_exit("There is no Hogwarts Section")
    logreg_train(data)
