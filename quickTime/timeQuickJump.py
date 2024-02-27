import datetime,win32api
from pytz import timezone
from enum import Enum

class TimePrefabType(Enum):
    NONE = 0,
    #绝对时间
    TIME_ALL = 1
    #相对时间
    RELATIVE_TIME = 2
    #周x
    WEEK_DAY = 2
    #月
    MONTH_DAY = 3

tz = timezone('Asia/Shanghai')

def get_now_time():
    return datetime.datetime.now()

def create_date_time(year, month, day, hour, minute, second):
    _time = datetime.datetime(year, month, day, hour, minute, second)
    # tz.localize(_time)
    return _time

class TimeQuickJumpData:
    def __init__(self, time: datetime.datetime) -> None:
        self.time = time

class TimeQuickJump:
    def __init__(self, type:TimePrefabType, data) -> None:
        self.type = type
        self.data = data
        self.jumpData = TimeQuickJump.formatJumpDataByTimeType(self.type, self.data)

    @staticmethod
    def updateSysTime(time: datetime.datetime):
        time += datetime.timedelta(hours=-8)
        try:
            # 修改系统时间
            win32api.SetSystemTime(time.year,time.month,time.weekday(),time.day,time.hour,time.minute,time.second, 0)
        except: 
            pass

    @staticmethod
    def create(type: TimePrefabType, data):
        return TimeQuickJump(type, data)

    @staticmethod
    def formatJumpDataByTimeType(type: TimePrefabType, data) -> TimeQuickJumpData:
        _datetime = None
        if type == TimePrefabType.TIME_ALL.value:
            _datetime = TimeQuickJump.ABSOLUTE_TIME(type, data)
        elif type == TimePrefabType.RELATIVE_TIME.value:
            _datetime = TimeQuickJump.RELATIVE_TIME(type, data)
        elif type == TimePrefabType.WEEK_DAY.value:
            _datetime = TimeQuickJump.WEEK_DAY(type, data)
        elif type == TimePrefabType.MONTH_DAY.value:
            _datetime = TimeQuickJump.MONTH_DAY(type, data)
        return TimeQuickJumpData(_datetime)  # type: ignore

    @staticmethod
    def ABSOLUTE_TIME(type: TimePrefabType, data: str):
        nowtime = get_now_time()
        times = data.split(' ')
        dateList = times[0].split('-')
        timeList = times[1].split(':')
        if type == TimePrefabType.TIME_ALL:
            return create_date_time(int(dateList[0]),int(dateList[1]),int(dateList[2]),int(timeList[0]),int(timeList[1]),int(timeList[2]))
        # elif type == TimePrefabType.TIME_DATE:
        #     return create_date_time(int(dateList[0]),int(dateList[1]),int(dateList[2]), nowtime.hour, nowtime.minute, nowtime.second)
        # elif type == TimePrefabType.TIME_TIME:
        #     return create_date_time(nowtime.year, nowtime.month, nowtime.day, int(timeList[0]), int(timeList[1]), int(timeList[2]))

    @staticmethod
    def RELATIVE_TIME(type: TimePrefabType, data: int):
        nowtime = get_now_time()
        # if type == TimePrefabType.RELATIVE_TIME_DAY:
        #     return nowtime + datetime.timedelta(days=data)
        # elif type == TimePrefabType.RELATIVE_TIME_HOUR:
        #     return nowtime + datetime.timedelta(hours=data)
        # elif type == TimePrefabType.RELATIVE_TIME_MIN:
        return nowtime + datetime.timedelta(minutes=data)

    @staticmethod
    def WEEK_DAY(type: TimePrefabType, weekDay: int):
        nowtime = get_now_time()
        if type == TimePrefabType.WEEK_DAY.value:
            return nowtime + datetime.timedelta(days=(weekDay - nowtime.weekday()))
        # elif type == TimePrefabType.WEEK_DAY_NEXT:
        #     return nowtime + datetime.timedelta(days=(weekDay - nowtime.weekday() + 7))
        # elif type == TimePrefabType.WEEK_DAY_LAST:
        #     return nowtime + datetime.timedelta(days=(weekDay - nowtime.weekday() - 7))

    @staticmethod
    def MONTH_DAY(type: TimePrefabType, monthDay: int):
        nowtime = get_now_time()
        if type == TimePrefabType.MONTH_DAY:
            return nowtime + datetime.timedelta(days=(monthDay - nowtime.day))
        # elif type == TimePrefabType.MONTH_DAY_NEXT:
        #     return nowtime + datetime.timedelta(days=(monthDay - nowtime.day + 30))
        # elif type == TimePrefabType.MONTH_DAY_LAST:
        #     return nowtime + datetime.timedelta(days=(monthDay - nowtime.day - 30))