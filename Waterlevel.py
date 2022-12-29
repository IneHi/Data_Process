import requests
import xml.etree.ElementTree as ET

def Get_Waterlevel():
    headers = {"Accept" : "application/xml"}
    Requested_xml = requests.get("https://fhy.wra.gov.tw/WraApi/v1/Water/RealTimeInfo?$top=300", timeout = 5, headers= headers) # ask for water gate KML
    ################################
    # testing data transfer 
    # f = open("shit.kml", mode = "w")
    # f.write(Requested_KML.text)
    #################################
    ns = {'xsd': 'http://www.w3.org/2001/XMLSchema', "xsi": "http://www.w3.org/2001/XMLSchema-instance"}
    if Requested_xml.status_code == requests.codes.ok:
        ####################################
        ##this shit is for laoding local xml file
        tree = ET.parse("/response.xml")
        root = tree.getroot()
        ####################################
        # root = ET.fromstring(Requested_xml.text)
        # print(Requested_xml.text)
        # Shits which works
        # for i in root.find(".//{" + namespaces.get("kml") + "}" + "/Document/Placemark[25]/ExtendedData/Data[1]/value"): #Require: {Namespaces}Tag
        # for i in root.findall("kml:Document", ns):
        #find element through xpath
        Waterlevel_Xpath_Dict = {  
            "台北橋" : ".//{*}ArrayOfWaterRealTimeInfo/{*}WaterRealTimeInfo[1]/{*}WaterLevel[1]"
        }
        # print(root.findall(Waterlevel_Xpath_Dict.get("台北橋")))
        print(Requested_xml.text)
        print(root.findall(Waterlevel_Xpath_Dict.get("台北橋")))
        # for k, v in Waterlevel_Xpath_Dict.items():
        #     for j in root.findall(v, ns):
        #         print(j.text)
        # print(Watergate_Status_Dict)
            
    else:
        print("Error : " + str(Requested_xml.status_code))
    return 0

if __name__ == "__main__":
    Get_Waterlevel()