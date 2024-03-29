#
#  OptionDialog.py
#
#  Created by jchrist on 1/10/08

from BackRow import *
import Foundation


class OptionItem(object):
    def __init__(self, text, userdata):
        self.text = text
        self.data = userdata

class OptionDialog(BROptionDialog):
    # You can either pass in a handler function to be called, or override handler in your subclassclass
    def initWithTitle_Items_Handler_(self, title, items, handler=None):
        self=super(OptionDialog,self).init()
        if self is None:
            return None
        
        self.items = items
        self.setTitle_(title)
        for i in self.items:
            self.addOptionText_(i.text)
        self.setActionSelector_target_("response:", self)
        self.handler_func=handler
        return self

    def response_(self,sender):
        if self.handler_func(self, self.selectedIndex(), self.items[ self.selectedIndex() ]):
            self.stack().popController()

    def handler(self, controller, index, item):
        # this should be overridden in the users class
        alert = BRAlertController.alertOfType_titled_primaryText_secondaryText_( 0, "Option response:", "Option #%s" % str(index), "Userdata: %s" % item.data)
        self.stack().pushController_(alert)
        #alret.release()
        return True

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
    #alert.release()
    # if we return true, we'll pop the controller and back up past the option dialog
    return False

def testOptionDialogTest(controller,arg):
    dlg=OptionDialog.alloc().initWithTitle_Items_Handler_UserData_("Test options",["Select a1","Select b","Select c"],testOptionDialogHandler,["a","b","c"])
    ret=controller.stack().pushController_(dlg)
    #dlg.release()
    return ret

def testFromMain():
    menuItems = [ OptionItem( "select %d" % i, i+50 ) for i in range(0,3) ]

    ret=OptionDialog.alloc().initWithTitle_Items_Handler_( "Test options", menuItems )
    return ret
