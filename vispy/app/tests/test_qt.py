# Import PyQt4, vispy will see this and use that as a backend
# Also import QtOpenGL, because vispy needs it.

# This is a strange test: vispy does not need designer or uic stuff to run!

from os import path as op

from vispy.app import Canvas, default_app
from vispy.testing import requires_application, SkipTest
from vispy.gloo import gl


@requires_application('pyqt4', has=['uic'])
def test_qt_designer():
    """Embed Canvas via Qt Designer"""
    default_app.use()
    if 'pyqt4' not in default_app.backend_name.lower():
        raise SkipTest('Not using PyQt4 backend')  # wrong backend
    from PyQt4 import uic
    fname = op.join(op.dirname(__file__), 'qt-designer.ui')
    WindowTemplate, TemplateBaseClass = uic.loadUiType(fname)
    default_app.create()  # make sure we have an app, or the init will fail

    class MainWindow(TemplateBaseClass):

        def __init__(self):
            TemplateBaseClass.__init__(self)

            self.ui = WindowTemplate()
            self.ui.setupUi(self)
            self.show()

    win = MainWindow()
    try:
        win.show()
        canvas = Canvas(create_native=False)
        canvas.app.use()  # Make sure the app exists (because create_native=0)
        canvas._set_backend(win.ui.canvas)
        canvas.create_native()

        @canvas.events.draw.connect
        def on_draw(ev):
            gl.glClearColor(0.0, 0.0, 0.0, 0.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            canvas.swap_buffers()
    finally:
        win.close()
