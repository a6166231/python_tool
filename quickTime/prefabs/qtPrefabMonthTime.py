import datetime,calendar
from prefabs.qtPrefabWidgetBase import QTPrefabWidgetBase

class QTPrefabMonthTime(QTPrefabWidgetBase):

    def __init__(self, parent, data) -> None:
        super().__init__(parent, data)

    def formatData(self):
        self.monthDay = int(self.data['data'])

    def getInfoName(self):
        s = '%s号' % self.monthDay
        return s

    def leftTime(self):
        now = self.getNow()

        if self.monthDay < now.day:
            dayCeil = now.day - self.monthDay
        else:
            monthday = calendar.monthrange(now.year, (now.month - 1) if now.month > 1 else 12)[1]
            if(monthday < self.monthDay):
                dayCeil = -now.day
            else:
                dayCeil = monthday - self.monthDay + now.day
        now = now + datetime.timedelta(days=-dayCeil)
        self.setTime(now)

    def rightTime(self):
        now = self.getNow()

        if self.monthDay > now.day:
            dayCeil = self.monthDay - now.day
        else:
            monthday = calendar.monthrange(now.year, now.month)[1]
            monthday2 = calendar.monthrange(now.year, (now.month + 1) if now.month < 11 else 1)[1]

            if(monthday2 < self.monthDay):
                dayCeil = monthday - now.day + monthday2
            else:
                dayCeil = monthday - now.day + self.monthDay

        now = now + datetime.timedelta(days=dayCeil)
        self.setTime(now)

    def triggerTime(self):
        now = self.getNow()

        if self.monthDay == now.day:
            return

        now = now + datetime.timedelta(days=self.monthDay - now.day)
        self.setTime(now)