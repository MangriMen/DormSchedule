from threading import Thread
import time
from typing import Any, Callable, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6 import uic

from models.room import Room


class RoomCard(QWidget):

    ui: Any
    model: Optional[Room] = None
    update_model: Optional[Callable] = None

    def __init__(self,
                 parent: Optional['QWidget'] = None,
                 flags: Qt.WindowType = Qt.WindowType.Widget) -> None:
        super().__init__(parent, flags)
        self.ui = uic.loadUi(  # type: ignore
            'views/RoomCard/RoomCard.ui', self)

        self.__setEnabledControls(False)

        self.ui.numberOfPeopleSpinBox.valueChanged.connect(
            self.somethingChanged)
        self.ui.penaltyDutySpinBox.valueChanged.connect(self.somethingChanged)

        self.ui.saveButton.clicked.connect(self.saveClicked)
        self.ui.resetButton.clicked.connect(self.resetChages)

    def __setEnabledControls(self, enabled: bool) -> None:
        self.ui.modelWidget.setVisible(enabled)
        self.ui.placeholderWidget.setVisible(not enabled)

        self.ui.saveButton.setEnabled(enabled)
        self.ui.numberOfPeopleSpinBox.setEnabled(enabled)
        self.ui.penaltyDutySpinBox.setEnabled(enabled)

    def setRoom(self, room: Room, commit_room: Callable) -> None:
        self.model = room
        self.update_model = commit_room

        self.model.main_observer = lambda _, *__: self.update()

        self.__setEnabledControls(True)

        self.resetChages()

    def removeRoom(self) -> None:
        self.model = None
        self.update_model = None
        self.__setEnabledControls(False)

    def update(self) -> None:
        if self.model is None:
            return

        if self.update_model is None:
            return

        self.ui.roomNumberLabel.setText(str(self.model.number))
        self.ui.numberOfPeopleSpinBox.setValue(self.model.num_of_people)
        self.ui.penaltyDutySpinBox.setValue(self.model.penalty_duty)

    @pyqtSlot()
    def somethingChanged(self) -> None:
        self.ui.resetButton.setEnabled(True)

    @pyqtSlot()
    def resetChages(self):
        self.update()
        self.ui.resetButton.setEnabled(False)

    @pyqtSlot()
    def saveClicked(self) -> None:
        if self.model is None:
            return

        self.model.num_of_people = self.ui.numberOfPeopleSpinBox.value()
        self.model.penalty_duty = self.ui.penaltyDutySpinBox.value()

        if self.update_model is None:
            return

        self.update_model()

        self.ui.resetButton.setEnabled(False)