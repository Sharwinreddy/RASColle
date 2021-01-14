#!/usr/bin/env python3
import os
import csv
import sys
import base64
import socket
import random
import argparse
import colorama
import requests
import threading
import concurrent.futures

from builtins import input # compatibility, python2/3
from datetime import datetime
from colorama import Fore, Style
from user_agent import generate_user_agent, generate_navigator


# Default configurations
MAX_WORKERS = 40
DEF_TIMEOUT = 10
DEFAULT_DIR_LIST_FILE = 'dir_list.txt'
FOUND = []



def _print_err(message):
    sys.stderr.write(Fore.RED + "[X]"+Style.RESET_ALL+"\t%s\n" % message)

def _print_succ(message):
    sys.stdout.write(Fore.GREEN + "[+]"+Style.RESET_ALL+"\t%s\n" % message)

def _print_info(message):
    sys.stdout.write(Fore.BLUE + "[+]" + Style.RESET_ALL + "\t%s\n" % message)

def _fetch_url(domain,ports, headers, ssl_verify=True, write_response=False, timeout=DEF_TIMEOUT):
    global FOUND
    socket.setdefaulttimeout = timeout
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    URLs_to_check=[]
    openports=[]
    responsecode=[]
    urls=[]
    screenshotspath=[]
    for port in ports:
        surl="https://%s:%s/" % (domain, port)
        url="http://%s:%s/" % (domain, port)
        try:
            site_request = requests.get(surl, headers=headers, verify=ssl_verify)
            openports.append(port)
            responsecode.append(str(site_request.status_code))
            print(surl)
            urls.append(surl)
            screenshotspath.append('https.'+domain+'.'+port+'..png')
        except:
            try:
                site_request = requests.get(url, headers=headers, verify=ssl_verify)
                openports.append(port)
                responsecode.append(str(site_request.status_code))
                urls.append(url)
                screenshotspath.append('https.'+domain+'.'+port+'..png')
                print(url)
            except:
                pass
    live=""
    if len(openports)!=0:
        FOUND.append([domain,openports,urls,responsecode,'live',screenshotspath])
    else:
        FOUND.append([domain,openports,urls,responsecode,'dead',screenshotspath])
    sys.stdout.flush()

def parse_arguemnts():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="domain or host to buster")
    parser.add_argument("-v", "--verbosity", action="count", default=0, help="Increase output verbosity")
    parser.add_argument("-p", "--port", help="Which port?", type=int)
    parser.add_argument("-P", "--pfile", help="Port file to iterate")
    parser.add_argument("-t", "--threads", type=int, help="Concurrent threads to run [15]", default=MAX_WORKERS)
    parser.add_argument("-o", "--output", help="Output file to write to")
    parser.add_argument("-l", "--dlist", help="Directory list file")
    parser.add_argument("-w", "--writeresponse", help="Write response to file", action="store_true", default=False)
    parser.add_argument("-i", "--ignorecertificate", help="Ignore certificate errors", action="store_true", default=False)
    parser.add_argument("-u", "--useragent", help="User agent to use.", default=generate_user_agent())
    parser.add_argument("--ssl", help="Should i use SSL?", action="store_true")
    parser.add_argument('--timeout', help="Socket timeout [3]", default=3, type=int)
    args = parser.parse_args()
    if args.port and args.pfile:
        _print_err("Can't have both port file [pfile] and port [port] specified.")
        _print_err("Kindly choose one.")
        exit()
    if args.dlist:
        if not os.path.exists(args.dlist):
            _print_err("Can't find file '%s'." % args.dlist)
            exit()
    if args.pfile:
        if not os.path.exists(args.pfile):
            _print_err("Can't find file '%s'." % args.pfile)
            exit()
    if args.ignorecertificate and not args.ssl:
        _print_info("Since ignore-certificate flag is on but SSL is not, will attempt SSL connection.")
    if not args.output:
        args.output = "%s.csv" % args.domain
    if args.verbosity:
        _print_info("Will write output to %s." % args.output)
    if args.verbosity and not args.useragent:
        _print_info("No user-agent was supplied so using '%s'." % args.useragent)

    if os.path.exists(args.output):
        i = input(Fore.RED + "[!]"+Style.RESET_ALL+"\tOutput file exists. Should i overwrite it?[no]:") or False
        if i == False:
            args.output = "%s_%s.csv" % (args.domain, random.randint(111,999))
            _print_info("Set output file to be '%s'." % args.output)
        else:
            _print_info("Original file will be overwritten.")
    return args

def main():
    args = parse_arguemnts()

    # Read relevant files
    # Parse ports file.
    if args.pfile:
        ports = []
        ports_raw = open(args.pfile, 'r').readlines()
        for port in ports_raw:
            try:
                if len(port) != 0:
                    ports.append(str(port.strip()))
                else:
                    # Probably empty line.
                    pass
            except:
                _print_err("Error parsing ports file. One of the lines in not an integer.")
                exit()
    elif args.port:
        ports = [args.port]
    elif args.ssl:
        ports = [443]
    else:
        ports = [80]
    # Parse Directory file
    dirs = []
    if args.dlist:
        dirs_raw = open(args.dlist, 'r').readlines()
        for i in dirs_raw:
            thisDir = i.strip()
            if len(thisDir) == 0:
                continue
            dirs.append(thisDir)
    else:
        dirs_raw = open(DEFAULT_DIR_LIST_FILE, 'r').readlines()
        for i in dirs_raw:
            thisDir = i.strip()
            if len(thisDir) == 0:
                continue
            dirs.append(thisDir)

    # Make output directory incase of writing
    if args.writeresponse:
        try:
            os.mkdir(args.domain)
        except:
            # Directory exists
            pass

    # Start threading
    headers = {'User-Agent': args.useragent}
    thread_local = threading.local()

    _print_info("Execution starting with %s threads..." % args.threads)

    thread_args = []
    for domain in dirs:
        thread_args.append((domain,ports,headers,args.ignorecertificate,args.writeresponse, args.timeout))

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(_fetch_url, *zip(*thread_args))


    # Write output to file
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['Domain', 'Ports','Urls','Response','Status','Screenshots']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print(FOUND)
        writer.writeheader()
        for item in FOUND:
            tports=""
            turls=""
            tresponsecode=""
            tspath=""
            for i in item[1]:
                tports=tports+"\n"+str(i)
            for i in item[2]:
                turls=turls+"\n"+str(i)
            for i in item[3]:
                tresponsecode=tresponsecode+"\n"+str(i)
            for i in tspath:
                tspath=tspath+","+str(i)
            thisItem = {'Domain': item[0], 'Ports':tports,'Urls':turls,'Response':tresponsecode,'Status':item[4],'Screenshots':tspath}
            writer.writerow(thisItem)

    _print_succ("Wrote all items to file '%s'." % args.output)

    exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        _print_err("Got keyboard interrupt. Byebye now.")
        exit()
