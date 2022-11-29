from typing import Optional, List
from PyQt6.QtCore import QAbstractListModel, QObject, QModelIndex, QVariant, Qt

from models.room import Room


class RoomListModel(QAbstractListModel):

    room_list: List[Room]

    def __init__(self,
                 room_list: List[Room],
                 parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        self.room_list = room_list

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.room_list)

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self.room_list):
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            return QVariant(
                "{0.number} - p {0.num_of_people}, d {0.duty_days_left}".
                format(self.room_list[index.row()]))

        return QVariant()