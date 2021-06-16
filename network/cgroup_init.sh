#!/bin/bash
sudo mkdir /sys/fs/cgroup/net_cls/replay
sudo echo 0x100001 > /sys/fs/cgroup/net_cls/replay/net_cls.classid
sudo tc qdisc add dev ens3 root handle 10: htb
sudo tc class add dev ens3 parent 10: classid 10:1 htb rate 10mbit
sudo tc filter add dev ens3 parent 10: protocol ip prio 10 handle 1: cgroup

