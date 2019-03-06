#!/bin/bash
stop-dfs.sh

#restore the configuration file
cp -R /home/zuoru/hadoop-3.1.1/etc/hadoop/* /home/zuoru/hadoop-etc
rm -r /home/zuoru/hadoop-3.1.1
cp -a /home/zuoru/hadoop-3.1.1-src/hadoop-dist/target/hadoop-3.1.1 /home/zuoru
cp -R /home/zuoru/hadoop-etc/* /home/zuoru/hadoop-3.1.1/etc/hadoop
cd /home/zuoru/hadoop-3.1.1/etc/hadoop; rm -rf testFile

#distribute
for i in 2 3 4 5 6 7 8 9 11 12 13 14 15 16 17 18 19 20 21
do
  rsync -av -e ssh ~/hadoop-3.1.1 jhli@node$i:~/
done 

#clear the log
for i in 2 3 4 5 6 7 8 9 11 12 13 14 15 16 17 18 19 20 21
do 
  ssh jhli@node$i "rm -rf ~/hadoop-3.1.1/logs"
done
