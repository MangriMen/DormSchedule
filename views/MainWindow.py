from datetime import date
from typing import Any
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSlot, QModelIndex, QItemSelection
from models.room_list_model import RoomListModel
from models.schedule_table_model import ScheduleTableModel

from models.scheduler import Scheduler


class MainWindow(QMainWindow):

    model: Scheduler = Scheduler()

    scheduleTableModel: ScheduleTableModel
    roomListModel: RoomListModel

    ui: Any

    def __init__(self) -> None:
        super().__init__()
        self.ui = uic.loadUi('views/MainWindow.ui', self)  # type: ignore

        self.scheduleTableModel = ScheduleTableModel(
            self.model.makeASchedule(809,
                                     end_date=date(date.today().year,
                                                   date.today().month + 1,
                                                   30)))

        self.roomListModel = RoomListModel(self.model.getRooms())

        self.ui.scheduleTableView.setModel(self.scheduleTableModel)
        self.ui.roomListView.setModel(self.roomListModel)

        roomListSelectionModel = self.ui.roomListView.selectionModel()
        roomListSelectionModel.currentChanged.connect(self.roomSelected)

    @pyqtSlot(QModelIndex, QModelIndex)
    def roomSelected(self, current: QModelIndex, previous: QModelIndex):
        if not (0 < current.row() < len(self.roomListModel.room_list)):
            return

        item = self.roomListModel.room_list[current.row()]

        if item is None:
            return

        self.ui.roomCard.setRoom(item)
