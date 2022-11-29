from typing import Any, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6 import uic

from models.room import Room


class RoomCard(QWidget):

    ui: Any

    def __init__(self,
                 parent: Optional['QWidget'] = None,
                 flags: Qt.WindowType = Qt.WindowType.Widget) -> None:
        super().__init__(parent, flags)
        self.ui = uic.loadUi('views/RoomCard.ui', self)  # type: ignore

    def setRoom(self, room: Room) -> None:
        self.ui.roomNumberLabel.setText(str(room.number))
        self.ui.numberOfPeopleSpinBox.setValue(room.num_of_people)
        self.ui.penaltyDutySpinBox.setValue(room.penalty_duty)