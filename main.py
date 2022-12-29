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
from Watergate_KML_Transcribe import Get_Watergate_Status
Watergate_deviceID = "Watergate_Status"
global _edgeAgent

def on_connected(edgeAgent, isConnected):
    print("connected !")

def on_disconnected(edgeAgent, isDisconnected):
    print("disconnected !")

def __sendData():
    _edgeAgent.sendData(__generateData())

def __generateConfig():
      config = EdgeConfig()
      nodeConfig = NodeConfig(nodeType = constant.EdgeType['Gateway'])
      config.node = nodeConfig
      deviceConfig = DeviceConfig(id = Watergate_deviceID,
        name = 'Watergate_Status',
        description = 'Watergate',
        deviceType = 'Watergate__Status_Receiver',
        retentionPolicyName = '')
      for j in range(1, 8):
        analog = AnalogTagConfig(name = 'Watergate' + str(j),
          description = "Watergate_Status",
          readOnly = False,
          arraySize = 0,
          spanHigh = 1000,
          spanLow = 0,
          engineerUnit = '',
          integerDisplayFormat = 4,
          fractionDisplayFormat = 2)
        deviceConfig.analogTagList.append(analog)
      config.node.deviceList.append(deviceConfig)
      return config
# Gate 1 close = 500, open = 200, Gate 2 close =500, open = 800
def __generateData():
    edgeData = EdgeData()
    Watergate_Status_Dict = Get_Watergate_Status()
    # Generate Random Data
    for k in Watergate_Status_Dict:
        Watergate_Status_Dict[k] = 200 if (random.randint(0, 1)) else 500
    print(Watergate_Status_Dict)
    deviceId = Watergate_deviceID #需對應剛剛取名的Device
    tagName = 'Watergate1' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡1,桂林"))
    edgeData.tagList.append(tag)
    tagName = 'Watergate2' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, 800 if (Watergate_Status_Dict.get("淡2,貴陽")) == 200 else 500)
    edgeData.tagList.append(tag)
    # tagName = 'Watergate3' #需對應剛剛取名的Tag
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡3,延平"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate4' #需對應剛剛取名的Tag
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡4,玉泉"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate5' #需對應剛剛取名的Tag
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡5,大稻埕"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate6' #需對應剛剛取名的Tag
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡5-1,國順"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate7' #需對應剛剛取名的Tag
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("淡6,敦煌"))
    edgeData.tagList.append(tag)
    tagName = 'waterLevel1'
    randvalue = random.randint(0, 150)
    tag =  EdgeTag(deviceId, tagName, randvalue)
    edgeData.tagList.append(tag)
    tagName = 'waterLevel2'
    tag =  EdgeTag(deviceId, tagName, randvalue if next((x for x in edgeData.tagList if (x.value == 200) or x.value == 800), False)else 0)
    edgeData.tagList.append(tag)
    edgeData.timestamp = datetime.datetime.now()
    return edgeData
    

def Auth():
    options = EdgeAgentOptions(
    nodeId = '7dfea751-49ee-48a3-8adf-30e5f800366b',
    type = constant.EdgeType['Gateway'],                    # 節點類型 (Gateway, Device), 預設是 Gateway
    deviceId = Watergate_deviceID,                                  # 若 type 為 Device, 則必填
    heartbeat = 60,                                         # 預設是 60 seconds
    dataRecover = True,                                     # 是否需要斷點續傳, 預設為 true
    connectType = constant.ConnectType['DCCS'],             # 連線類型 (DCCS, MQTT), 預設是 DCCS
    DCCS = DCCSOptions(
    apiUrl = 'https://api-dccs-ensaas.education.wise-paas.com/',
    credentialKey = '79af9b4ffd45d3dd1353438f336f87ei'
    )
)
    return options
    
           
if __name__ == '__main__':    
    
    _edgeAgent = EdgeAgent( options = Auth() );
    _edgeAgent.on_connected = on_connected
    _edgeAgent.on_disconnected = on_disconnected
    _edgeAgent.connect()
    time.sleep(2)

    # _edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = __generateConfig())
    while True:
        __sendData()
        time.sleep(5)
    _edgeAgent.disconnect()
    _edgeAgent1.disconnect()