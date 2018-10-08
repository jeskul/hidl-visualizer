#!/usr/bin/env python3
import re

foundPidTable = False
pidToName = {}

# The input file containing the output from a 'lshal' and a 'ps -ef' will be read twice.
# to keep the parseing of the two sections independent.

#
# Step 1. Read and parse the process ids and corresponding process names from 'ps -ef'
#
with open('lshal.txt') as file_object:
    for line in file_object:
        line = line.rstrip()
        matchPidHead = re.match(r'UID *PID .*CMD', line)
        if matchPidHead:
            foundPidTable = True
        else:
            matchPidLine = re.match(r'\w+ +(\d+) +.* \d\d:\d\d:\d\d (.+)\W*', line)
            if matchPidLine and foundPidTable:
                pidName = matchPidLine.group(2).split(" ")[0]
                if pidName == 'hwservicemanager':
                    hwservicemanagerPid = matchPidLine.group(1)
                pidToName[matchPidLine.group(1)] = pidName
            else:
                foundPidTable = False

#
# Step 2. Read interfaces and server + client process ids from 'lshal'
#
HIDLTable = []
foundHIDLTable = 0
with open('lshal.txt') as file_object:
    for line in file_object:
        line = line.rstrip()
        # It might seem/be unnecessary two match two different lines (the 'header' of the relevant part) here
        # but it will be done anyway...
        matchHIDLHead = re.match(r'All binderized services \(registered services through hwservicemanager\)', line)
        matchHIDLHead2 = re.match(r'. Interface +Thread Use Server Clients', line)
        if matchHIDLHead:
            foundHIDLTable = 1
        elif foundHIDLTable == 1 and matchHIDLHead2:
            foundHIDLTable = 2
        else:
            matchHIDLLine = re.match(r'. (.+)::(\w+/\w+) +./. {8}(\d+|N/A) *(.*)', line)
            if matchHIDLLine and foundHIDLTable == 2:
                if matchHIDLLine.group(3) != 'N/A':
                    HIDLTable.append((matchHIDLLine.group(1), matchHIDLLine.group(2), matchHIDLLine.group(3), matchHIDLLine.group(4)))
            else:
                foundHIDLTable = 0

#
# Generating the the output
#

print("digraph hidl {")
print("    graph [rankdir = \"LR\"];")
print("    node [shape=box];")

for HIDLInterface in HIDLTable:
    if True:
        _interface = HIDLInterface[0]
        _server = pidToName.get(str(HIDLInterface[2]))
        clients = HIDLInterface[3:][0].split(" ")
        if clients.count(hwservicemanagerPid) > 0:
            clients.remove(hwservicemanagerPid)
            if len(clients) == 0:
                print("    \"" + _server + "\" -> \"" + _server + "\" [label=\"" + _interface + "\n" + HIDLInterface[1] + "\"];")
            else:
                for client in clients:
                    _client = pidToName.get(str(client))
                    print("    \"" + _client + "\" -> \"" + _server + "\" [label=\"" + _interface + "\"];")
            
print("}")