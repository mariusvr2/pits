import sensor
import urllib2

ozone = sensor.getOzone()
(humidity, pressure, temperature) = sensor.getTemp()
(visible,ir,uv) = sensor.getLight()

print "Humidity is : " + humidity + " %"
print "Pressure is : " + pressure + " mbar"
print "Temperature is : " + temperature + " C"
print "Visible light is : " + visible + " lux"
print "IR light is : " + ir + " lux"
print "UV light is : " + uv + " lux"
print "Ozone concentration is : " + ozone + " ppm"

baseURL = "https://api.thingspeak.com/update?api_key=KA8898GKT8TYZUYQ"
baseURL += "&field1=" + temperature
baseURL += "&field2=" + humidity
baseURL += "&field3=" + pressure
baseURL += "&field4=" + ozone
baseURL += "&field5=" + uv
baseURL += "&field6=" + visible
baseURL += "&field7=" + ir
urllib2.urlopen(baseURL).read()

f=open("/home/pi/sensor/sensor.txt","w+")
f.write(temperature + "," + humidity + "," + pressure + "," + ozone + "," + uv + "," + visible + "," + ir)
f.close()

f=open("/home/pi/sensor/log.txt","a+")
f.write(temperature + "," + humidity + "," + pressure + "," + ozone + "," + uv + "," + visible + "," + ir)
f.close()
