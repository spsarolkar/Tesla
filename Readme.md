bluetoothctl

power on

pairable on

agent on

default agent

default-agent
scan on
pair <mac address>

trust <mac address>
quit

sudo rfcomm bind rfcomm0 <mac address>

screen /dev/rfcomm0 

atz

atl1

ath1

atsp0

010D --> speed

edit /etc/rc.local

rfcomm bind rfcomm99 <mac address>


vim /etc/systemd/system/dbus-org.bluez.service 

add


