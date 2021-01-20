import os,sys

#os.system("amass enum -passive -d "+str(sys.argv[1])+" -o temp1.txt")
#os.system("python3 tools/Sublist3r/subdomain.py "+str(sys.argv[1]))
os.system("python3 tools/OneForAll/oneforall.py --target "+str(sys.argv[1])+" --fmt csv run")
#os.system("cat tools/OneForAll/results/"+str(sys.argv[1])+".csv") # | jq '.[].subdomain' | sed 's/\"//g' | sort -u > temp3.txt")

filenames = ['temp1.txt', 'temp2.txt', 'temp3.txt']
'''
try:
    with open('temp4.txt', 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                outfile.write(infile.read())
            outfile.write("\n")
    os.remove("temp1.txt")
    os.remove("temp2.txt")
    os.remove("temp3.txt")

    lines_seen = set() # holds lines already seen
    with open(str(sys.argv[1])+".txt", "w") as output_file:
    	for each_line in open("temp4.txt", "r"):
    	    if each_line not in lines_seen: # check if line is not duplicate
    	        output_file.write(each_line)
    	        lines_seen.add(each_line)
    os.remove("temp4.txt")
except:
    print('failed amass')
    os.rename('temp2.txt',str(sys.argv[1])+".txt")
'''
#os.system("python3 tools/livefinder/BirDuster.py -P tools/livefinder/ports.txt -t 10 -i -l "+ str(sys.argv[1])+".txt "+str(sys.argv[1]))
os.system("mkdir ../static/output/"+str(sys.argv[2]))
os.system("mv tools/OneForAll/results/"+str(sys.argv[1])+".csv ../static/output/"+str(sys.argv[2])+"/")
#os.system("mv "+str(sys.argv[1])+".txt "+" output/"+str(sys.argv[2])+"/")
#os.system("mv "+str(sys.argv[1])+".csv "+" output/"+str(sys.argv[2])+"/")
#os.system("python3 screenshot.py "+str(sys.argv[1])+" "+str(sys.argv[2]))
