#!/bin/bash

IPRANGE=$1
START_IP=$2
LAST_IP=$3

not_in_table=()

for ip in `seq $START_IP $LAST_IP`
do
    output=`/usr/bin/vtysh -e "show ip route $IPRANGE.$ip/32" |grep $IPRANGE.$ip`
    status=$?
    if [[ ! $status -eq 0 ]]
    then
        not_in_table+=($IPRANGE.$ip)
    fi
done

array_len=${#not_in_table[@]}

if [[ $array_len -eq 0 ]]
then
    echo "All IPs in table"
    exit 0
else
    echo "${not_in_table[@]} not in table, please check OSPF"
    exit 2
fi
