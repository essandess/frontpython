from distutils.core import setup
import py2app


plist = dict(NSPrincipalClass='RUIFrontMyth',
             CFBundleDevelopmentRegion='English',
             CFBundleExecutable='FrontMyth',
             CFBundleName='FrontMyth',
             CFBundleIdentifier="com.apple.frontrow.appliance.FrontMyth",
             CFBundleInfoDictionaryVersion='6.0',
             CFBundlePackageType='BNDL',
             CFBundleSignature='????',
             CFBundleVersion='1.0',
             FRApplianceIconHorizontalOffset=0.046899999999999997,
             FRApplianceIconKerningFactor=0.10000000000000001,
             FRApplianceIconReflectionOffset=-0.125,
             FRAppliancePreferedOrderValue=-1,
             FRRemoteAppliance=True )


setup(
    plugin = ['FrontMyth.py'],
    packages = ['PyFR'],
    data_files=['English.lproj'],
    options=dict(py2app=dict(extension='.frappliance', plist=plist))
 )
