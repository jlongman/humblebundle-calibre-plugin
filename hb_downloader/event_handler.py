#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logger
from hb_downloader.humble_api.events import Events

__author__ = "Brian Schkerke"
__copyright__ = "Copyright 2016 Brian Schkerke"
__license__ = "MIT"


class EventHandler(object):
    @staticmethod
    def initialize():
        Events.on(Events.EVENT_MD5_START, EventHandler.print_md5_start)
        Events.on(Events.EVENT_MD5_END, EventHandler.print_md5_end)
        Events.on(Events.EVENT_DOWNLOAD_START,
                  EventHandler.print_download_start)
        Events.on(Events.EVENT_DOWNLOAD_END, EventHandler.print_download_end)
        Events.on(Events.EVENT_PROGRESS, EventHandler.print_progress)

    @staticmethod
    def print_md5_start(filename):
        logger.display_message(False, "Checksum", "%s: " % filename, False)
        sys.stdout.flush()

    @staticmethod
    def print_md5_end(filename):
        print("")

    @staticmethod
    def print_download_start(filename):
        logger.display_message(False, "Download", "%s: " % filename, False)
        sys.stdout.flush()

    @staticmethod
    def print_download_end(filename):
        print("")

    @staticmethod
    def print_progress(percentage):
        sys.stdout.write("{0:.0f}% ".format(percentage))
        sys.stdout.flush()
