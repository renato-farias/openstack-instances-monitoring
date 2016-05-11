#!/bin/bash

export COLUMNS=512

IFS='
'

MONITORING_SERVICE_IP="http://SERVER_IP:8000"

instance_ps='qemu-system'

PSS=$(top -c -b -p $(pgrep ${instance_ps} -d ',') -n 1 |grep ${instance_ps})

hv_mem=$(free -k |sed -n '2p' |awk '{print $2}')
hv_cpu=$(cat /proc/cpuinfo |grep processor |wc -l)

for i in ${PSS}; do
  IFS=' '
  read cpu mem instance <<<$(echo ${i}| awk '{match($0,"instance-[0-9a-zA-Z]{8}",a)}END{print $9, $10, a[0]}')
  instance_mem=$(virsh dommemstat ${instance} |awk '{if ($1=="actual") {print $2}}')
  total_mem=$(echo "scale=4;(((${hv_mem}/100)*${mem})/${instance_mem})*100"|bc)
  total_cpu=$(echo "scale=4;(${cpu}/(100*${hv_cpu}))*100"|bc)
  instance_id=$(virsh dominfo ${instance} |awk '{if ($1=="UUID:") {print $2}}')
  curl --silent -d "instance_id=${instance_id}&cpu=${total_cpu}&mem=${total_mem}" "${MONITORING_SERVICE_IP}/monitoring/post"
done
