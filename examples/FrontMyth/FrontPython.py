#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#


#import modules required by application
import PyFR.Appliance


#class RUIPythonAppliance( PyFR.Appliance.Appliance ):
#    def getController(self):
#        return BRAlertController.alertOfType_titled_primaryText_secondaryText_( 0, "Title", "Hello", "world" )

import PyFR.WaitController

class MyWaitController(PyFR.WaitController.WaitController):
    def PyFR_start(self):
        self.launchApp( '/Applications/MythFrontend.app')

class RUIPythonAppliance( PyFR.Appliance.Appliance ):
    def getController(self):
        return MyWaitController.alloc().initWithText_("Loading Myth")






