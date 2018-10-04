#input file as first argument

import numpy as np
from sklearn.neighbors import NearestNeighbors as NN
import sys
from random import random

class attributes_data(object):
	def __init__(self):
		self.data = []
		self.yesno = []
		self.data_index = []
		self.flags = [] 	#1 for safe, 0 for not-safe
		
f=open(sys.argv[1])

#change below parameters according to requirment
YNcolumn = 36	#column containing Y/N. This column should be last column of csv file.
ReasonColumn = -1	#Set this variable -1 if there is no column for reason.
heading_present = 1	# 1 if heading is present in csv file, 0 if not present.
K = 105 #Value of k in KNN
relabel = 1 #1 for Yes, 0 for No.



indices = range(0,YNcolumn)	#numbers in indices list should represent columns of float type
original = []
YNcolumn = YNcolumn-1
if heading_present:
	heading = f.readline()

for r in f.readlines():
	original.append(r[:-1].split(','))

orig_len = len(original)
f.close()




def knn_training_test_same(dataset,k_knn):
	data_numpy = np.array(dataset, dtype=np.float)
	nbrs = NN(n_neighbors=k_knn+1, algorithm='ball_tree').fit(data_numpy)
	distances,k_i = nbrs.kneighbors(data_numpy)
	return k_i

def knn_training_test_diff(trainset,testset,k_knn):
	train_numpy = np.array(trainset, dtype=np.float)
	test_numpy = np.array(testset, dtype=np.float)
	nbrs = NN(n_neighbors=k_knn+1, algorithm='ball_tree').fit(train_numpy)
	distances,k_i = nbrs.kneighbors(test_numpy)
	return k_i

def amplify(dest,src,example,example_index,k_knn):
	k_i = knn_training_test_diff(src.data,[example],k_knn)
	maj_n=0
	min_n=0
	for index in k_i[0][1:]:
		if src.yesno[index]=='N':
			maj_n += 1
		else:
			min_n += 1

	n = maj_n-min_n+1
	k_i = knn_training_test_diff(src.data,[example],n)
	for i in range(0,n):
		dest.data.append(example)
		dest.yesno.append('Y')
		dest.data_index.append(example_index)


def filewrite(file,group,synthetic_flag=0):
	L=len(group.yesno)
	for i in range(0,L):
		if synthetic_flag and ReasonColumn != -1:
			temp=original[group.data_index[i]][ReasonColumn]
			original[group.data_index[i]][ReasonColumn]='Synthetic'

		for j in range(0,YNcolumn):
			if j in indices:
				file.write(str(group.data[i][indices.index(j)])+',')
			else:
				file.write(original[group.data_index[i]][j]+',')
		file.write(group.yesno[i]+'\n')
		if synthetic_flag and ReasonColumn != -1:
			original[group.data_index[i]][ReasonColumn]=temp


def mainprocess(k,relabel):
	cpy = original
	DS = attributes_data()

	for i in range(0,orig_len):
		temp = []
		for index in indices:
			temp.append(float(cpy[i][index]))
		DS.data.append(temp)
		DS.yesno.append(cpy[i][YNcolumn])
		DS.data_index.append(i)

	#flag setting code starts
	knn_indices = knn_training_test_same(DS.data,k)

	for i,element in enumerate(knn_indices):
		positive = 0
		negetive = 0
		for e in element[1:]:
			if DS.yesno[e] == DS.yesno[i]:
				positive += 1
			else:
				negetive += 1
		if positive >= negetive:
			DS.flags.append(1)
		else:
			DS.flags.append(0)
	#flag setting code ends

	RS = attributes_data()

	for i,d in enumerate(DS.data):
		if DS.yesno[i]=='N' and DS.flags[i]==0:
			RS.data.append(d)
			RS.yesno.append('N')
			RS.flags.append(0)
			RS.data_index.append(DS.data_index[i])

	if relabel:
		for i,index in enumerate(RS.data_index):
			DS.yesno[index]='Y'
			if ReasonColumn != -1:
				cpy[index][ReasonColumn]='Relabled'
	else:
		for i,index in enumerate(RS.data_index):
			DS.data.pop(index-i)
			DS.data_index.pop(index-i)
			DS.yesno.pop(index-i)
			DS.flags.pop(index-i)

	DS.flags=[]

	#flag setting code starts
	knn_indices = knn_training_test_same(DS.data,k)

	for i,element in enumerate(knn_indices):
		positive = 0
		negetive = 0
		for e in element[1:]:
			if DS.yesno[e] == DS.yesno[i]:
				positive += 1
			else:
				negetive += 1
		if positive >= negetive:
			DS.flags.append(1)
		else:
			DS.flags.append(0)
	#flag setting code ends

	#ampl = 0
	outfile = open('k%dr%da0.csv'%(k,relabel),'w')
	if heading_present:
		outfile.write(heading)
	filewrite(outfile,DS,0)
	print ('%d\textra entries added to top of file k%dr%da0.csv'%(0,k,relabel))
	outfile.close()

	#ampl = 1
	extra = attributes_data()
	outfile = open('k%dr%da1.csv'%(k,relabel),'w')
	if heading_present:
		outfile.write(heading)
	L=len(DS.yesno)
	for i in range(0,L):
		if DS.yesno[i]=='Y' and DS.flags[i]==0:
			amplify(extra,DS,DS.data[i],DS.data_index[i],k)
	filewrite(outfile,extra,1)
	filewrite(outfile,DS,0)
	print ('%d\textra entries added to top of file k%dr%da1.csv'%(len(extra.yesno),k,relabel))
	outfile.close()

	#ampl = 2
	extra = attributes_data()
	outfile = open('k%dr%da2.csv'%(k,relabel),'w')
	if heading_present:
		outfile.write(heading)
	L=len(DS.yesno)
	for i in range(0,L):
		if DS.yesno[i]=='Y' and DS.flags[i]==0:
			knn_indices = knn_training_test_diff(DS.data,[DS.data[i]],k+2)
			positive = 0
			negetive = 0
			for index in knn_indices[0][1:]:
				if DS.yesno[index]=='Y':
					positive += 1
				else:
					negetive += 1
			if positive >= negetive:
				amplify(extra,DS,DS.data[i],DS.data_index[i],k)
			else:
				amplify(extra,DS,DS.data[i],DS.data_index[i],k+2)
	filewrite(outfile,extra,1)
	filewrite(outfile,DS,0)
	print ('%d\textra entries added to top of file k%dr%da2.csv'%(len(extra.yesno),k,relabel))
	outfile.close()


if __name__=='__main__':
	mainprocess(K,relabel)
