# Ref : http://dx.doi.org/10.1016/j.ins.2014.08.051
# Ref : https://cran.r-project.org/web/packages/DMwR/DMwR.pdf

# USAGE : rscript smoteipf.r <raw-data-csv> <output-csv>
# the last column of csv file should contain 'Y' or 'N'
# the file should contain a header and last column should be named 'Class'



library(DMwR)
library(data.table)

args = commandArgs(trailingOnly=TRUE)
d = read.csv(args[1],header = TRUE)

# change the below paramters accroding to requirment
YNcolumn = 36

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

y=countyes(d)
ov = ((length(d[,YNcolumn])-y)/y)*100
un = (ov*y/100)*100/(length(d[,YNcolumn])-(2*y))	#please ignore these
print("Original Data")
print(table(d$Class))

D = SMOTE(Class~.,d,perc.over=ov,perc.under=un,k=k_knn,learner=NULL)	#apply SMOTE on original data
print("SMOTEd Data")

print(table(D$Class))

fwrite(d,args[2])	#write final dataset to another csv
