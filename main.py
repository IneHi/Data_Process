import datetime
import time
import string
import random
import threading
from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer
import requests

global _edgeAgent

def on_connected(edgeAgent, isConnected):
    print("connected !")

def on_disconnected(edgeAgent, isDisconnected):
    print("disconnected !")

def __sendData():
    _edgeAgent.sendData(__generateData())
    

def __generateData():
    edgeData = EdgeData()
    
    deviceId = 'nJLkBcnjmikE' #需對應剛剛取名的Device
    tagName = 'Tag1' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 0)
    edgeData.tagList.append(tag)
    tagName = 'Tag2' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 1)
    edgeData.tagList.append(tag)
    tagName = 'Tag3' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 0)
    edgeData.tagList.append(tag)
    tagName = 'Tag4' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 1)
    edgeData.tagList.append(tag)
    tagName = 'Tag5' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 0)
    edgeData.tagList.append(tag)
    tagName = 'Tag6' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 1)
    edgeData.tagList.append(tag)
    tagName = 'Tag7' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 0)
    edgeData.tagList.append(tag)
    edgeData.timestamp = datetime.datetime.now()
    return edgeData


def Auth():
    options = EdgeAgentOptions(
    nodeId = '704687f9-d796-45ae-af00-98ac55abefe2',
    type = constant.EdgeType['Gateway'],                    # 節點類型 (Gateway, Device), 預設是 Gateway
    deviceId = 'grtpau9R0X8A',                                  # 若 type 為 Device, 則必填
    heartbeat = 60,                                         # 預設是 60 seconds
    dataRecover = True,                                     # 是否需要斷點續傳, 預設為 true
    connectType = constant.ConnectType['DCCS'],             # 連線類型 (DCCS, MQTT), 預設是 DCCS
    DCCS = DCCSOptions(
    apiUrl = 'https://api-dccs-ensaas.education.wise-paas.com/',
    credentialKey = '1b0f6cd4cb5a2d36e7b8a61bb6adffbh'
    )
)
    return options
    
           
if __name__ == '__main__':    
    
    _edgeAgent = EdgeAgent( options = Auth() );
    _edgeAgent.on_connected = on_connected
    _edgeAgent.on_disconnected = on_disconnected
    _edgeAgent.connect()
    time.sleep(2)
    while True:
        __sendData()
        time.sleep(2)
    _edgeAgent.disconnect()
    _edgeAgent1.disconnect()