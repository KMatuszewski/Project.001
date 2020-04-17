from datetime import datetime


#	"WW_Isttemperatur" 		=> "8427:0",
#	"Kessel_Vorlaufisttemperatur" 	=> "882b:0,ne", # great part of all messages

#	"Aussentemperatur" 		=> "893c:0,s",
#	"Aussentemperatur_gedaempft" 	=> "893d:0,s",
#	"Versionsnummer_VK" 		=> "893e:0",
#	"Versionsnummer_NK" 		=> "893f:0",
#	"Modulkennung" 			=> "8940:0",
#	"ERR_Letzter_Fehlerstatus" 	=> "aa:0,em",


def MessageDecoding(message):

    DecodingMessage = ""

    KodRozkazu = message[0] + message[1]
    
    if KodRozkazu == '0000':
        DecodingMessage = "000000000000000000000"
    elif KodRozkazu == '8427':
        DecodingMessage = "WW_Isttemperatur = " + int(message[2],16) + " °C"
    elif KodRozkazu == '882B':
        DecodingMessage = "Kessel_Vorlaufisttemperatur = " + int(message[2],16) + " °C"
    elif KodRozkazu == '893C':
        DecodingMessage = "Aussentemperatur = " + int(message[2],16) + " °C"
    elif KodRozkazu == '893D':
        DecodingMessage = "Aussentemperatur_gedaempft" + int(message[2],16) + " °C"



    else:
        DecodingMessage = "????????????????????_" + KodRozkazu + "_"


    

    
    now=datetime.now()
    fileName = "/home/pi/buderus/Buderus_" + now.strftime("%Y%m%d") + ".txt"
    file = open(fileName,"a")
    file.write(now.strftime("%Y.%m.%d %H:%M:%S") + '\n')
    file.write("<------ " + DecodingMessage + '\n')
    file.write("<------ Message ")
    file.write(str(message))
    file.write('\n') 
    file.write('----------------------------------------------------\n')
    file.close()
