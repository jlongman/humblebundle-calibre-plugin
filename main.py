#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'


from PyQt5.Qt import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, QLabel, QTextEdit

from config import prefs
import os
# Import hb-downloader stuff
from hb_downloader.humble_api.humble_api import HumbleApi
from hb_downloader.humble_download import HumbleDownload
from hb_downloader.config_data import ConfigData

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
        self.conf_button = QPushButton('Configure', self)
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
        if self.check_field_exists():
            existing_hb_filenames = db.all_field_names('#humble_filename')
        else:
            existing_hb_filenames = []
        self.textlog.append(str(len(existing_hb_filenames)) + ' existing books from Humble Bundle identified.')
        
        # Attempt to authenticate
        hapi = HumbleApi(prefs['cookie_auth_token'])
        ConfigData.download_location = prefs['download_loc']
        full_directory = os.path.join(ConfigData.download_location)
        if not os.path.exists(full_directory):
            os.makedirs(full_directory)

        if hapi.check_login():
            self.textlog.append('Authentication successful...')
        else:
            self.textlog.append('Unable to login - check authentication token.')
            return
        
        # Get orders
        game_keys = hapi.get_gamekeys()
        self.textlog.append('%s orders/keys found...' % (len(game_keys)))
        
        key_downloads = dict()
        
        # Get relevant downloads
        num_books_found = 0
        num_new_books = 0
        for key in game_keys:
            humble_downloads = []
            order = hapi.get_order(key)
            
            for subproduct in order.subproducts or []:
                for download in subproduct.downloads or []:
                    # Check platform
                    if download.platform != 'ebook':
                        continue
                    
                    for dl_struct in download.download_structs:
                        num_books_found += 1
                        
                        # Check filename
                        if dl_struct.filename in existing_hb_filenames:
                            continue
                        
                        humble_downloads.append( HumbleDownload(download, dl_struct, order, subproduct, key) )
                        num_new_books += 1
                        
            key_downloads[key] = humble_downloads
        
        self.textlog.append('(%s/%s) books found do not already exist in Calibre...' % (num_new_books, num_books_found) )
        
        ticker = 0
        for key in key_downloads:
            # Update URL in case of expiry
            HumbleDownload.update_download_list_url(hapi, key_downloads.get(key))
            
            for hd in key_downloads.get(key):
                ticker += 1
    
                if hd.filename.endswith('.cbz') or hd.filename.endswith(".pdf"):
                    self.textlog.append('(%s/%s) Skipping %s ...' % (ticker, num_new_books, hd.filename))
                    continue
                self.textlog.append('(%s/%s) Downloading %s ...' % (ticker, num_new_books, hd.filename) )
                hd.download_file()


    def config(self):
        self.do_user_config(parent=self)
        self.refresh_label()
        self.textlog.append('Config changed.')
        
        
    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About Humble-Bundle downloader', text.decode('utf-8'))
