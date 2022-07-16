#coding=utf-8

class Email:
    def __init__(self, host, username, userpwd):
        """ -初始化邮件信息-
            传进的参数长度都不能为0
        """
        if len(host) == 0 or len(username) == 0 or len(userpwd) == 0:
            print('some parames length is 0')
            return False
        self.host = host
        self.username = username
        self.userpwd = userpwd
    
    def sendEmail(self, smessage = 'message', sfrom = 'from',title = 'title', tarMail = []):
        """ 发送邮件  
            smessage: 邮件内容
            sfrom: 发送人名字
            title: 邮件标题
        """
        if len(tarMail) == 0:
            print('tarMail length is 0')
            return False
        import smtplib
        from email.mime.text import MIMEText
        omessage = MIMEText(smessage,'plain','utf-8')
        omessage['Subject'] = title
        omessage['From'] = sfrom
        omessage['To'] = ','.join(tarMail)
        try:
            smtpObj = smtplib.SMTP() 
            smtpObj.connect(self.host,25)
            smtpObj.login(self.username,self.userpwd) 
            smtpObj.sendmail(self.username, tarMail, omessage.as_string()) 
            smtpObj.quit() 
            print('success')
            return True
        except smtplib.SMTPException as e:
            print('error',e)
            return False

def playSound(url):
    """
        播放音效 仅wav格式
    """
    import pyaudio, wave
    def play(url):
        chunk = 1024
        wf = wave.open(url, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
        data = wf.readframes(chunk)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
    play(url)

def daysCeilAsNow(year, mouth, day):
    """ 目标日期和当前时间的天数差 """
    import datetime
    now = datetime.datetime.today()
    tar = datetime.datetime(year,mouth,day)
    return abs(now-tar).days

def daysCeil(year, mouth, day, year2, mouth2, day2):
    """ 指定2个日期的天数差 """
    import datetime
    now = datetime.datetime(year,mouth,day)
    tar = datetime.datetime(year2,mouth2,day2)
    return abs(now-tar).days

def getWeather(cityCode,days): 
    import requests
    from bs4 import BeautifulSoup 
    url = 'http://www.weather.com.cn/weather/%s.shtml' % str(cityCode) 
    html = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'} ) 
    html.encoding = 'utf-8' 
    soup=BeautifulSoup(html.text,'html.parser')
    weather = u''
    count = 0
    ssd = u'℃'
    for item in soup.find("div", {'id': '7d'}).find('ul').find_all('li'): 
        if count >= days:
            break
        count += 1
        date, detail = item.find('h1').string, item.find_all('p') 
        title = detail[0].string 
        templow = detail[1].find("i").string 
        span = detail[1].find('span')
        temphigh = ''
       
        wind,direction = detail[2].find('span')['title'], detail[2].find('i').string 
        templow = templow[0:templow.index(ssd)]
        if span:
            temphigh = '~' + span.string
        else:
            templow += ssd
        info = "%-8s\t%-15s\t%s%s%s\t\t%-8s\t%-8s\n" % (date,title,templow,temphigh,'',wind,direction)
        weather += info
    return weather

def copyDir(start, end, mt = 128, std = False):
    import os
    print(start,' - ', end)
    stdStr = "" if std else ">nul"
    cmd = 'ROBOCOPY ' + start + ' ' + end + " /E /MT:"+ str(mt) + " " + stdStr
    os.system(cmd)

def updateViewLight(light = 100):
    import os
    os.system('updateLight 100')