#
#  main.py
#  FrontPython
#
#  Created by garion on 12/15/07.
#  Copyright __MyCompanyName__ 2007. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

# Import backrow
objc.loadBundle("BackRow", globals(), bundle_path=objc.pathForFramework("/System/Library/PrivateFrameworks/BackRow.framework" ))

def log(s):
    Foundation.NSLog( "FrontPython: %s" % str(s) )


key = u"com.tzo.garion.frontpython"

class RUIPythonAppliance( BRAppliance ):

    sanityCheck = False

    @classmethod
    def initialize(cls):
        name = NSString.alloc().initWithString_( u"com.apple.frontrow.appliance.frontpython" )
        BRFeatureManager.sharedInstance().enableFeatureNamed_( name )

    @classmethod
    def className(cls):

        clsName = NSString.alloc().initWithString_( cls.__name__ )

        backtrace = BRBacktracingException.backtrace()
        range = backtrace.rangeOfString_( "_loadApplianceInfoAtPath:" )

        if range.location == Foundation.NSNotFound and cls.sanityCheck == False:
            range = backtrace.rangeOfString_( "(in BackRow)" )
            cls.sanityCheck = True
        
        if range.location != Foundation.NSNotFound:
            clsName = NSString.alloc().initWithString_( "RUIMoviesAppliance" )

        return clsName

    def applianceController(self):

        alert = BRAlertController.alertOfType_titled_primaryText_secondaryText_( 0, "Title", "Hello", "world" )

        return alert


