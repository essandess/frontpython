import Foundation

from BackRow import *

class Appliance( BRAppliance ):
    # Logging.
    def log(self,s):
        Foundation.NSLog( "%s: %s" % (self.__class__.__name__, str(s) ) )

    sanityCheck = False

    @classmethod
    def initialize(cls):
        BRFeatureManager.sharedInstance().enableFeatureNamed_( u"com.apple.frontrow.appliance.frontpython" )

    @classmethod
    def className(cls):

        clsName = cls.__name__

        backtrace = BRBacktracingException.backtrace()
        range = backtrace.rangeOfString_( "_loadApplianceInfoAtPath:" )

        if range.location == Foundation.NSNotFound and cls.sanityCheck == False:

            range = backtrace.rangeOfString_( "(in BackRow)" )
            cls.sanityCheck = True
        
        if range.location != Foundation.NSNotFound:
            clsName = u"RUIMoviesAppliance"
        return clsName

    def applianceController(self):
        return self.getController()

    def applianceControllerWithScene_(self, scene):
        return self.getController()

