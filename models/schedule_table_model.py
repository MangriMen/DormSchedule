from datetime import date
from typing import Any, List, Optional, Tuple
from PyQt6.QtCore import QAbstractTableModel, QObject, QModelIndex, QVariant, Qt


class ScheduleTableModel(QAbstractTableModel):

    __schedule_table: List[Tuple[date, int]]

    def __init__(self,
                 schedule_table: List[Tuple[date, int]],
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        self.__schedule_table = schedule_table

    def setTable(self, schedule_table: List[Tuple[date, int]]):
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

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: int = ...) -> QVariant:
        match orientation:
            case Qt.Orientation.Vertical:
                if not (0 <= section <= len(self.__schedule_table)):
                    return QVariant()

                match role:
                    case Qt.ItemDataRole.DisplayRole:
                        return super().headerData(section, orientation, role)
                    case _:
                        return QVariant()
            case Qt.Orientation.Horizontal:
                if not len(self.__schedule_table) or not (0 <= section <= len(self.__schedule_table[0])):
                    return QVariant()

                match role:
                    case Qt.ItemDataRole.DisplayRole:
                        match section:
                            case 0:
                                return QVariant("Date")
                            case 1:
                                return QVariant("Room")
                    case _:
                        return QVariant()
            case _:
                return QVariant()
        return QVariant()