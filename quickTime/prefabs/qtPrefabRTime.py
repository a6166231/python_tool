import datetime
from prefabs.qtPrefabWidgetBase import QTPrefabWidgetBase

class QTPrefabRTime(QTPrefabWidgetBase):

    def __init__(self, parent, data) -> None:
        super().__init__(parent, data)
        self.setBtn.pack_forget()

    def formatData(self):
        vData = self.data['data'].split('-')
        self.day = int(vData[0])
        self.hour = int(vData[1])
        self.minute = int(vData[2])

    def getInfoName(self):
        s = ''
        if self.day != 0:
            s += "%s天" % self.day
        if self.hour != 0:
            s += "%s小时" % self.hour
        if self.minute != 0:
            s += "%s分钟" % self.minute
        return s

    def leftTime(self):
        now = self.getNow()
        now = now + datetime.timedelta(days=-self.day, hours=-self.hour, minutes=-self.minute)
        self.setTime(now)

    def rightTime(self):
        now = self.getNow()
        now = now + datetime.timedelta(days=self.day, hours=self.hour, minutes=self.minute)
        self.setTime(now)