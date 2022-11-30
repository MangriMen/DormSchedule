import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator

from views.MainWindow.MainWindow import MainWindow


def init_translator(app):
    translator = QTranslator(app)
    translator.load("translations/qtbase_ru.qm")
    app.installTranslator(translator)


def main() -> None:
    app = QApplication(sys.argv)  # type: ignore

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()