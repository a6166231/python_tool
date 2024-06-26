import datetime
from prefabs.qtPrefabWidgetBase import QTPrefabWidgetBase

class QTPrefabWeekTime(QTPrefabWidgetBase):
    def formatData(self):
        self.weekDay = int(self.data['data'])

    def getInfoName(self):
        s = '周%s' % self.weekDay
        return s

    def leftTime(self):
        now = self.getNow()
        week = now.isoweekday()

        if self.weekDay < week:
            dayCeil = week - self.weekDay
        else:
            dayCeil = 7 - self.weekDay + week
        now = now + datetime.timedelta(days=-dayCeil)
        self.setTime(now)

    def rightTime(self):
        now = self.getNow()
        week = now.isoweekday()

        if self.weekDay > week:
            dayCeil = self.weekDay - week
        else:
            dayCeil = 7 - week + self.weekDay
        now = now + datetime.timedelta(days=dayCeil)

        self.setTime(now)

    def triggerTime(self):
        now = self.getNow()
        week = now.isoweekday()

        if self.weekDay == week:
            return

        now = now + datetime.timedelta(days=self.weekDay - week)
        self.setTime(now)