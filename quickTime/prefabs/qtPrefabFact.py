from prefabs.qtPrefabRTime import QTPrefabRTime
from prefabs.qtPrefabATime import QTPrefabATime

from prefabs.qtPrefabWidgetBase import QTPrefabWidgetBase
from prefabs.qtPrefabMonthTime import QTPrefabMonthTime
from prefabs.qtPrefabWeekTime import QTPrefabWeekTime
from timeQuickJump import TimePrefabType

def createQTPrefabByType(type, parent, data):
    if type == TimePrefabType.TIME_ALL.value:
        return QTPrefabATime(parent, data)
    elif type == TimePrefabType.RELATIVE_TIME.value:
        return QTPrefabRTime(parent, data)
    elif type == TimePrefabType.WEEK_DAY.value:
        return QTPrefabWeekTime(parent, data)
    elif type == TimePrefabType.MONTH_DAY.value:
        return QTPrefabMonthTime(parent, data)
    return QTPrefabWidgetBase(parent, data)