# -*- coding: utf-8 -*-
#
# (c) Copyright 2001-2015 HP Development Company, L.P.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Authors: Don Welch
#

# StdLib
import operator

# Local
from base.g import *
from base import device, utils, maint
from prnt import cups
from base.codes import *
from .ui_utils import *

# Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Ui
from .pqdiagdialog_base import Ui_Dialog


class PQDiagDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, device_uri):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.device_uri = device_uri
        self.initUi()

        QTimer.singleShot(0, self.updateUi)


    def initUi(self):
        # connect signals/slots
        self.connect(self.CancelButton, SIGNAL("clicked()"), self.CancelButton_clicked)
        self.connect(self.RunButton, SIGNAL("clicked()"), self.RunButton_clicked)
        self.connect(self.DeviceComboBox, SIGNAL("DeviceUriComboBox_noDevices"), self.DeviceUriComboBox_noDevices)
        self.connect(self.DeviceComboBox, SIGNAL("DeviceUriComboBox_currentChanged"), self.DeviceUriComboBox_currentChanged)
        self.DeviceComboBox.setFilter({'pq-diag-type': (operator.gt, 0)})

        # Application icon
        self.setWindowIcon(QIcon(load_pixmap('hp_logo', '128x128')))

        if self.device_uri:
            self.DeviceComboBox.setInitialDevice(self.device_uri)


    def updateUi(self):
        self.DeviceComboBox.updateUi()
        self.LoadPaper.setButtonName(self.__tr("Run"))
        self.LoadPaper.updateUi()


    def DeviceUriComboBox_currentChanged(self, device_uri):
        self.device_uri = device_uri


    def DeviceUriComboBox_noDevices(self):
        FailureUI(self, self.__tr("<b>No devices that support print quality diagnostics found.</b><p>Click <i>OK</i> to exit.</p>"))
        self.close()


    def CancelButton_clicked(self):
        self.close()


    def RunButton_clicked(self):
        d = None

        try:
            try:
                d = device.Device(self.device_uri)
            except Error:
                CheckDeviceUI(self)
                return

            pqdiag_type = d.pq_diag_type

            try:
                d.open()
            except Error:
                CheckDeviceUI(self)
            else:
                if d.isIdleAndNoError():
                    if pqdiag_type == 1:
                        maint.printQualityDiagType1(d, lambda : True)

                    elif pqdiag_type == 2:
                        maint.printQualityDiagType2(d, lambda : True)

                else:
                    CheckDeviceUI(self)

        finally:
            if d is not None:
                d.close()

        self.close()

    #
    # Misc
    #

    def __tr(self,s,c = None):
        return qApp.translate("PQDiagDialog",s,c)


