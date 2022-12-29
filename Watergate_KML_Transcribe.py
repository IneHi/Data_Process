import requests
import xml.etree.ElementTree as ET

def Get_Watergate_Status():
    Requested_KML = requests.post("https://www.google.com/maps/d/u/0/kml?mid=1teHTnT-t7raWTPr55wx3u6Ky9T8&lid=xKlKDRMn1R8&forcekml=1", timeout = 5) # ask for water gate KML
    ################################
    # testing data transfer
    # f = open("shit.kml", mode = "w")
    # f.write(Requested_KML.text)
    #################################
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    if Requested_KML.status_code == requests.codes.ok:
        ####################################
        ##this shit is for laoding local xml file
        # tree = ET.parse("watergate.xml")
        # root = tree.getroot()
        ####################################
        root = ET.fromstring(Requested_KML.text)
        #Shits which works
        # for i in root.find(".//{" + namespaces.get("kml") + "}" + "/Document/Placemark[25]/ExtendedData/Data[1]/value"): #Require: {Namespaces}Tag
        # for i in root.findall("kml:Document", ns):
        #find element through xpath
        Watergate_Xpath_Dict = {
            "淡6,敦煌" : ".//kml:Document/kml:Placemark[25]/kml:ExtendedData/kml:Data[1]/kml:value", 
            "淡5-1,國順" : ".//kml:Document/kml:Placemark[10]/kml:ExtendedData/kml:Data[1]/kml:value", 
            "淡5,大稻埕" : ".//kml:Document/kml:Placemark[9]/kml:ExtendedData/kml:Data[1]/kml:value", 
            "淡4,玉泉" :   ".//kml:Document/kml:Placemark[24]/kml:ExtendedData/kml:Data[1]/kml:value", 
            "淡3,延平" :   ".//kml:Document/kml:Placemark[8]/kml:ExtendedData/kml:Data[1]/kml:value", 
            "淡2,貴陽" :   ".//kml:Document/kml:Placemark[7]/kml:ExtendedData/kml:Data[1]/kml:value", 
            "淡1,桂林" :   ".//kml:Document/kml:Placemark[33]/kml:ExtendedData/kml:Data[1]/kml:value"
        }
        Watergate_Status_Dict = {}
        for k, v in Watergate_Xpath_Dict.items():
            for j in root.findall(v, ns):
                Watergate_Status_Dict[k] = 500 if (j.text == "關") else 200 # close = 500, open = 200
        # print(Watergate_Status_Dict)
            
    else:
        print("Error : " + str(Requested_KML.status_code))
    return Watergate_Status_Dict

if __name__ == "__main__":
    Get_Watergate_Status()