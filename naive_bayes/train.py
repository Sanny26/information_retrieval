'''
Acheived an accuracy of 50% on approx. 100 docs from spam and ham both.
'''

import os
from naive_bayes import NaiveBayes
from utils import *
import pdb

def read_file(f_path):
	text = open(f_path,'r').read().decode('utf8')
	text = preprocess(text)
	return text


if __name__ == "__main__":
	data_path = "enron1/"
	sub_dir = os.listdir(data_path)
	N = NaiveBayes()
	print('Loading Train Data')

	for directory in sub_dir:
		if directory in ['spam', 'ham']:
			dir_path = data_path+directory+'/'
			files = os.listdir(dir_path)
			for f in files:
				label = f.split('.')[3]
				text = read_file(dir_path+f)
				N.add_data(text, label)

	print('Training model')
	N.update_class_probability()
	N.update_vocab()
	N.update_P_wc()

	print('Testing model')
	correct = 0
	total = 0
	test_path = data_path+"test/"
	files = os.listdir(test_path)
	for f in files:
		print total
		label = f.split('.')[3]
		text = read_file(test_path+f)
		predict = N.test(text)
		if predict == label:
			correct += 1
		total += 1

	print('Accuracy for Enron1 SPAM/HAM  data is ', float(correct)/total )




