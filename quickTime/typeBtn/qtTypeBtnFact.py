
from typeBtn.qtMonthDayTypeBtn import QTMonthDayTypeBtn
from typeBtn.qtRelativeTimeTypeBtn import QTRelativeTimeTypeBtn
from typeBtn.qtTimeTypeBtn import QTTimeTypeBtn
from typeBtn.qtWeekDayTypeBtn import QTWeekDayTypeBtn
from typeBtn.qtTypeBtnBase import QTTypeBtnBase

def createQTTypeBtnByType(_type, parent, editState):
    if (_type == QTRelativeTimeTypeBtn.__name__):
        return QTRelativeTimeTypeBtn(parent, editState)
    elif (_type == QTTimeTypeBtn.__name__):
        return QTTimeTypeBtn(parent, editState)
    elif (_type == QTWeekDayTypeBtn.__name__):
        return QTWeekDayTypeBtn(parent, editState)
    elif (_type == QTMonthDayTypeBtn.__name__):
        return QTMonthDayTypeBtn(parent, editState)
    return QTTypeBtnBase(parent, editState)