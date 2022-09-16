import ctypes
import platform

from PySide6.QtGui import QOffscreenSurface, QOpenGLContext


class RenderContext:

    def __init__(self):
        self._context = self._current_opengl_context()
        self._surface = QOffscreenSurface()
        self._surface.create()

    def _current_opengl_context(self):
        operating_system = platform.system()
        if operating_system == 'Linux':
            return self.linux_context()
        elif operating_system == 'Window':
            return self.windows_context()
        elif operating_system == 'Darwin':
            return self.darwin_context()
        else:
            raise f"Platform {operating_system} not supported yet"

    def get_proc_address(self, context, name):
        address = self._context(name)
        return ctypes.cast(address, ctypes.c_void_p).value

    def darwin_context(self):
        # try:
        #     import glfw
        #     return self.glfw_implementation
        # except AttributeError:
        #     pass
        try:
            from OpenGL import GLUT
            return self.glut_implementation
        except AttributeError:
            pass
        raise 'Cannot initialize OpenGL'

    def linux_context(self):
        try:
            from OpenGL import GLX
            return self.glx_implementation
        except AttributeError:
            pass
        try:
            from OpenGL import EGL
            return self.egl_implementation
        except AttributeError:
            pass
        raise 'Cannot initialize OpenGL'

    def windows_context(self):
        try:
            import glfw
            return self.glfw_implementation
        except AttributeError:
            pass
        try:
            from OpenGL import GLUT
            return self.glut_implementation
        except AttributeError:
            pass
        raise 'Cannot initialize OpenGL'

    @staticmethod
    def glut_implementation(name: bytes):
        from OpenGL import GLUT
        return GLUT.glutGetProcAddress(name)

    @staticmethod
    def glx_implementation(name: bytes):
        from OpenGL import GLX
        return GLX.glXGetProcAddress(name)

    @staticmethod
    def egl_implementation(name: bytes):
        from OpenGL import EGL
        return EGL.eglGetProcAddress(name)

    @staticmethod
    def wgl_implementation(name: bytes):
        from OpenGL import WGL
        return WGL.wglGetProcAddress(name)

    def glfw_implementation(self, name: bytes):
        import glfw

        if not glfw.init():
            raise 'Cannot initialize OpenGL'

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(1, 1, "", None, None)

        glfw.make_context_current(window)
        context = QOpenGLContext.currentContext()
        context.makeCurrent(self._surface)
        return glfw.get_proc_address(name.decode('utf-8'))





