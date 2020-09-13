#!/bin/bash

stop-dfs.sh

echo "clear metadata"
cd ~/dfs/name; rm -rf *
sleep 5s

echo "clear raw data"
for i in 3 4 5 6 7 8 9 11 12 13 14 15 16 17 18 19 20 21
do
  ssh jhli@node$i "cd ~/dfs/data; rm -rf *"
done

echo "start to format NameNode, please check the new report"
sleep 5s
hdfs namenode -format myhdfs

start-dfs.sh

hdfs dfsadmin -report > report

