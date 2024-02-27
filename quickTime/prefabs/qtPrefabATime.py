from prefabs.qtPrefabWidgetBase import QTPrefabWidgetBase
from timeQuickJump import create_date_time

class QTPrefabATime(QTPrefabWidgetBase):
    def __init__(self, parent, data) -> None:
        super().__init__(parent, data)
        self.leftBtn.pack_forget()
        self.rightBtn.pack_forget()

    def formatData(self):
        vData = self.data['data'].split(' ')
        dateObj = None
        timeObj = None
        if len(vData) == 1:
            typeData = vData[0].split('-')
            if len(typeData) == 1:
                typeData = vData[0].split(':')
                timeObj = {"hour": int(typeData[0]), "minute": int(typeData[1]), "second": int(typeData[2])}
            else:
                dateObj = {"year": int(typeData[0]), "month": int(typeData[1]), "day": int(typeData[2])}
        else:
            _date = vData[0].split('-')
            _time = vData[1].split(':')
            dateObj = {"year": int(_date[0]), "month": int(_date[1]), "day": int(_date[2])}
            timeObj = {"hour": int(_time[0]), "minute": int(_time[1]), "second": int(_time[2])}
        self.date = dateObj
        self.time = timeObj

    def getInfoName(self):
        s = ''
        if self.date:
            s += f'{self.date["year"]}年{self.date["month"]}月{self.date["day"]}日'
        if self.time:
            if self.date:
                s += ' '
            s += f'{self.time["hour"]}时{self.time["minute"]}分{self.time["second"]}秒'
        return s

    def triggerTime(self):
        now = self.getNow()
        year,month,day,hour,minute,second = now.year,now.month,now.day,now.hour,now.minute,now.second
        if self.date:
            year = self.date['year']
            month = self.date['month']
            day = self.date['day']

        if self.time:
            hour = self.time['hour']
            minute = self.time['minute']
            second = self.time['second']

        _tempTime = create_date_time(year,month,day,hour,minute,second)
        self.setTime(_tempTime)


    # def leftTime(self):
    #     now = self.getNow()
    #     now = now + datetime.timedelta(days=-self.day, hours=-self.hour, minutes=-self.minute)
    #     self.setTime(now)

    # def rightTime(self):
    #     now = self.getNow()
    #     now = now + datetime.timedelta(days=self.day, hours=self.hour, minutes=self.minute)
    #     self.setTime(now)