from datetime import date
from typing import Any, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6 import uic


class DateRange(QWidget):

    ui: Any

    def __init__(self,
                 parent: Optional['QWidget'] = None,
                 flags: Qt.WindowType = Qt.WindowType.Widget) -> None:
        super().__init__(parent, flags)
        self.ui = uic.loadUi(  # type: ignore
            'views/DateRange/DateRange.ui', self)

        self.ui.startDateEdit.setDate(date.today())
        self.ui.endDateEdit.setDate(
            date(date.today().year,
                 date.today().month, 30))

    def getRange(self):
        return (self.ui.startDateEdit.date(), self.ui.endDateEdit.date())
