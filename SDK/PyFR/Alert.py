#import modules required by application
from BackRow import *

def Alert(controller,msg):
    alert = BRAlertController.alertOfType_titled_primaryText_secondaryText_( 0, "Alert", msg, "Press any remote button to go back.")
    return controller.stack().pushController_(alert)

#
# example usage
#

# import PyFR.Alert
# def SomeRandomMenuHandler(controller, arg):
#      return PyFR.Alert.Alert(controller, "Eat me!")

