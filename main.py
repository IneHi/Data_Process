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
    deviceId = Watergate_deviceID 
    tagName = 'Watergate1' 
    tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("???1,??????"))
    edgeData.tagList.append(tag)
    tagName = 'Watergate1_dash' 
    tag = EdgeTag(deviceId, tagName, 1 if(Watergate_Status_Dict.get("???1,??????")) == 200 else 0)
    edgeData.tagList.append(tag)
    tagName = 'Watergate2' 
    tag = EdgeTag(deviceId, tagName, 800 if (Watergate_Status_Dict.get("???2,??????") == 200) else 500)
    edgeData.tagList.append(tag)
    tagName = 'Watergate2_dash' 
    tag = EdgeTag(deviceId, tagName, 1 if (Watergate_Status_Dict.get("???2,??????") == 200) else 0)
    edgeData.tagList.append(tag)
    # tagName = 'Watergate3' 
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("???3,??????"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate4' 
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("???4,??????"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate5' 
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("???5,?????????"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate6'    
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("???5-1,??????"))
    # edgeData.tagList.append(tag)
    # tagName = 'Watergate7'    
    # tag = EdgeTag(deviceId, tagName, Watergate_Status_Dict.get("???6,??????"))
    # edgeData.tagList.append(tag)
    tagName = "waterLevel_below15"
    randvalue = 1.5 + random.uniform(-0.1, 0.1)
    tag = EdgeTag(deviceId, tagName, randvalue)
    edgeData.tagList.append(tag)
    tagName = 'waterLevel1'
    tag =  EdgeTag(deviceId, tagName, randvalue * 50)
    edgeData.tagList.append(tag)
    tagName = 'waterLevel2'
    tag =  EdgeTag(deviceId, tagName, randvalue* 50 if next((x for x in edgeData.tagList if (x.value == 200) or x.value == 800), False)else 0)
    edgeData.tagList.append(tag)
    tagName = "Line"
    randvalue = 0
    tag = EdgeTag(deviceId, tagName, randvalue)
    edgeData.tagList.append(tag)
    edgeData.timestamp = datetime.datetime.now()
    return edgeData
    

def Auth():
    options = EdgeAgentOptions(
    nodeId = '7dfea751-49ee-48a3-8adf-30e5f800366b',
    type = constant.EdgeType['Gateway'],                    # ???????????? (Gateway, Device), ????????? Gateway
    deviceId = Watergate_deviceID,                                  # ??? type ??? Device, ?????????
    heartbeat = 60,                                         # ????????? 60 seconds
    dataRecover = True,                                     # ????????????????????????, ????????? true
    connectType = constant.ConnectType['DCCS'],             # ???????????? (DCCS, MQTT), ????????? DCCS
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
        time.sleep(30)
    _edgeAgent.disconnect()
