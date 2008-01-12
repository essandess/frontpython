import traceback

import Foundation
import PyObjCTools.Debugging

def PyFRExceptionLogger(exception):
    userInfo = exception.userInfo()

    excStr = traceback.format_exception( userInfo[u'__pyobjc_exc_type__'],
                                         userInfo[u'__pyobjc_exc_value__'],
                                         userInfo[u'__pyobjc_exc_traceback__'] )

    for line in excStr:
        for l in line.split('\n'):
            Foundation.NSLog( l.decode('utf8') )


    # we logged it, so don't log it for us
    return False


PyObjCTools.Debugging.nsLogPythonException = PyFRExceptionLogger

PyObjCTools.Debugging.installPythonExceptionHandler()

