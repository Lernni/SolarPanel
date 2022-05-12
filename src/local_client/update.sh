#!/bin/bash

RESET=0
START=0

# check option parameters
while getopts rs flag
do
  case "${flag}" in
    r) RESET=1 ;;
    s) START=1 ;;
  esac
done

# shutdown current docker instance
cd ~/SolarPanel/src/
docker-compose down

# update repo if requested
if [ $RESET -eq 1 ]; then
  git reset --hard origin/main
  git fetch
  git pull origin main
fi

# get all other parameters except options
declare -a finalopts
finalopts=()

for o in "$@"; do
  if [[ $o == "-"* ]] ; then
    continue
  fi
  finalopts+=("$o")
done

# rebuild all docker containers or only those that are given as parameters
docker-compose build --build-arg CACHEBUST=$(date +%s) "${finalopts[@]}"

# restart SolarPanel if requested
if [ $START -eq 1 ]; then
  sudo ./local_client/start_solarpanel.sh
fi