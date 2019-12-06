from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import math
from math import *
import csv


app = Flask(__name__)


def calculateDistance(user_input):

    my_real_data = pd.read_csv("filtered.csv")
    my_real_data["genres"] = my_real_data["genres"].str.split("|", n=20)
    var = ([], [])
    for index, row in my_real_data.iterrows():
        if row['title'] == user_input:
            var = (row[3], row[2])
            break

    if len(var[1]) == 0:
        return [], []

    listOfvalues = []
    listOfFound = []
    listOfAdded = []
    for i in range(0, len(var[1])):
        listOfvalues.append((var[1][i], i))
    for i in range(0, len(var[1])):
        listOfFound.append(0)
    for i in range(len(var[1])):
        listOfAdded.append(1)
    listOfAdded.append(var[0])
    distance = []
    for index, row in my_real_data.iterrows():
        # matches=set(var[1])&set(row[2])
        # value=math.sqrt((row[3]-var[0])*(row[3]-var[0])+(len(var[1])-len(matches)))
        # distance.append((value,row[0]))
        # distance.sort()

        listOfFound = [0] * (len(var[1]))
        for index in range(len(var[1])):  # traversing thro length of the list
            for x in row[2]:
                if var[1][index] == x:
                    listOfFound[index] = 1
        listOfFound.append(row[3])

        distancec = math.sqrt(
            sum([(a - b) ** 2 for a, b in zip(listOfFound, listOfAdded)]))
        distance.append((distancec, row[0]))
        distance = sorted(distance)[:5]

    recommended = []
    for i in range(len(distance)):
        for index, row in my_real_data.iterrows():
            if row['movieId'] == distance[i][1]:
                recommended.append(
                    {'movieId': row[0], 'title': row[1], 'genres': row[2], 'rating': row[3]})
    return recommended, var[1]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie', methods=['POST', 'GET'])
def movie():
    dic = request.form.to_dict()
    user_input = dic['Movie']
    recommended, category = calculateDistance(user_input)
    # if category == (-100, -100):
    if len(recommended) == 0:
        return render_template('index.html', movie="No Record Found")
    else:
        return render_template('index.html', movie=user_input, category=category, l=recommended)


if __name__ == "__main__":
    app.run(debug=True)
