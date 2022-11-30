from typing import Optional, List
from PyQt6.QtCore import QAbstractListModel, QObject, QModelIndex, QVariant, Qt
from PyQt6.QtSql import QSqlQueryModel
from models.room import Room
from sqlalchemy.orm import Query

class RoomListModel(QAbstractListModel):

    query: Query
    rows: List[Room] = []
    count: int = 0

    def __init__(self, query: Query, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.query = query
        self.refresh()

    def refresh(self):
        q = self.query

        self.layoutAboutToBeChanged.emit()

        self.rows = q.all()
        self.count = q.count()

        self.layoutChanged.emit()

        self.query.session.flush()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.count

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        if not index.isValid():
            return QVariant()

        if index.row() >= self.rowCount():
            return QVariant()

        match role:
            case Qt.ItemDataRole.DisplayRole:
                return QVariant("Комната {0.number}: Людей {0.num_of_people}, Дежурств {0.duty_days_left}".format(self.rows[index.row()]))
            case _:
                return QVariant()