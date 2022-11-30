from datetime import date
from typing import Any
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QComboBox
from PyQt6.QtCore import pyqtSlot, QItemSelection
from models.room import Room
from models.room_list_model import RoomListModel
from models.schedule_table_model import ScheduleTableModel

from configs.consts import PATH_TO_DB
from models.scheduler import Scheduler


class MainWindow(QMainWindow):

    model: Scheduler = Scheduler()

    scheduleTableModel: ScheduleTableModel
    roomListModel: RoomListModel

    ui: Any

    def __init__(self) -> None:
        super().__init__()
        self.ui = uic.loadUi(  # type: ignore
            'views/MainWindow/MainWindow.ui', self)

        self.roomComboBoxFill()
        self.scheduleTableModel = ScheduleTableModel([])

        # Initialize models
        self.roomListModel = RoomListModel(self.model.conn.query(Room))

        # Setup models
        self.ui.scheduleTableView.setModel(self.scheduleTableModel)
        self.ui.roomListView.setModel(self.roomListModel)

        # Setup signals
        self.ui.generateScheduleButton.clicked.connect(
            self.generateScheduleButtonClicked)

        roomListSelectionModel = self.ui.roomListView.selectionModel()
        roomListSelectionModel.selectionChanged.connect(self.roomSelected)

    def roomComboBoxFill(self):
        rooms = [str(room[0]) for room in self.model.conn.query(Room.number)]
        self.ui.roomComboBox.addItems(rooms)

    @pyqtSlot(QItemSelection, QItemSelection)
    def roomSelected(self, selected: QItemSelection,
                     deselected: QItemSelection):
        if not len(selected.indexes()):
            self.ui.roomCard.removeRoom()
            return

        item = self.roomListModel.rows[selected.indexes()[0].row()]

        self.ui.roomCard.setRoom(item, lambda: self.model.conn.commit())

    @pyqtSlot()
    def generateScheduleButtonClicked(self):
        start_room = int(self.ui.roomComboBox.currentText())
        startDate, endDate = self.ui.startEndDateRange.getRange()

        newSchedule = self.model.makeASchedule(start_room,
                                               startDate.toPyDate(),
                                               endDate.toPyDate())

        self.scheduleTableModel = ScheduleTableModel(newSchedule)
        self.ui.scheduleTableView.setModel(self.scheduleTableModel)
