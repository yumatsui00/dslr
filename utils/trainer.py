import numpy as np
import utils.math as ft
import os

class Hogwarts(object):
    """Hogwarts class which keeps dataFrame as array
    init Parameters
    X: dataFrame,
    Y: answer data"""
    def __init__(self, X, Y):
        self.x = X.to_numpy()
        self.y = Y.to_numpy()
        self.columns = X.columns
        self.mean = []
        self.std = []
        for i in range(ft._len(self.columns)):
            col_data = self.x[:, i]
            col_mean = ft._mean(col_data)
            col_std = ft._std(col_data)

            self.mean.append(col_mean)
            self.std.append(col_std)
            self.x[:, i] = (self.x[:, i] - self.mean[i]) / self.std[i]


class LogisticRegression(object):
    """Logistic Regression class
    Parameters
    LR: float, default: 0.1 Learning Rate
    Iter: int, defautl 100
    Lambda: int, default 0"""

    def __init__(self, LR=0.001, Iter=1000, Lambda=0.001, weight=None, labels=None):
        self.LR = LR
        self.Iter = Iter
        self.Lambda = Lambda
        self.weight = weight
        self._labels = labels
        self._cost = []
        self._errors = []

    def fit(self, data: Hogwarts, sample_weight=None):
        """function to train model"""
        self._labels = np.unique(data.y).tolist()
        newX = np.insert(data.x, 0, 1, axis=1)
        size = newX.shape[0]
        self.weight = sample_weight
        if self.weight is None:
            self.weight = np.zeros((ft._len(self._labels), newX.shape[1])) #重みはクラス数×（特徴数＋１）　１はバイアス項
        #print(self.weight) #行：クラス、列：特徴
        vectorY = np.zeros((ft._len(data.y), ft._len(self._labels)))
        for i in range(0, ft._len(data.y)):
            vectorY[i, self._labels.index(data.y[i])] = 1
        #print(vectorY) #vectorY　列：クラス、行：生徒のデータ　であり、その生徒のクラスの部分に１が入る

        for _ in range(self.Iter):
            predictions = self.net_input(newX).T  #net_inputはニューラルネットワークの各ノードに渡される重み付き合計
            #print(predictions)

            lhs = vectorY.T.dot(np.log(predictions))
            rhs = (1 - vectorY).T.dot(np.log(1 - predictions))
            #print(lhs)
            #print(rhs)

            #r1 = (self.Lambda / (2 * size)) * ft._sum(ft._sum(self.weight[:, 1:] ** 2)) #重みの正則化項
            #cost = (-1 / size) * ft._sum(lhs + rhs) + r1 #コスト関数は精度評価のために用いる。
            #print(cost) #コスト関数の最小化を目指して学習率や試行回数を調整する

            r2 = (self.Lambda / size) * self.weight[:, 1:]
            self.weight = self.weight - (self.LR * (1 / size) * (predictions - vectorY).T.dot(newX) + np.insert(r2, 0, 0, axis=1))

        return self


    def net_input(self, x):
        z = self.weight.dot(x.T)
        sigmoidZ = 1 / (1 + np.exp(-z))
        #print(sigmoidZ)
        return sigmoidZ


    def predict(self, x):
        x = np.insert(x, 0, 1, axis=1)
        prediction = self.net_input(x).T
        #print(prediction)
        return [self._labels[i] for i in prediction.argmax(1)] #各クラスのうち、最大値のラベルを返す


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
