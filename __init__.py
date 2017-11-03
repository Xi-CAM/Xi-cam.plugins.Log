import numpy as np
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from xicam.core import msg

colors = {msg.DEBUG: Qt.gray, msg.ERROR: Qt.darkRed, msg.CRITICAL: Qt.red,
          msg.INFO: Qt.white, msg.WARNING: Qt.yellow}

from xicam.plugins import GUIPlugin, GUILayout


class LogPlugin(GUIPlugin):
    name = 'Log'
    sigLog = Signal(int, str, str, np.ndarray)

    def __init__(self, *args, **kwargs):
        self.logwidget = QListWidget()
        self.stages = {'Log': GUILayout(self.logwidget)}

        # msg.guilogcallable = self.log

        super(LogPlugin, self).__init__(*args, **kwargs)

    def log(self, level, timestamp, s, image=None, icon=None):  # We can have icons!
        item = QListWidgetItem(s)
        item.setForeground(QBrush(colors[level]))
        item.setToolTip(timestamp)
        self.logwidget.addItem(item)
        if image is not None:
            image = np.uint8((image - image.min()) / image.ptp() * 255.0)
            pixmap = QPixmap.fromImage(QImage(image, image.shape[0], image.shape[1], QImage.Format_Indexed8))
            i = QListWidgetItem()
            w = QLabel()
            w.setPixmap(pixmap)
            size = QSize(*image.shape)
            w.setFixedSize(size)
            i.setSizeHint(w.sizeHint())
            self.centerwidget.addItem(i)
            self.centerwidget.setItemWidget(i, w)
