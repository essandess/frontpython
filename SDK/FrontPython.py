#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#


#import modules required by application
import PyFR.Appliance
import PyFR.WaitController
import PyFR.Debugging
import PyFR.OptionDialog
import PyFR.FileBrowser
import PyFR.AppLauncherController

class MyFileBrowser(PyFR.FileBrowser.FileBrowserController):
    def init(self):
        PyFR.FileBrowser.FileBrowserController.initWithDirectory_( self, "/Users/garion/Movies" )
        return self

    def fileSelected_(self, selectedFile):
        self.stack().pushController_( 
            PyFR.AppLauncherController.AppLauncherController.alloc().initWithApp_file_( 'Launching VLC',
                                                                                        '/Applications/VLC.app', 
                                                                                        selectedFile ) )

class RUIPythonAppliance( PyFR.Appliance.Appliance ):
    def getController(self):
        return MyFileBrowser.alloc().init()






