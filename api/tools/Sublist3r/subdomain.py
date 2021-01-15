#!/usr/bin/python3

import sys
import sublist3r
import os
def getsubdomines(domine):
    subdomains = sublist3r.main(domine, 40, "temp2.txt", ports= None, silent=False, verbose= True, enable_bruteforce= False, engines=None)
    return subdomains

print(sys.argv[1])
subdomains = getsubdomines(str(sys.argv[1]))
