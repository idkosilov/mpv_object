import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    QQuickWindow.setGraphicsApi(QSGRendererInterface.OpenGL)

    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).parent / "main.qml"
    engine.load('main.qml')

    sys.exit(app.exec())
