#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'

# The class from which all Interface Action plugin wrappers must inherit.
from calibre.customize import InterfaceActionBase

class InterfacePluginDemo(InterfaceActionBase):

    name                = 'Humble-Bundle Downloader'
    description         = 'Download ebooks from your Humble-Bundle library into calibre.'
    supported_platforms = ['linux'] #TODO check other platforms
    author              = 'bd-ober'
    version             = (1, 0, 0)
    minimum_calibre_version = (0, 7, 53)

    actual_plugin       = 'calibre_plugins.hb_downloader.ui:InterfacePlugin'


    # Enable customization via Preferences->Plugins
    def is_customizable(self):
        
        return True


    # Implement custom configuration dialog.
    def config_widget(self):
        
        from calibre_plugins.hb_downloader.config import ConfigWidget
        return ConfigWidget()


    # Save the settings specified by the configuration widget
    def save_settings(self, config_widget):

        config_widget.save_settings()

        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
