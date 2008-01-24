#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#


#import modules required by application
import PyFR.WaitController


class AppLauncherController(PyFR.WaitController.WaitController):
    def initWithApp_file_(self, text, application, file):
        self.app = application
        self.file = file
        PyFR.WaitController.WaitController.initWithText_( self, text )
        return self

    def PyFR_start(self):
        self.launchApp( self.app, self.file )

    def FRWasShown(self):
        self.stack().popController()





