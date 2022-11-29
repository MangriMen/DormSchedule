from datetime import date
from typing import List, Optional, Tuple
from PyQt6.QtCore import QAbstractTableModel, QObject, QModelIndex, QVariant, Qt


class ScheduleTableModel(QAbstractTableModel):

    __schedule_table: List[Tuple[date, int]]

    def __init__(self,
                 schedule_table: List[Tuple[date, int]],
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        self.__schedule_table = schedule_table

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.__schedule_table)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.__schedule_table[0]) if self.rowCount() > 0 else 0

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.__schedule_table):
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            column = index.column()

            return QVariant(str(self.__schedule_table[row][column]))

        return QVariant()