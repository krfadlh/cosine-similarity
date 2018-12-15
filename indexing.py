from collections import Counter
import pandas as pd
import numpy as np
from pprint import pprint

tandaBaca = ['.',',',':','\"','/','(',')','-',';','\\','{','}','!','@','#','$','^','&','*']
datasets = pd.read_csv("data/datasets.csv")
dokumen = datasets.values.tolist()
docs, index = [], []

for baris in dokumen:
	temp = list(baris[3])
	temp = [x.lower() for x in temp if x not in tandaBaca]
	temp = "".join(temp)
	docs.append(temp.split())

for record in docs:
	for kata in record:
		if kata.lower() not in index:
			index.append(kata.lower())

df_index = pd.DataFrame({
	'kata':index
	})

for i in range(len(docs)):
	terdeteksi = []
	for kata in index:
		terdeteksi.append(docs[i].count(kata.lower()))
	df_index[i+1] = pd.Series(terdeteksi)

df_index.to_csv("data/index.csv", index=False)