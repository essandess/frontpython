#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#


#import modules required by application
import WaitController
import objc

class AppLauncherController(WaitController.WaitController):
    def initWithApp_file_(self, application, file):
        self.app = application
        self.file = file
        WaitController.WaitController.initWithText_( self, "Launching application" )
        return self

    def initWithApp_( self, application ):
        self.app = application
        self.file = None
        WaitController.WaitController.initWithText_( self, "Launching application" )
        return self

    def PyFR_start(self):
        self.launchApp( self.app, self.file )

        # FR automatically quits after 20 minutes.  This should disable that behavior...
        #   not tested here, you might need to do this a few seconds into your AppShouldExit callback
        foo=objc.lookUpClass("FRAutoQuitManager")
        foo.sharedManager().setAutoQuitEnabled_(False)


    def FRWasShown(self):
        self.waitDone()
