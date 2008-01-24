import time
import os 

import objc
import Foundation
import AppKit
from ScriptingBridge import *

from BackRow import *


class ControllerUtilities:
    """ this is a mixin with some useful utilities for other Controllers """
    def enableObjCCapture(self):
        objc.loadBundleFunctions(Foundation.__bundle__, globals(),[('instrumentObjcMessageSends', objc._C_VOID + objc._C_NSBOOL)])
        instrumentObjcMessageSends(True)

    def disableObjCCapture(self):
        objc.loadBundleFunctions(Foundation.__bundle__, globals(),[('instrumentObjcMessageSends', objc._C_VOID + objc._C_NSBOOL)])
        instrumentObjcMessageSends(False)


    # Logging.
    def log(self, s):
        Foundation.NSLog( "%s: %s" % (self.__class__.__name__, str(s) ) )


    # subclass can replace this with an additional exit condition test.  If this fn returns true
    # we return to FrontRow
    def AppShouldExit(self):
        return False

    def AboutToHideFR(self):
        return False

    def FRWasShown(self):
        return False


    def __IsRunning(self):
        # Check to see if App is running.
        for app in Foundation.NSWorkspace.sharedWorkspace().launchedApplications():
            if app['NSApplicationName'] == self.lookForApp:
                return True

        return False

    def launchedAppTick_(self, senders):
        # timer method to see if the app we launched is still running.
        # If not, exit back to FR.

        found=self.__IsRunning()

        # If we don't find App running, then we exited. So bring FR back.
        if not found or self.AppShouldExit():
            frController = BRAppManager.sharedApplication().delegate()
            frController._makeScene()

            # Make sure to turn off the timer!
            self.timer.invalidate()

            self.FRWasShown()

    def launchApp(self, appToLaunch, fileToLoad=None):
        """ launches the application specified by appToLaunch.
    
            appToLaunch is a full path to an application. For example,
            to launch Sarafi, it would be:
                "/Applications/Safari.app"
        """
    
        self.launchedApp = appToLaunch
        self.lookForApp = self.launchedApp.split('/')[-1][:-4]

        # Launch the app
        ws = Foundation.NSWorkspace.sharedWorkspace()
        ws.launchApplication_( self.launchedApp )

        # possibly Load App
        while not self.__IsRunning():
    
            # I probably shouldn't use a sleep here, as thats not good GUI 
            # practice. But it works. Not like its going to be around long in 
            # here.
            time.sleep(0.5)

        # Start hiding the display
        frController = BRAppManager.sharedApplication().delegate()
        # We use continue, since it seems to skip the -slow- fade out.
        # It also doesn't seem to kill the controller stack!
        frController._continueDestroyScene_(None)

        # Ping the app to the front
        ws.launchApplication_( self.launchedApp )

        # Tell the app to load the file we want to open, if necessary.
        if fileToLoad is not None:
            app = SBApplication.applicationWithURL_( NSURL.alloc().initFileURLWithPath_( self.launchedApp ) )
            app.open_( fileToLoad )

        # Well, we already hid, so we may move this. 
        self.AboutToHideFR()
    
        # Start a timer
        self.timer = Foundation.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_( 0.25, self, "launchedAppTick:", None, True )
     
     





