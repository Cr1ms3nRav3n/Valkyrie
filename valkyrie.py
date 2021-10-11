#!/usr/bin/env python3
#rDNS sweeps and initial enumeration for internal penetration tests
#author: Cr1ms3nRav3n
#version: 1.0

import sys
import subprocess
import getopt
from termcolor import colored
from subprocess import call

b= open ('valk.txt', 'r')
print(colored(''.join([line for line in b]),'blue')) 

print (colored('Starting rDNS sweeps, this could take a while...','blue'))
process = subprocess.Popen(['nmap', '-sL', '-R', '192.168.0.0/16'],  stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    
    output = process.stdout.readline()
    with open('output/rdns.txt', 'a') as f:
      print(output.strip(),file=f)
      # Do something else
      return_code = process.poll()
      if return_code is not None:
        # Process has finished, read rest of the output 
        for output in process.stdout.readlines():
            print(output.strip(),file=f)
        break

print()
print(colored('rDNS sweeps done!', 'blue'))
print()
print(colored('Grepping output for live hosts...', 'blue'))

call("scripts/grep.sh")

print()
print(colored('Creating list of subnets to sweep...', 'blue'))

call("scripts/subnet.sh")

print()
print(colored('Sweeping enumerated subnets...', 'blue'))

call("scripts/pingsweep.sh")

print()
print(colored('Running first round nmap scans, hold on to your coffee...', 'blue'))

call("scripts/nmap.sh")

print()
print(colored('Enumerating HTTP, HTTPS and SMB from initial nmap scans...','blue'))

call("scripts/lhf.sh")

print()
print(colored('Checking SMB hosts for signing policy...', 'blue'))

call("scripts/smb.sh")
