# SMA Inverters ModbusTCPIP

**SMA Sunny Tripower is supported,**
Sunny Boy not yet

**Requirements:**
    1. SMA Sunny Tripower:
      * Modbus server TCP enabled,
      * Modbus server UDP enabled.

**Installation:**
cd ~/domoticz/plugins
git clone https://github.com/doopa75/SMA-Inverter-ModbusTCPIP

Then restart domoticz with: ```sudo service domoticz.sh restart```

Succesfully Tested on Domoticz version: 4.10717 (Stable)

**Dependancies**
For this plugin to work you need to install some dependancies

pymodbus AND pymodbusTCP

Install for python 3.x with: sudo pip3 install -U pymodbus pymodbusTCP
