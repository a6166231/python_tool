import sys
import wmi,sys
try :
    light = sys.argv[1]
except:
    light = 100
c = wmi.WMI(namespace='root/WMI')
a = c.WmiMonitorBrightnessMethods()[0]
a.WmiSetBrightness(light,100)