import serial
import re
import time
import urllib,urllib2

ser=serial.Serial("com3",38400)
ser.timeout=1

ser.write("AT+VERSION?\r\n")
tmp=ser.read(22)
print (ser.name)
tmp.replace('','')
tmp.replace('','')
tmp.replace('\0','')
tmp.replace('\n\r','')
print ("ver ",tmp)

ser.write("at+init\r\n")
tmp=ser.read(20)
print ("init...")

ser.write("at+iac=9e8b33\r\n")
tmp=ser.read(20)

ser.write("at+class=0\r\n")
tmp=ser.read(20)

ser.write("at+inqm=0,9,10\r\n")
tmp=ser.read(15)
print ("config...",tmp)

while 1:
    ser.timeout=10
    ser.write("AT+INQ\r\n")
    print ("search...")
    tmp=ser.read(1000)
    print ("list...")
    tmp.strip('\n')
    tmp.strip('\r')
    tmp.strip('\r\n')
    tmp.strip('\n\r')
    print (tmp)

    print ("set...")
    pattern = re.compile("(\+INQ:([A-Z]|\d){4}\W([A-Z]|\d){2}\W([A-Z]|\d){6}\W)|(\+INQ:([A-Z]|\d){2}:([A-Z]|\d){2}:([A-Z]|\d){5})\W") 

    i=0
    for m in pattern.finditer(tmp):
        print (m.group()[5:-1])
        i=i+1
        print (i)
        str=m.group()[5:-1]
        url="http://192.168.43.146:8000/update_device/?address=%s&location=111"%str
        print (url)
        res=urllib2.urlopen(url)
    
    time.sleep(10)
ser.close()