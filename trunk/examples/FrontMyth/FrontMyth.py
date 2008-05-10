#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#


#import modules required by application
import PyFR.Appliance
import PyFR.AppLauncherController
#import PyFR.Debugging

class MythLaunch(PyFR.AppLauncherController.AppLauncherController):
    def init(self):
        PyFR.AppLauncherController.AppLauncherController.initWithApp_( self,
                                                                       'Launching MythTV',
                                                                       '/Applications/MythFrontend.app' )
        return self
    
class RUIFrontMyth( PyFR.Appliance.Appliance ):
    def getController(self):
        return MythLaunch.alloc().init()






