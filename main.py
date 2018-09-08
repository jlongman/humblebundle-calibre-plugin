#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'


from PyQt5.Qt import QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel

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

        # Create layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add label
        self.label = QLabel('')
        self.layout.addWidget(self.label)
        self.refresh_label()

        # Add 'about' button
        self.about_button = QPushButton('About', self)
        self.about_button.clicked.connect(self.about)
        self.layout.addWidget(self.about_button)

        # Add config button
        self.conf_button = QPushButton('Set authentication token', self)
        self.conf_button.clicked.connect(self.config)
        self.layout.addWidget(self.conf_button)

        self.resize(self.sizeHint())

    
    def refresh_label(self):
        if prefs['cookie_auth_token'] == '' :
            self.label.setText('Authentication token not set.')
        else:
            self.label.setText('Authentication token set.')


    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About Humble-Bundle downloader', text.decode('utf-8'))


    #def marked(self):
        #''' Show books with only one format '''
        #db = self.db.new_api
        #matched_ids = {book_id for book_id in db.all_book_ids() if len(db.formats(book_id)) == 1}
        ## Mark the records with the matching ids
        ## new_api does not know anything about marked books, so we use the full
        ## db object
        #self.db.set_marked_ids(matched_ids)

        ## Tell the GUI to search for all marked records
        #self.gui.search.setEditText('marked:true')
        #self.gui.search.do_search()

    #def view(self):
        #''' View the most recently added book '''
        #most_recent = most_recent_id = None
        #db = self.db.new_api
        #for book_id, timestamp in db.all_field_for('timestamp', db.all_book_ids()).iteritems():
            #if most_recent is None or timestamp > most_recent:
                #most_recent = timestamp
                #most_recent_id = book_id

        #if most_recent_id is not None:
            ## Get a reference to the View plugin
            #view_plugin = self.gui.iactions['View']
            ## Ask the view plugin to launch the viewer for row_number
            #view_plugin._view_calibre_books([most_recent_id])

    #def update_metadata(self):
        #'''
        #Set the metadata in the files in the selected book's record to
        #match the current metadata in the database.
        #'''
        #from calibre.ebooks.metadata.meta import set_metadata
        #from calibre.gui2 import error_dialog, info_dialog

        ## Get currently selected books
        #rows = self.gui.library_view.selectionModel().selectedRows()
        #if not rows or len(rows) == 0:
            #return error_dialog(self.gui, 'Cannot update metadata', 'No books selected', show=True)
        ## Map the rows to book ids
        #ids = list(map(self.gui.library_view.model().id, rows))
        #db = self.db.new_api
        #for book_id in ids:
            ## Get the current metadata for this book from the db
            #mi = db.get_metadata(book_id, get_cover=True, cover_as_data=True)
            #fmts = db.formats(book_id)
            #if not fmts:
                #continue
            #for fmt in fmts:
                #fmt = fmt.lower()
                ## Get a python file object for the format. This will be either
                ## an in memory file or a temporary on disk file
                #ffile = db.format(book_id, fmt, as_file=True)
                #ffile.seek(0)
                ## Set metadata in the format
                #set_metadata(ffile, mi, fmt)
                #ffile.seek(0)
                ## Now replace the file in the calibre library with the updated
                ## file. We dont use add_format_with_hooks as the hooks were
                ## already run when the file was first added to calibre.
                #db.add_format(book_id, fmt, ffile, run_hooks=False)

        #info_dialog(self, 'Updated files', 'Updated the metadata in the files of %d book(s)'%len(ids), show=True)


    def config(self):
        self.do_user_config(parent=self)
        self.refresh_label()
