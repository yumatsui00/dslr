import pandas as pd
import sys
import numpy as np
from utils import math as ft
from utils import parser
from utils.trainer import LogisticRegression, Hogwarts

def logreg_predict(data):
    UsefulData = ["Herbology","Divination","Muggle Studies","Ancient Runes","Charms","Flying"]
    data = data[UsefulData]
    data = np.array(data)
    try:
        df = pd.read_csv("./data/weights.csv")
    except FileNotFoundError:
        print("Error: Couldn't find './data/weights.csv'")
    except pd.errors.EmptyDataError:
        print("Error: Couldn't find './data/weights.csv'")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    #print(df)
    labels = list(df)[:4]
    #print(labels)
    mean = df.values[1:, 4]
    #print(mean)
    std = df.values[1:, 5]
    #print(std)
    weights = df.values[:, :4].T
    #print(weights)
    data = (data - mean) / std #標準化
    #print(data)
    model = LogisticRegression(weight=weights, labels=labels)
    prediction = model.predict(data)
    #print(prediction)
    f = open("./data/house.csv", "+w")
    f.write("Index,Hogwarts House\n")
    for i in range(0, len(prediction)):
        f.write(f'{i},{prediction[i]}\n')


if __name__ == "__main__":
    parser.check_arg_num(2)
    parser.check_path(sys.argv[1])
    data = pd.read_csv(sys.argv[1])
    if not "Hogwarts House" in data.columns:
        parser.Error_exit("There is no Hogwarts House Section")
    if not data["Hogwarts House"].isnull().all():
        parser.Error_exit("Hogwarts house column contains data")
    logreg_predict(data)