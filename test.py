apiIpAndPort="10.0.34.78:3000"
consulIpAndPort="10.0.34.78:8500"
isitdead="DeadMaster"
delaytime=100
mysqlport=61106

#文件路径
templateFile="/etc/consul-template/templates/haproxy.ctmpl"
haproxycfg="/etc/haproxy/haproxy.cfg"
logfile="/var/log/orch_hook.log"

import datetime
nextDate = datetime.datetime.now().strftime("%Y_%m_%d_%H")

print(nextDate)