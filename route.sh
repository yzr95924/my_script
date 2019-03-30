#!/bin/bash
# For Node11:
# rack-3
sudo route add -net 192.168.10.29 netmask 255.255.255.255 gw 192.168.10.30
sudo route add -net 192.168.10.28 netmask 255.255.255.255 gw 192.168.10.30
sudo route add -net 192.168.10.27 netmask 255.255.255.255 gw 192.168.10.30
# rack-2
sudo route add -net 192.168.10.26 netmask 255.255.255.255 gw 192.168.10.30
sudo route add -net 192.168.10.25 netmask 255.255.255.255 gw 192.168.10.30
sudo route add -net 192.168.10.24 netmask 255.255.255.255 gw 192.168.10.30
# rack-1
sudo route add -net 192.168.10.21 netmask 255.255.255.255 gw 192.168.10.30
sudo route add -net 192.168.10.22 netmask 255.255.255.255 gw 192.168.10.30
sudo route add -net 192.168.10.23 netmask 255.255.255.255 gw 192.168.10.30