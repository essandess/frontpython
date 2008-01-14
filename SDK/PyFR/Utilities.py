import time

import objc
import Foundation
import AppKit

from BackRow import *


class ControllerUtilities:
    """ this is a mixin with some useful utilities for other Controllers """

    # Logging.
    def log(self, s):
        Foundation.NSLog( "%s: %s" % (self.__class__.__name__, str(s) ) )


    # subclass can replace this with an additional exit condition test.  If this fn returns true
    # we return to FrontRow
    def AppShouldExit(self):
        return False

    def AboutToHideFR(self):
        return False

    def AboutToShowFR(self):
        return False


    def IsRunning(self, ping=False):
        # Check to see if App is running.
        for app in Foundation.NSWorkspace.sharedWorkspace().launchedApplications():
            if app['NSApplicationName'] == self.lookForApp:
                
                # Is it the active app?
                ws = Foundation.NSWorkspace.sharedWorkspace()
                
                activeApp = ws.activeApplication()
                if activeApp['NSApplicationName'] != self.lookForApp:

                    # ping it, so it becomes active.
                    # Why do we do this you ask? Well.. When we hide front row
                    # above, it brings the last active application to the front.
                    # Why? I don't know.

                    if (ping):
                        ws.launchApplication_( self.launchedApp )

                return True

        return False

    def launchedAppTick_(self, senders):

        self.log('*'*80)

        found=self.IsRunning(True)

        # If we don't find App running, then we exited. So bring FR back.
        if not found or self.AppShouldExit():
            frController = BRAppManager.sharedApplication().delegate()
            frController._showFrontRow()

            # Make sure to turn off the timer!
            self.timer.invalidate()

    def launchApp(self, appToLaunch):
        """ launches the application specified by appToLaunch.

            appToLaunch is a full path to an application. For example,
            to launch Sarafi, it would be:
                "/Applications/Safari.app"
        """

        self.launchedApp = appToLaunch
        self.lookForApp = self.launchedApp.split('/')[-1][:-4]

        # possibly Load App
        while not self.IsRunning():
            ws = Foundation.NSWorkspace.sharedWorkspace()
            ws.launchApplication_( self.launchedApp )

            # I probably shouldn't use a sleep here, as thats not good GUI 
            # practice. But it works. Not like its going to be around long in 
            # here.
            time.sleep(0.5)

        self.AboutToHideFR()

        # Get FR out of the way. Boy was this fun trying to figure out.
        frController = BRAppManager.sharedApplication().delegate()
        frController._hideFrontRow()

        # Start a timer
        self.log(self.launchedAppTick_)
        self.timer = Foundation.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_( 0.25, self, "launchedAppTick:", None, True )


