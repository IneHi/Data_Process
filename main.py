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
import Watergate_KML_Transcribe

global _edgeAgent

def on_connected(edgeAgent, isConnected):
    print("connected !")

def on_disconnected(edgeAgent, isDisconnected):
    print("disconnected !")

def __sendData():
    _edgeAgent.sendData(__generateData())
    

def __generateData():
    edgeData = EdgeData()
    Watergate_Status_Dict = Get_Watergate_Status()
    deviceId = 'grtpau9R0X8A' #需對應剛剛取名的Device
    tagName = 'Gate_1' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡1,桂林"))
    edgeData.tagList.append(tag)
    tagName = 'Gate_2' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡2,貴陽"))
    edgeData.tagList.append(tag)
    tagName = 'Gate_3' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡3,延平"))
    edgeData.tagList.append(tag)
    tagName = 'Gate_4' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡4,玉泉"))
    edgeData.tagList.append(tag)
    tagName = 'Gate_5' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡5,大稻埕"))
    edgeData.tagList.append(tag)
    tagName = 'Gate_6' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡5-1,國順"))
    edgeData.tagList.append(tag)
    tagName = 'Gate_7' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡6,敦煌"))
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