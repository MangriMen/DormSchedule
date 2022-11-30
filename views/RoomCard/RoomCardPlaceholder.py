from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6 import uic


class RoomCardPlaceholder(QWidget):

    def __init__(self,
                 parent: Optional['QWidget'] = None,
                 flags: Qt.WindowType = Qt.WindowType.Widget) -> None:
        super().__init__(parent, flags)
        self.ui = uic.loadUi(  # type: ignore
            'views/RoomCard/RoomCardPlaceholder.ui', self)
