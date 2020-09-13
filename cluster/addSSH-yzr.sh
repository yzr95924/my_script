#!/bin/bash

usage(){
  echo "Usage: ${0} <start> <end>"
}

isNum(){ # Linux version
  re='^[0-9]+$'
  if [[ $1 =~ $re ]]; then
    return 0 
  fi  
  return 1
}

if [[ $# -ne 2 ]]; then
  usage
  exit
elif ! isNum $1; then
  echo "ERROR: $1 is not an integer"
  usage
  exit
elif ! isNum $2; then
  echo "ERROR: $2 is not an integer"
  usage
  exit
elif [[ $1 -gt $2 ]]; then
  echo "ERROR: $1 is larger than $2"
  exit
fi

set -x
for ((i=${1}; i<=${2}; i++))
do
  ssh node${i} mkdir -p ~/.ssh
  cat ~/.ssh/id_rsa.pub | ssh node${i} 'cat >> .ssh/authorized_keys'
  ssh node${i} ls -al 
done
set +x

