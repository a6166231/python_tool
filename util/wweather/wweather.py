#coding=utf-8
import json,os,wutil
import wpop.pop
os.chdir(os.path.dirname(os.path.abspath(__file__)))

f = open('./conf.json','r')
conf = json.loads(f.read())
f.close()

if not conf['isListener']:
    print("un listener")
    os.system("pause")
    exit()

f = open('./country.json', 'r')
country = json.loads(f.read())
f.close()

def getWeatherByCity(city):
    id = country[city]
    info = wutil.getWeather(id, 2)
    rainStr = u'有雨' if u'雨' in info else u''
    snowStr = u'有雪' if u'雪' in info else u''
    info = city + ' ' + '\n' + info
    if rainStr == u'有雨' or snowStr == u'有雪':
        city += ' ' + rainStr + ' ' + snowStr
        return {
            "title": city,
            "message": info,
        }
    return {
        "title": "",
        "message": "",
    }

LINE = " \n ---------------------------------------------\n"
for obj in conf["citys"]:
    warning = {
        "title": "",
        "message": "",
    }
    for cityname in obj["name"]:
        cityinfo = getWeatherByCity(cityname)
        if len(cityinfo["title"]) != 0:
            warning["title"] += cityinfo["title"] + "; "
            warning["message"] += cityinfo["message"] + LINE
    
    if(len(warning["title"]) != 0):
        wpop.pop.popEmail(warning["message"],warning["title"],tar = obj['email'])
        print(warning["title"])
        print(warning["message"])   