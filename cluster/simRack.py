# usage python simTOR.py
#             1. rack num
#             2. bandwidth (Mb/s)

from random import seed
from random import randint
from random import random
import sys
import subprocess
import time
import threading
import os

RACKNUM=sys.argv[1]
BANDWIDTH=sys.argv[2]

controller=24
cluster=[11,12,13,14]

nic="eth0"
nic23="enp1s0f0"
nic24="enp0s31f6"

#rackid2nodes
rack2nodes={}
node2gw={}

# divide cluster into racks
# namenode is assigned into the first rack
# rack="rack1"
# topo[rack]=[24]

numPerRack=(len(cluster))/int(RACKNUM)

for i in range(int(RACKNUM)):
  gwidx = i * numPerRack
  gwnodeid = cluster[gwidx]
  gwip = "192.168.0."+str(10+gwnodeid)
  racknodes=[]
  for j in range(numPerRack):
    nodeidx=gwidx+j
    nodeid=cluster[nodeidx]
    nodeip="192.168.0."+str(10+nodeid)
    if j==0:
      # this is gw
      racknodes.append(nodeip)
      node2gw[nodeip] = gwip
    else:
      # this is inner node
      racknodes.append(nodeip)
      node2gw[nodeip] = gwip
  rack2nodes[i] = racknodes

print "rack2nodes:"
print rack2nodes
print "node2gw:"
print node2gw

for nodeid in cluster:
  node = "node" + str(nodeid)
  curnic = nic
  if nodeid == 24:
    curnic = nic24
  elif nodeid == 23:
    curnic = nic23
  
  cmd="ssh "+node+" \"sudo tc qdisc del dev "+curnic+" root\""
  print cmd
  os.system(cmd)
  cmd="ssh "+node+" \"sudo tc qdisc add dev "+curnic+" root handle 1: htb default 20\""
  print cmd
  os.system(cmd)
  cmd="ssh "+node+" \"sudo tc class add dev "+curnic+" parent 1: classid 1:1 htb rate "+BANDWIDTH+"mbit ceil "+BANDWIDTH+"mbit burst 10000k\""
  print cmd
  os.system(cmd)


# configure gw on each node
for srcid in cluster:
  srcip = "192.168.0."+str(10+srcid)
  srcgw = node2gw[srcip]
  srcnic = nic
  if srcid == 24:
    srcnic = nic24
  elif srcid == 23:
    srcnic = nic23
  
  if srcip == srcgw:
    print srcip+ " is gateway"
    for dstid in cluster:
      dstip = "192.168.0."+str(10+dstid)
      dstgw = node2gw[dstip]
      if srcgw == dstgw:
        # srcip and dstip are in the same rack, can directly connect to each other
        # traffic via gate to node in the same rack are the traffic whose source is from a different rack
        cmd="ssh "+srcip+" \"sudo tc filter add dev "+srcnic+" protocol ip parent 1: prio 7 u32 match ip dst "+dstip+" flowid 1:1\""
        print cmd
        os.system(cmd)
        continue
      else:
        # all traffic to dstip are first routed to dstgw
        if dstip!= dstgw:
          cmd="ssh "+srcip+" \"sudo route add -net "+dstip+" netmask 255.255.255.255 gw "+dstgw+"\""
          print cmd
          os.system(cmd)
  else:
    print srcip+ " is not gateway"
    for dstid in cluster:
      dstip = "192.168.0."+str(10+dstid)
      dstgw = node2gw[dstip]
      if srcgw == dstgw:
        continue
      else:
        if dstip == dstgw:
          continue
        # all traffic to dstip are first route to srcgw
        cmd="ssh "+srcip+" \"sudo route add -net "+dstip+" netmask 255.255.255.255 gw "+dstgw+"\""
        print cmd
        os.system(cmd)