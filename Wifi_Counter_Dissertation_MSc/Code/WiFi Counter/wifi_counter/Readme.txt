For the wifi counter to work the following packages must be installed on the Arduino IDE:

	ESP8266 Community 2.5.2
		- packages inside - 
			ESP8266Wifi
			MD5
			WiFiUdp
			stdio
			SPI
			SD
	NTPClient 3.1.0

Adruino Board: NodeMCU 1.0 (ESP-12E Module)
Upload Speed : 115200

To run upload code to ESP8266 microcontroller using the Arduino IDE. See the console to see if the code
has been uploaded correctly or not.

The board set up will be the ESP8266 with the Micro SD card module : 
https://www.amazon.co.uk/kwmobile-Reader-Adapter-Arduino-Microcontrollers/dp/B06XHJTGGC/ref=asc_df_B06XHJTGGC/?tag=googshopuk-21&linkCode=df0&hvadid=310802245808&hvpos=1o1&hvnetw=g&hvrand=16161436127438113121&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1007408&hvtargid=pla-422342020223&psc=1

The connections that will need to be made are :
 Micro SD Card module pins -> ESP8266 pins : 
 VCC -> VV , GND -> G, CS -> D8, MOSI -> D7, SCK -> D5, MOSO -> D6;

Then the filteredMacAddresss.csv must be uploaded to the micro SD card, Formatted in FAT32.
WARNING: make sure the csv file uploaded to the sd card is called 'filteredMacAddresss.csv' 
with MAC address you want to filter in it.