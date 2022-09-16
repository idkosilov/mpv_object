from PySide6.QtCore import QObject
from PySide6.QtQuick import QQuickFramebufferObject

from mpv_renderer import MpvRenderer


class MpvPlayer(QQuickFramebufferObject):

    def __init__(self, mpv_instance, parent: QObject = None):
        super().__init__(parent)
        self._mpv_instance = mpv_instance
        self._renderer = None

    def createRenderer(self) -> 'QQuickFramebufferObject.Renderer':
        self._renderer = MpvRenderer(self)
        return self._renderer
