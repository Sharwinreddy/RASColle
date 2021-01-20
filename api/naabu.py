import os,sys
import csv

projectnumber=str(sys.argv[2])
projectpath='../static/output/'+projectnumber+"/"
csvpath=projectpath+str(sys.argv[1])+".csv"
data=[]
sdata=[]
with open(csvpath, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
count=0
for d in data:
    count=count+1
    if count==1:
        pass
    else:
        print(d[5])
        sdata.append(d[5])
sdata=list(set(sdata))
with open(str(sys.argv[1])+'.txt', "w") as myfile:
    for d in sdata:
        myfile.write("%s\n" % d)
os.system('mv '+str(sys.argv[1])+'.txt '+projectpath)
os.system('naabu -v -top-ports 100 -iL  '+projectpath+str(sys.argv[1])+'.txt '+' -json > naabu.txt')
os.system('mv naabu.txt '+projectpath)
