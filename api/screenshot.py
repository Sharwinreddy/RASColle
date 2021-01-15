import os,sys
import csv

projectnumber=str(sys.argv[2])
projectpath='output/'+projectnumber+"/"
csvpath=projectpath+str(sys.argv[1])+".csv"
os.system('mkdir '+projectpath+'temp')
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

os.system('cp -R output/'+str(projectnumber)+" ../static/output/"+str(projectnumber))
