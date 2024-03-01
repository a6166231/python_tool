from prefabs.qtPrefabRTime import QTPrefabRTime
from prefabs.qtPrefabATime import QTPrefabATime

from prefabs.qtPrefabWidgetBase import QTPrefabWidgetBase
from prefabs.qtPrefabMonthTime import QTPrefabMonthTime
from prefabs.qtPrefabWeekTime import QTPrefabWeekTime
from timeQuickJump import TimePrefabType

def createQTPrefabByType(qtType, parent, data):
    type = qtType.type
    if type == TimePrefabType.TIME_ALL.value:
        return QTPrefabATime(parent, data, qtType)
    elif type == TimePrefabType.RELATIVE_TIME.value:
        return QTPrefabRTime(parent, data, qtType)
    elif type == TimePrefabType.WEEK_DAY.value:
        return QTPrefabWeekTime(parent, data, qtType)
    elif type == TimePrefabType.MONTH_DAY.value:
        return QTPrefabMonthTime(parent, data, qtType)
    return QTPrefabWidgetBase(parent, data, qtType)