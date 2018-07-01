# weatherscreen
This is a Raspberry Pi Zero W project that use an Inky pHAT's (212x104 pixel) screen to display two temperatures, time and a weather forecast.

The two temperatures are read from a Domoticz service and the weather forecast is fetched from Yr. 

Some minor configuration is needed. 

<b>Temperature sensors</b>
Go to the Setup/Devices page in Domoticz and get the temperature sensor’s “Idx”. Edit the python script’s variables in the upper section.<br/>

<b>Weather forecast</b><br/>
Select the preferable location for weather forecast. Select a location at Yr.no and paste the link into the script, append “/varsel.xml”. This will download the forecast in XML format.

<b>Usage</b></br>
Copy weather to `/etc/init.d`, then make script executable with `sudo chmod +x /etc/init.d/weather`. If you want the script to run at boot then do `sudo update-rc.d weather defaults`.
