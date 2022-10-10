#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'


# The class from which all interface action plugins must inherit
from calibre.gui2.actions import InterfaceAction
from main import HBDDialog

class HBDownloader(InterfaceAction):

    name = 'Humble-Bundle Downloader'

    # Declare the main action associated with this plugin
    action_spec = ('HB Sync', None, 'Sync library with Humble', None)


    # This method is called once per plugin, do initial setup here
    def genesis(self):

        icon = get_icons('images/icon.png')

        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)


    def show_dialog(self):
        
        # The base plugin object defined in __init__.py
        base_plugin_object = self.interface_action_base_plugin
        
        # Show the config dialog
        do_user_config = base_plugin_object.do_user_config

        d = HBDDialog(self.gui, self.qaction.icon(), do_user_config)
        d.show()


    def apply_settings(self):
        from calibre_plugins.hb_downloader.config import prefs
        prefs
