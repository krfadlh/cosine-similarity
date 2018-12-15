from flask import Flask, render_template, request
import pandas as pd
import json
import webbrowser
import numpy as np
import math
import copy

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def process():
	if request.method == 'GET':
		return render_template('result.html')

	elif request.method =='POST':
		keyword = request.form['keyword']
		datasets = pd.read_csv("data/datasets.csv")
		dokumen = datasets.values.tolist()
		index = pd.read_csv("data/index.csv")
		index = index.values.tolist()
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		result = [[] for i in range(len(dokumen))]
		data = []

		temp = keyword.split()
		temp = set(temp)
		temp = list(temp)
		kata = [[] for i in range(len(temp))]

		for i in range(len(temp)):
			kata[i].append(temp[i])

		temp = keyword.split()

		for i in range(len(kata)):
			kata[i].append(temp.count(kata[i][0]))

		temp = set(temp)
		temp = list(temp)

		index = [x for x in index if x[0] in temp]

		index = sorted(index, key=lambda x: x[0])
		kata = sorted(kata, key=lambda x: x[0])

		for i in range(len(dokumen)):
			result[i].append(i+1)
			temp = 0
			for n in range(len(index)):
				temp += index[n][i+1]*kata[n][1]
			result[i].append(temp)

		result = [x for x in result if x[1] > 0]
		
		result = sorted(result, key=lambda x: x[1], reverse=True)

		for i in range(len(result)):
			data.append(dokumen[result[i][0]-1])		

		return render_template('result.html', keyword=keyword, data=data)

	# else:
 #        '<center>404 Not Found</center>'

# run app
if __name__ == "__main__":
    app.run(debug=True)