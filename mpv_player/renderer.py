import ctypes
from typing import Callable, Any

from PySide6.QtCore import QSize
from PySide6.QtGui import QOpenGLContext, QOffscreenSurface
from PySide6.QtOpenGL import QOpenGLFramebufferObject
from PySide6.QtQuick import QQuickFramebufferObject
import glfw

from mpv import MpvGlGetProcAddressFn, MpvRenderContext


def get_proc_address_adapter(glfw_get_proc_address: Callable[[str], int]) -> Callable[[Any, bytes], int]:
    def mpv_get_proc_address(_, name: bytes) -> int:
        return glfw_get_proc_address(name.decode('utf-8'))

    return mpv_get_proc_address


class MpvRenderer(QQuickFramebufferObject.Renderer):

    def __init__(self, mpv_player):
        super().__init__()
        self._mpv_player = mpv_player
        self._surface = QOffscreenSurface()
        self._surface.create()
        self._mpv_render_context = None

        if not glfw.init():
            raise 'Cannot initialize OpenGL'

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self._glfw_window = glfw.create_window(1, 1, "", None, None)
        monitor = glfw.get_primary_monitor()
        self.x_scale, self.y_scale = glfw.get_monitor_content_scale(monitor)

        glfw.make_context_current(self._glfw_window)
        self._opengl_context = QOpenGLContext.currentContext()
        self._opengl_context.makeCurrent(self._surface)

        self._proc_address_function = get_proc_address_adapter(glfw.get_proc_address)

    def createFramebufferObject(self, size: QSize) -> QOpenGLFramebufferObject:
        if self._mpv_render_context is None:
            self._mpv_render_context = MpvRenderContext(
                self._mpv_player.mpv_instance,
                api_type='opengl',
                opengl_init_params={'get_proc_address': MpvGlGetProcAddressFn(self._proc_address_function)}
            )

            self._mpv_render_context.update_cb = self._mpv_player.do_update.emit

        return QQuickFramebufferObject.Renderer.createFramebufferObject(self, size)

    def render(self) -> None:
        if self._mpv_render_context is not None:
            rectangle = self._mpv_player.size()
            width = int(rectangle.width() * self.x_scale)
            height = int(rectangle.height() * self.y_scale)
            fbo = int(self.framebufferObject().handle())
            self._mpv_render_context.render(flip_y=False, opengl_fbo={"w": width, "h": height, "fbo": fbo})
