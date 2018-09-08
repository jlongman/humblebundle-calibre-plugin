#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'


from PyQt5.Qt import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, QLabel, QTextEdit

from calibre_plugins.hb_downloader.config import prefs

class HBDDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        # The current database shown in the GUI
        # db is an instance of the class LibraryDatabase from db/legacy.py
        # This class has many, many methods that allow you to do a lot of
        # things. For most purposes you should use db.new_api, which has
        # a much nicer interface from db/cache.py
        self.db = gui.current_db

        # Window properties
        self.setWindowTitle('Humble-Bundle Downloader')
        self.setWindowIcon(icon)

        # Create main layout
        self.mainlayout = QHBoxLayout()
        self.setLayout(self.mainlayout)

        # Create layout for buttons
        self.buttonlayout = QVBoxLayout()
        self.mainlayout.addLayout(self.buttonlayout)

        # Add label
        self.label = QLabel('')
        self.buttonlayout.addWidget(self.label)

        # Add config button
        self.conf_button = QPushButton('Set authentication token', self)
        self.conf_button.clicked.connect(self.config)
        self.buttonlayout.addWidget(self.conf_button)
        
        # Add Sync button
        self.Import_button = QPushButton('Import', self)
        self.Import_button.clicked.connect(self.Import)
        self.buttonlayout.addWidget(self.Import_button)
        
        # Add 'about' button
        self.about_button = QPushButton('About', self)
        self.about_button.clicked.connect(self.about)
        self.buttonlayout.addWidget(self.about_button)

        # Add log pane
        self.textlog = QTextEdit(self)
        self.mainlayout.addWidget(self.textlog)
        self.textlog.setReadOnly(True)

        self.refresh_label()
        self.check_field_exists()
        self.resize(800,200)

    
    def check_field_exists(self):
        db = self.db.new_api
        
        if '#humble_filename' in db.get_categories():
            self.textlog.append('#humble_filename field exists.')
        else:
            self.textlog.append('#humble_filename field does not exist.')
            # TODO Create the field here
        
    
    def refresh_label(self):
        if prefs['cookie_auth_token'] == '' :
            self.label.setText('Authentication token not set.')
            self.Import_button.setEnabled(False)
        else:
            self.label.setText('Authentication token set.')
            self.Import_button.setEnabled(True)


    def Import(self):
        # Identify any existing books with humblebundle tag
        db = self.db.new_api
        existing_hb_filenames = db.all_field_names('#humble_filename')
        
        self.textlog.append(str(len(existing_hb_filenames)) + ' existing books from Humble Bundle identified.')
        """
        TODO    -- Pass existing_hb_filenames as ignores to hb-downloader, and download to a specified location
                -- Have calibre import these
                -- Add #humble_filename field to the new books
                -- Delete from download directory?
        """

    def config(self):
        self.do_user_config(parent=self)
        self.refresh_label()
        self.textlog.append('Authentication token changed.')
        
        
    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About Humble-Bundle downloader', text.decode('utf-8'))
