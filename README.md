# IoTLevelTempSensor
A project I did for a client where they required a device to measure the level and temperature of a milk vat.

I used a Raspberry Pi Model 3 B+, an industrial 24V hydrostatic pressure sensor, a DS18B20 temperature sensor, an MCP3008 analog to digital converter(with SPI), a 165ohm resistor, 24V DC power supply, a Hologram Nova 3G module, a few jumper cables and a breadboard to build the prototype.

The hydrostatic sensor was connected to the Pi with a few jumper cables, with a 165ohm resistor connected to the negative terminal of the sensor. The resistor was added to change the 4.20ma signal loop to a 3.3v signal in for the MCP3008 (otherwise the Pi would fry).

The DS18B20 was connected directly to the Raspberry Pi with the help of some tutorials.

The device required 3G network capabilities as the client's intention was to distribute the devices to rural farms where WiFi was not available. I decided to use a Hologram Nova for the 3G functionality, mainly due to it's open-source SDK which would save me the hassle of programming AT cellular commands manually.

The python script I wrote starts by connecting the Nova to the cellular network, initializes the DS18B20 sensor, creates a SPI and defines methods for reading the values from each sensor.

I added a loop that reads the values and then using JSON posts the data to a firebase server.

I then scheduled a cron job that would run my script every time the Pi was connected to power, to save the client and their customers from having to interact with the prototype aside from plugging into power.

The script may not reflect the final product that was handed over to the client, as I coded most of it on the Pi locally and forgot to save to my desktop before I handed the prototype over.




