#!/bin/bash

for i in {2..13}
do
echo "shutdown node$i"
ssh cloud-node$i "sudo reboot"
done

sudo reboot

