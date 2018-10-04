# Ref : http://dx.doi.org/10.1016/j.ins.2014.08.051
# J.A. Sáez et al., SMOTE–IPF : Addressing the noisy and borderline examples problem in imbalanced classification by a re-sampling method with filtering, Inform. Sci. (2014)

# USAGE : rscript smoteipf.r <raw-data-csv> <output-csv>
# the last column of csv file should contain 'Y' or 'N'
# the file should contain a header and last column should be named 'Class'

library(RWeka)
library(DMwR)
library(data.table)

args = commandArgs(trailingOnly=TRUE)
d = read.csv(args[1],header = TRUE)

# change the below paramters accroding to requirment
YNcolumn = 36

# print("Number of sub-datsets to make : ")
n=9 # as.integer(readLines("stdin",n=1))

# print("Number of iterations to identify noisy examples : ")
k=3 # as.integer(readLines("stdin",n=1))

# print("1 for majority, 0 for consensus : ")
voting=1 # as.integer(readLines("stdin",n=1))

# print("Percentage of original dataset considered for filtering : ")
p=1.0 # as.numeric(readLines("stdin",n=1))

# print("Specify k as in knn of SMOTE : ")
k_knn=11 # k_knn=as.integer(readLines("stdin",n=1))

countyes <- function(dataset)
{
	y=0
	for (cl in dataset[,YNcolumn])
	{
		if (cl=="Y")
			y=y+1
	}
	return (y)
}

shuffleSmotedData <- function(dataset)
{
	for (i in 1:3)
		dataset = dataset[sample(nrow(dataset)),]
	return (dataset)
}

y=countyes(d)
ov = ((length(d[,YNcolumn])-y)/y)*100
un = (ov*y/100)*100/(length(d[,YNcolumn])-(2*y))	#please ignore these
print("Original Data")
print(table(d$Class))

D = SMOTE(Class~.,d,perc.over=ov,perc.under=un,k=k_knn,learner=NULL)	#apply SMOTE on original data
print("SMOTEd Data")
print(table(D$Class))

P = sapply((length(d[,1])*p)/100,as.integer)	#maximum no of tolerable noisy instances in each iteration

i_k=0
while(i_k<k)
{
	L=length(D[,1])	#no of rows in D(Smoted Dataset)
	step = as.integer(L/n)	#length of each sub-dataset

	models = vector(mode="list",length=n)
	D=shuffleSmotedData(D)	#shuffle D randomly such that each sub-datset contains roughly equal 'Y' and 'N'

	for (i in 0:(n-2))
	{
		models[[i+1]] = J48(as.factor(Class)~.,D[(i*step+1):((i+1)*step),])	#append each tree generated through subsets into models
	}
	models[[n]] = J48(as.factor(Class)~.,D[(n-1)*step+1:length(D[,1]),])
	predictions = vector(mode="list",length=n)
	for (i in 1:n)
	{
		predictions[[i]] = predict(models[[i]],newdata=D)	#run the whole dataset through each model
	}
	
	temp_indices=c()	#stores indices of noisy data
	i_t=0	#counter for above variable
	if (voting==1)	#for majority
	{
		for (i in 1:L)
		{
			positive=0
			negetive=0
			for (j in 1:n)
			{
				if (D$Class[i]==predictions[[j]][i])
					positive=positive+1
				else
					negetive=negetive+1
			}
			if (positive<negetive)
			{
				i_t=i_t+1
				temp_indices[i_t]=i
			}
		}
	}
	else 	#for consensus
	{
		for (i in 1:L)
		{
			misclassified_by_all=1
			for (j in 1:n)
			{
				if (D$Class[i]==predictions[[j]][i])
				{
					misclassified_by_all=0
					break
				}
			}
			if (misclassified_by_all==1)
			{
				i_t=i_t+1
				temp_indices[i_t]=i
			}
		}
	}
	D=D[-temp_indices,]	#remove noisy examples

	if (i_t<=P)	#no of noisy examples less than P : increment counter
		i_k=i_k+1
	else 	#set counter to 0
		i_k=0
	print(".")
}

print("Filtered Data")
print(table(D$Class))

fwrite(D,args[2])	#write final dataset to another csv
