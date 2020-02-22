#!/usr/bin/env python
"""
Solar inverter SMA Sunny Tripower. The Python plugin for Domoticz
Author: doki
Requirements:
    1. SMA Sunny Tripower with Modbus server TCP and UDP enabled.
    2. Install for python 3.x with: sudo pip3 install -U pymodbus pymodbusTCP

"""
"""
<plugin key="SMA" name="SMA-ModbusTCPIP" version="0.7.3" author="doki">
    <params>
        <param field="Mode2" label="SMA inverter" width="120px" required="true">
            <options>
                <option label="Sunny Tripower" value="tri" default="true"/>
                <option label="Sunny Boy" value="boy"/>
                <option label="other" value="other"/>
            </options>
        </param>
        <param field="Address" label="Your SMA IP_Address" width="200px" required="true" default="192.168.1.45"/>
        <param field="Port" label="Port" width="40px" required="true" default="502"/>
        <param field="Mode1" label="Device ID" width="40px" required="true" default="3" />
        <param field="Mode3" label="Reading Interval min." width="40px" required="true" default="1" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

from pyModbusTCP.client import ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import Domoticz


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        return

    def onStart(self):
        devicecreated = []
        Domoticz.Log("SMA Inverter Modbus plugin start")
        self.runInterval = int(Parameters["Mode3"]) * 1


        if 1 not in Devices:
            Domoticz.Device(Name="Solar Production", Unit=1,Type=0x71,Subtype=0x0,Used=0).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="SMA DC Voltage", Unit=2,TypeName="Voltage",Used=0).Create()
        if 3 not in Devices:
            Domoticz.Device(Name="Active Power AC", Unit=3,TypeName="Usage",Used=0).Create()
        if 4 not in Devices:
            Domoticz.Device(Name="Active Power DC", Unit=4,TypeName="Usage",Used=0).Create()
        if 5 not in Devices:
            Domoticz.Device(Name="DC Current", Unit=5,TypeName="Current (Single)",Used=0).Create()
        if 6 not in Devices:
            Domoticz.Device(Name="Active Power L1", Unit=6,TypeName="Usage",Used=0).Create()
        if 7 not in Devices:
            Domoticz.Device(Name="Active Power L2", Unit=7,TypeName="Usage",Used=0).Create()
        if 8 not in Devices:
            Domoticz.Device(Name="Active Power L3", Unit=8,TypeName="Usage",Used=0).Create()


    def onStop(self):
        Domoticz.Log("SMA Inverter Modbus plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;

        if (self.runInterval <= 0 and Parameters["Mode2"] == "tri"):
            DCVreg = 30771
            # Get data from SMA
            try:
                c = ModbusClient(host=Parameters["Address"], port=Parameters["Port"], unit_id=Parameters["Mode1"], auto_open=True, auto_close=True)
                data = c.read_holding_registers(30529,2)
                dataDCA = c.read_holding_registers(30769,2)
                dataDCV = c.read_holding_registers(DCVreg,2)
                dataDCP = c.read_holding_registers(30773,2)
                dataACP = c.read_holding_registers(30775,2)
                dataACP1 = c.read_holding_registers(30777,2)
                dataACP2 = c.read_holding_registers(30779,2)
                dataACP3 = c.read_holding_registers(30781,2)

            except:
                Domoticz.Log("Connection problem");

            else:
                if Parameters["Mode6"] == 'Debug': Domoticz.Log("DCV Data from SMA" + str(dataDCV))

                decoder = BinaryPayloadDecoder.fromRegisters(data, byteorder=Endian.Big, wordorder=Endian.Big)
                decoderDCA = BinaryPayloadDecoder.fromRegisters(dataDCA, byteorder=Endian.Big, wordorder=Endian.Big)
                decoderDCV = BinaryPayloadDecoder.fromRegisters(dataDCV, byteorder=Endian.Big, wordorder=Endian.Big)
                decoderDCP = BinaryPayloadDecoder.fromRegisters(dataDCP, byteorder=Endian.Big, wordorder=Endian.Big)
                decoderACP = BinaryPayloadDecoder.fromRegisters(dataACP, byteorder=Endian.Big, wordorder=Endian.Big)
                decoderACP1 = BinaryPayloadDecoder.fromRegisters(dataACP1, byteorder=Endian.Big, wordorder=Endian.Big)
                decoderACP2 = BinaryPayloadDecoder.fromRegisters(dataACP2, byteorder=Endian.Big, wordorder=Endian.Big)
                decoderACP3 = BinaryPayloadDecoder.fromRegisters(dataACP3, byteorder=Endian.Big, wordorder=Endian.Big)
                Solar_Production = decoder.decode_32bit_uint()
                DCA = decoderDCA.decode_32bit_uint()
                DCV = decoderDCV.decode_32bit_uint()
                DCP = decoderDCP.decode_32bit_uint()
                ACP = decoderACP.decode_32bit_uint()
                ACP1 = decoderACP1.decode_32bit_uint()
                ACP2 = decoderACP2.decode_32bit_uint()
                ACP3 = decoderACP3.decode_32bit_uint()

                if Parameters["Mode6"] == 'Debug': Domoticz.Log("DCV decode " + str(DCV))

                if (DCV == 2147483648) or (DCA == 2147483648) or (DCP == 2147483648) or (ACP == 2147483648) or (ACP1 == 2147483648) or (ACP2== 2147483648) or (ACP3 == 2147483648):
                    if Parameters["Mode6"] == 'Debug': Domoticz.Log("Fake DC Voltage " + str(DCV))
                    DCV = 0
                    if Parameters["Mode6"] == 'Debug': Domoticz.Log("Only DC Voltage update by zero " + str(DCV))
                    Devices[2].Update(0,str(DCV))

                else:
                    DCV = str(round(DCV / 100, 2))
                    DCA = str(round(DCA / 1000, 2))
                    if Parameters["Mode6"] == 'Debug': Domoticz.Log("Update DC Voltage " + str(DCV))

                    #Update devices
                    if Parameters["Mode6"] == 'Debug': Domoticz.Log("Update AC Power " + str(ACP))
                    Devices[1].Update(0,str(Solar_Production))
                    Devices[2].Update(0,str(DCV))
                    Devices[3].Update(0,str(ACP))
                    Devices[4].Update(0,str(DCP))
                    Devices[5].Update(0,str(DCA))
                    Devices[6].Update(0,str(ACP1))
                    Devices[7].Update(0,str(ACP2))
                    Devices[8].Update(0,str(ACP3))

            self.runInterval = int(Parameters["Mode3"]) * 6

        elif (self.runInterval <= 0 and Parameters["Mode2"] == "boy"):
            Domoticz.Log("Your inverter is SMA Sunny Boy")
            self.runInterval = int(Parameters["Mode3"]) * 6

        elif (self.runInterval <= 0 and Parameters["Mode2"] == "other"):
            Domoticz.Log("Your inverter is SMA Sunny Boy")
            self.runInterval = int(Parameters["Mode3"]) * 6

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
