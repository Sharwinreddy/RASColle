import os,sys
import csv

projectnumber=str(sys.argv[2])
projectpath='../static/output/'+projectnumber+"/"
csvpath=projectpath+str(sys.argv[1])+".csv"
data=[]
with open(csvpath, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
count=0
with open(str(sys.argv[1])+'_urls.txt', "w") as myfile:
    for d in data:
        count=count+1
        if d[1]=='1':
            t=d[4]+":"+d[11]
            myfile.write("%s\n" % t)
os.system('mv '+str(sys.argv[1])+'_urls.txt '+projectpath)
os.system('nuclei -l '+projectpath+str(sys.argv[1])+'_urls.txt '+'-t templates/cves/ -t templates/misconfiguration/  -t templates/default-logins/  -t templates/exposed-panels/ -t templates/exposures/ -t templates/vulnerabilities/  -stats -json -include-rr  > nuclie.txt')
os.system('mv nuclie.txt '+projectpath)
