
from typeBtn.qtMonthDayTypeBtn import QTMonthDayTypeBtn
from typeBtn.qtRelativeTimeTypeBtn import QTRelativeTimeTypeBtn
from typeBtn.qtTimeTypeBtn import QTTimeTypeBtn
from typeBtn.qtWeekDayTypeBtn import QTWeekDayTypeBtn
from typeBtn.qtTypeBtnBase import QTTypeBtnBase

def createQTTypeBtnByType(_type, parent, call,  data):
    if (_type == QTRelativeTimeTypeBtn.__name__):
        return QTRelativeTimeTypeBtn(parent, call,  data)
    elif (_type == QTTimeTypeBtn.__name__):
        return QTTimeTypeBtn(parent, call,  data)
    elif (_type == QTWeekDayTypeBtn.__name__):
        return QTWeekDayTypeBtn(parent, call,  data)
    elif (_type == QTMonthDayTypeBtn.__name__):
        return QTMonthDayTypeBtn(parent, call,  data)
    return QTTypeBtnBase(parent, call,  data)