 #!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'


from PyQt5.Qt import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from calibre.utils.config import JSONConfig


prefs = JSONConfig('plugins/hb_downloader')

# Set defaults
prefs.defaults['cookie_auth_token'] = ''
prefs.defaults['download_loc'] = '~/Downloads/'

class ConfigWidget(QWidget):

    def __init__(self):
        
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        
        self.AuthLayout = QHBoxLayout()
        self.layout.addLayout(self.AuthLayout)

        self.AuthLabel = QLabel('Auth token:')
        self.AuthLayout.addWidget(self.AuthLabel)

        self.AuthMsg = QLineEdit(self)
        self.AuthMsg.setText(prefs['cookie_auth_token'])
        self.AuthLayout.addWidget(self.AuthMsg)
        self.AuthLabel.setBuddy(self.AuthMsg)
        
        
        self.DownloadLayout = QHBoxLayout()
        self.layout.addLayout(self.DownloadLayout)

        self.DownloadLabel = QLabel('Download location:')
        self.DownloadLayout.addWidget(self.DownloadLabel)

        self.DownloadMsg = QLineEdit(self)
        self.DownloadMsg.setText(prefs['download_loc'])
        self.DownloadLayout.addWidget(self.DownloadMsg)
        self.DownloadLabel.setBuddy(self.DownloadMsg)

    def save_settings(self):
        
        prefs['cookie_auth_token'] = self.AuthMsg.text()
        prefs['download_loc'] = self.DownloadMsg.text()
