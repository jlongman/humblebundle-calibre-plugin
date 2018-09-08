#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'


from PyQt5.Qt import QWidget, QHBoxLayout, QLabel, QLineEdit
from calibre.utils.config import JSONConfig


prefs = JSONConfig('plugins/hb_downloader')

# Set defaults
prefs.defaults['cookie_auth_token'] = ''

class ConfigWidget(QWidget):

    def __init__(self):
        
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('Auth token:')
        self.layout.addWidget(self.label)

        self.msg = QLineEdit(self)
        self.msg.setText(prefs['cookie_auth_token'])
        self.layout.addWidget(self.msg)
        self.label.setBuddy(self.msg)

    def save_settings(self):
        prefs['cookie_auth_token'] = unicode(self.msg.text())

