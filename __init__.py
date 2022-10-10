#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

__license__   = 'GPL v3'
__copyright__ = '2018, bd-ober <https://github.com/bd-ober>'
__docformat__ = 'restructuredtext en'


# The class from which all Interface Action plugin wrappers must inherit.
from calibre.customize import InterfaceActionBase

class HBDownloaderInit(InterfaceActionBase):

    name                = 'Humble-Bundle Downloader'
    description         = 'Download ebooks from your Humble-Bundle library into calibre.'
    supported_platforms = ['linux','osx'] #TODO check other platforms
    author              = 'bd-ober'
    version             = (1, 0, 1)
    minimum_calibre_version = (0, 7, 53)

    actual_plugin       = 'calibre_plugins.hb_downloader.ui:HBDownloader'


    # Enable customization via Preferences->Plugins
    def is_customizable(self):
        
        return True


    # Implement custom configuration dialog.
    def config_widget(self):
        
        from calibre_plugins.hb_downloader.config import ConfigWidget
        return ConfigWidget()

    def load_actual_plugin(self, gui):
        # so the sys.path was modified while loading the plug impl.
        with self:

            # Make sure the fanficfare module is available globally
            # under its simple name, -- This is the only reason other
            # plugin files can import fanficfare instead of
            # calibre_plugins.fanficfare_plugin.fanficfare.
            #
            # Added specifically for the benefit of
            # eli-schwartz/eschwartz's Arch Linux distro that wants to
            # package FFF plugin outside Calibre.
            import calibre_plugins.hb_downloader.requests as requests
            return InterfaceActionBase.load_actual_plugin(self,gui)

    # Save the settings specified by the configuration widget
    def save_settings(self, config_widget):

        config_widget.save_settings()

        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
