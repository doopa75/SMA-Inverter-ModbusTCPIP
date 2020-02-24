# SMA Inverters ModbusTCPIP
Author: doki

**SMA Sunny Tripower is supported,**

Sunny Boy not yet

**Requirements:**

SMA Sunny Tripower:
* Modbus server TCP enabled,
* Modbus server UDP enabled.

https://www.sma-sunny.com/en/how-to-test-the-connection-to-your-sma-inverter/

**Installation:**

cd ~/domoticz/plugins

git clone https://github.com/doopa75/SMA-Inverter-ModbusTCPIP

Then restart domoticz with: ```sudo service domoticz.sh restart```

Succesfully Tested on Domoticz version: 4.10717 (Stable)

**Dependencies**

For this plugin to work you need to install some dependencies

pymodbus AND pymodbusTCP

Install for python 3.x with: ```sudo pip3 install -U pymodbus pymodbusTCP```

**Thanks**

Inspired by MFxMF
