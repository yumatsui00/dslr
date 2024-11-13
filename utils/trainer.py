import numpy as np
import utils.math as ft
import os


class Hogwarts(object):
    """This class keeps dataFrame as arrays
    This keeps mean, std, and normalized x and y"""
    def __init__(self, X, Y):
        self.x = X.to_numpy()
        self.y = Y.to_numpy()
        self.columns = X.columns
        self.mean = []
        self.std = []
        for i in range(len(self.columns)):
            self.mean.append(ft._mean(self.x[:, i]))
            self.std.append(ft._std(self.x[:, i]))
            self.x[:, i] = (self.x[:, i] - self.mean[i]) / self.std[i]


class LogisticRegression(object):
    """Logistic Regression class
    Parameters
    LR: float default: 0.1   Learning Rate
    Iter: int default: 100
    """

    def __init__(self, LR=0.1, Iter=100, Lambda=0, weight=None, labels=None):
        self.LR = LR
        self.Iter = 100
        self.Lambda = Lambda
        self.weight = weight
        self._labels = labels
        self._cost = []
        self._errors = []

    def fit(self, data: Hogwarts, sample_weight=None):
        self._labels = np.unique(data.y).tolist() #uniqueなlabelを取得
        newX = np.insert(data.x, 0, 1, axis=1) #ｘ行列に切片項を追加し、計算しやすくする
        size = newX.shape[0] #データの量を取得
        self.weight = sample_weight #サンプルの重みがあったら追加。なかったら初期化
        if self.weight is None:
            self.weight = np.zeros(newX.shape[1] * len(self._labels))
        self.weight = self.weight.reshape(len(self._labels), newX.shape[1])

        vectorY = np.zeros((len(data.y), len(self._labels))) # yのラベル情報を、後の計算のために行列に変換
        for i in range(0, len(data.y)):
            vectorY[i, self._labels.index(data.y[i])] = 1

        for _ in range(0, self.Iter):
            predictions = self.predict(newX).T #predictionは各クラスの確率を含む行列

            lhs = vectorY.T.dot(np.log(predictions)) #正解クラスの対数確率を計算
            rhs = (1 - vectorY).T.dot(np.log(1 - predictions)) #不正解クラスの対数確率を計算

            r1 = (self.Lambda / (2 * size)) * ft._sum(ft._sum(self.weight[:, 1:] ** 2)) #バイアス項を除いた、重みの正則化項を計算する
            cost = (-1 / size) * ft._sum(lhs + rhs) + r1
            self._cost.append(cost)
            self._errors.append(ft._sum(data.y != self.inspect(data.x)))

            r2 = (self.Lambda / size) * self.weight[:, 1:]
            self.weight = self.weight - (self.LR * (1 / size) * (predictions - vectorY).T.dot(newX) + np.insert(r2, 0, 0, axis=1))
            print(cost)
        return self



    def save(self, data, filename="./data/weights.csv"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f = open(filename, 'w+')
        for i in range(0, len(self._labels)):
            f.write(f'{self._labels[i]},')
        f.write('Mean,Std\n')

        for i in range(0, self.weight.shape[1]):
            for j in range(0, self.weight.shape[0]):
                f.write(f'{self.weight[j][i]},')
            f.write(f'{data.mean[i - 1] if i > 0 else ""},{data.std[i - 1] if i > 0 else ""}\n')
        f.close()
        return self

    def predict(self, x):
        z = self.weight.dot(x.T)
        sigmoidZ = 1 / (1 + np.exp(-z))
        return sigmoidZ

    def inspect(self, x):
        x = np.insert(x, 0, 1, axis=1)
        prediction = self.predict(x).T
        return [self._labels[i] for i in prediction.argmax(1)]
