import os

path = "../data/"
filenames = list()
sub_dir = os.listdir(path)
for d in sub_dir:
	files = os.listdir(path+d+'/')
	for f in files:
		filenames.append(f)



fp = open('en.qrels.126-175.2011.txt','r')
wp = open('output.txt', 'w')
for line in fp:
	name = line.strip().split(' ')[2]
	if name in filenames:
		wp.write(line)
		

