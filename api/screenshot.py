import os,sys
import csv

projectnumber=str(sys.argv[2])
projectpath='../static/output/'+projectnumber+"/"
csvpath=projectpath+str(sys.argv[1])+".csv"
os.system('mkdir '+projectpath+'temp')
os.system('mkdir '+projectpath+'screenshots')
'''
with open(csvpath, newline='') as csvfile:
    data = csv.DictReader(csvfile)
    count=0
    for row in data:
        count=count+1
        os.system('mkdir '+projectpath+str(count))
        os.system('mkdir '+projectpath+str(count)+'/screenshots')
        if row['Status']=='live':
            open(projectpath+'turls.txt', 'w').write(str(row['Urls']))
            os.system('eyewitness --web --timeout 60 -f '+projectpath+'turls.txt -d '+projectpath+'temp'+' --no-prompt')
            os.system('mv -v '+projectpath+'temp/screens/* '+projectpath+str(count)+'/screenshots/')
            os.remove(projectpath+'turls.txt')
'''
data=[]
with open(csvpath, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
count=0
with open(str(sys.argv[1])+'_urls.txt', "w") as myfile:
    for d in data:
        count=count+1
        os.system('mkdir '+projectpath+str(count))
        t=d[4]+":"+d[11]
        myfile.write("%s\n" % t)
os.system('mv '+str(sys.argv[1])+'_urls.txt '+projectpath)
os.system('eyewitness --web --timeout 60 --threads 5 --max-retries 2 -f '+projectpath+str(sys.argv[1])+'_urls.txt -d '+projectpath+'temp'+' --no-prompt')
os.system('mv -v '+projectpath+'temp/screens/* '+projectpath+'screenshots/')
#os.system('cp -R output/'+str(projectnumber)+" ../static/output/"+str(projectnumber))
