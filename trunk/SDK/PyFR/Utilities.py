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

                        # I'm attempting to delay the file opening as
                        # late as possible, since FR likes to cover everything.
                        #if not self.fileOpened and self.fileToLoad is not None:
                        #    self.fileOpened = True
                        #    app = SBApplication.applicationWithURL_( NSURL.alloc().initFileURLWithPath_( self.launchedApp ) )
                        #    app.open_( self.fileToLoad )

                return True

        return False

    def launchedAppTick_(self, senders):

        found=self.IsRunning(True)

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
        self.fileToLoad = fileToLoad
        self.lookForApp = self.launchedApp.split('/')[-1][:-4]


        ws = Foundation.NSWorkspace.sharedWorkspace()
        ws.launchApplication_( self.launchedApp )

        # possibly Load App
        while not self.IsRunning():
    
            # I probably shouldn't use a sleep here, as thats not good GUI 
            # practice. But it works. Not like its going to be around long in 
            # here.
            time.sleep(0.5)

        # Start hiding the display
        frController = BRAppManager.sharedApplication().delegate()
        # We use continue, since it seems to skip the -slow- fade out.
        frController._continueDestroyScene_(None)

        self.fileOpened = False
        if not self.fileOpened and self.fileToLoad is not None:
            self.fileOpened = True
            app = SBApplication.applicationWithURL_( NSURL.alloc().initFileURLWithPath_( self.launchedApp ) )
            app.open_( self.fileToLoad )


        self.AboutToHideFR()
    
        # Start a timer
        self.timer = Foundation.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_( 0.25, self, "launchedAppTick:", None, True )
     
     





