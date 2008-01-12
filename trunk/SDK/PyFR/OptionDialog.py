#
#  OptionDialog.py
#
#  Created by jchrist on 1/10/08

#import modules required by application
import objc
import Foundation
import AppKit

from BackRow import *

class OptionDialog(BROptionDialog):
    def initWithTitle_Items_Handler_UserData_(self,title,items,handler,userdata):
        BROptionDialog.init(self)
        self.setTitle_(title)
        for i in items:
            self.addOptionText_(i)
        self.setActionSelector_target_("response:", self)
        self.handler=handler
        self.userdata=userdata
        return self

    def response_(self):
        if self.handler(self,self.selectedIndex(),self.userdata):
            self.stack().popController()

# 
# example of using a OptionDialog:  
#    OptionDialogTest creates & pushes a dialog with prompts 1,2,3 and userdata [a,b,c]
#
# if the dialog is responded to (i.e. not backed out of), OptionDialogHandler will be 
# called with the index of the selected menu item and the userdata can be displayed
#

def testOptionDialogHandler(controller,idx,userdata):
    alert = BRAlertController.alertOfType_titled_primaryText_secondaryText_( 0, "Option response:", "Option #%s" % str(idx), "Userdata: %s" % str(userdata[idx]))
    controller.stack().pushController_(alert)

    # if we return true, we'll pop the controller and back up past the option dialog
    return False

def testOptionDialogTest(controller,arg):
    dlg=OptionDialog.alloc().initWithTitle_Items_Handler_UserData_("Test options",["Select a1","Select b","Select c"],testOptionDialogHandler,["a","b","c"])
    return controller.stack().pushController_(dlg)
