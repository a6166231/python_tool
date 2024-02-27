from prefabs.qtPrefabRTime import QTPrefabRTime
from prefabs.qtPrefabWidgetBase import QTPrefabWidgetBase
from timeQuickJump import TimePrefabType

def createQTPrefabByType(type, parent, data):
    if type == TimePrefabType.TIME_ALL.value:
        return QTPrefabWidgetBase(parent, data)
    elif type == TimePrefabType.RELATIVE_TIME.value:
        return QTPrefabRTime(parent, data)
    elif type == TimePrefabType.WEEK_DAY.value:
        return QTPrefabWidgetBase(parent, data)
    elif type == TimePrefabType.MONTH_DAY.value:
        return QTPrefabWidgetBase(parent, data)
    return QTPrefabWidgetBase(parent, data)