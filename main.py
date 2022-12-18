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

global _edgeAgent, _edgeAgent1

def on_connected(edgeAgent, isConnected):
    print("connected !")


def on_disconnected(edgeAgent, isDisconnected):
    print("disconnected !")

def __sendData():
    _edgeAgent.sendData(__generateData())
    
def __sendData1():
    _edgeAgent1.sendData(__generateData1())

def __generateData():
    edgeData = EdgeData()

    value=[random.uniform(10,40),random.uniform(0,50),random.uniform(0,100)]  
    
    #Air sensor
    deviceId = 'nJLkBcnjmikE' #需對應剛剛取名的Device
    tagName = 'Humidity' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[2])
    edgeData.tagList.append(tag)
    deviceId = 'nJLkBcnjmikE' #需對應剛剛取名的Device
    tagName = 'PM_2p5'     #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[1])
    edgeData.tagList.append(tag)
    deviceId = 'nJLkBcnjmikE' #需對應剛剛取名的Device
    tagName = 'Temperature' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[0])
    edgeData.tagList.append(tag)
    edgeData.timestamp = datetime.datetime.now()
    
    return edgeData

def __generateData1():

    edgeData = EdgeData()
    value=[random.randrange(10,20,1),random.uniform(30,50),random.randrange(0,2,1),random.uniform(90,100),random.uniform(10,30)]
    #Water_dispenser 
    deviceId = 'XffzJ87qngx3' #需對應剛剛取名的Device
    tagName = 'Cold_temp' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[4] if value[2] else 0)
    edgeData.tagList.append(tag)
    deviceId = 'XffzJ87qngx3' #需對應剛剛取名的Device
    tagName = 'Hot_temp' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[3] if value[2] else 0)
    edgeData.tagList.append(tag)
    deviceId = 'XffzJ87qngx3' #需對應剛剛取名的Device
    tagName = 'Status' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[2])
    edgeData.tagList.append(tag)
    deviceId = 'XffzJ87qngx3' #需對應剛剛取名的Device
    tagName = 'Warm_temp' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[1] if value[2] else 0)
    edgeData.tagList.append(tag)
    deviceId = 'XffzJ87qngx3' #需對應剛剛取名的Device
    tagName = 'Water_level' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[0] if value[2] else 0)
    edgeData.tagList.append(tag)
    edgeData.timestamp = datetime.datetime.now()
    
    return edgeData

def Auth():
    options = EdgeAgentOptions(
    nodeId = '48d1f490-408d-4717-a8b6-1dce79f1ed86',
    type = constant.EdgeType['Gateway'],                    # 節點類型 (Gateway, Device), 預設是 Gateway
    deviceId = 'nJLkBcnjmikE',                                  # 若 type 為 Device, 則必填
    heartbeat = 60,                                         # 預設是 60 seconds
    dataRecover = True,                                     # 是否需要斷點續傳, 預設為 true
    connectType = constant.ConnectType['DCCS'],             # 連線類型 (DCCS, MQTT), 預設是 DCCS
    DCCS = DCCSOptions(
    apiUrl = 'https://api-dccs-ensaas.education.wise-paas.com/',
    credentialKey = '186896822d73b72c00a2b8de0988abyk'
    )
)
    return options
    
def Auth1():
    options = EdgeAgentOptions(
    nodeId = '48d1f490-408d-4717-a8b6-1dce79f1ed86',
    type = constant.EdgeType['Gateway'],                    # 節點類型 (Gateway, Device), 預設是 Gateway
    deviceId = 'XffzJ87qngx3',                                  # 若 type 為 Device, 則必填
    heartbeat = 60,                                         # 預設是 60 seconds
    dataRecover = True,                                     # 是否需要斷點續傳, 預設為 true
    connectType = constant.ConnectType['DCCS'],             # 連線類型 (DCCS, MQTT), 預設是 DCCS
    DCCS = DCCSOptions(
    apiUrl = 'https://api-dccs-ensaas.education.wise-paas.com/',
    credentialKey = '186896822d73b72c00a2b8de0988abyk'
    )
)
    return options
           
if __name__ == '__main__':    
    _edgeAgent = EdgeAgent( options = Auth() );
    _edgeAgent.on_connected = on_connected
    _edgeAgent.on_disconnected = on_disconnected
    _edgeAgent.connect()
    _edgeAgent1 = EdgeAgent( options = Auth1() );
    _edgeAgent1.on_connected = on_connected
    _edgeAgent1.on_disconnected = on_disconnected
    _edgeAgent1.connect()
    time.sleep(2)
    while True:
        __sendData()
        __sendData1()
        time.sleep(2)
    _edgeAgent.disconnect()
    _edgeAgent1.disconnect()