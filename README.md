# oversampling-techniques

## SMOTE
Input file should contain Yes/No Class and header. The header of Yes/No Column should be named 'Class'. Entries in Yes/No Column should be either 'Y' or 'N'. Input File should be in csv format.

Change k in KNN for SMOTE by changing the variable 'k_knn' in smote.r . Change 'YNcolumn' variable to indicate column number of Yes/No Column. Column numbers start  from 1.

File Usage : rscript smote.r <input.csv> <output.csv>


## SMOTE-IPF
Input file should contain Yes/No Class and header. The header of Yes/No Column should be named 'Class'. Entries in Yes/No Column should be either 'Y' or 'N'. Input File should be in csv format.

Change k in KNN for SMOTE by changing the variable 'k_knn' in smoteipf.r . Change 'YNcolumn' variable to indicate column number of Yes/No Column. Column numbers start  from 1.

Also, variable 'n', 'k', 'voting', 'p' can be changed accordingly. For information on these variables visit : https://www.sciencedirect.com/science/article/pii/S0020025514008561

File Usage : rscript smoteipf.r <input.csv> <output.csv>

## SPIDER2
Input file should contain Yes/No Class and header. The header of Yes/No Column should be named 'Class'. Entries in Yes/No Column should be either 'Y' or 'N'. Input File should be in csv format.

Change k in KNN changing the variable 'k' in spider.py . Change 'YNcolumn' variable to indicate column number of Yes/No Column. Column numbers start  from 1.

Other variables can be changed below the comment "#change below parameters according to requirment". For info on these variables visit : https://link.springer.com/chapter/10.1007/978-3-642-13529-3_18

File Usage : python3 spider.py <input.csv>

Output : k-r-a0.csv, k-r-a1.csv, k-r-a2.csv where a0, a1 and a2 represent no aplification, weak amplification and strong amplification respectively.


#### A sample file named 'sample.csv' is uploaded for reference. 
