import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from mpv_player.player import MpvPlayer

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    QQuickWindow.setGraphicsApi(QSGRendererInterface.OpenGLRhi)

    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).parent / "main.qml"
    engine.load('main.qml')

    if not engine.rootObjects():
        del engine
        sys.exit(-1)

    return_code = app.exec()
    del engine
    sys.exit(return_code)
