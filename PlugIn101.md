  1. Download the SDK. We currently recommend downloading the source from subversion, as we haven't really made an official release yet.
  1. Copy the files from the SDK/ directory to your own directory.
  1. Edit English.lproj/InfoPlist.strings. The CFBundleName is the name that will appear in the menu.
  1. Edit the setup.py file. You'll want to change the NSPrincipleClass, CFBundleExecutable, and CFBundleName..
  1. Rename FrontPython.py to match what you named the CFBundleExecutable (followed by the .py)..
  1. Edit your newly named file, and change the name of the class that overrides PyFR.Appliance to match the name you entered for NSPrincipleClass.
  1. Run "python setup.py py2app -A". This creates a plugin for you, in the dist directory. It will be named after what you put into CFBundleName (I think, untested)
  1. Create a symlink in your FrontRow directory: ln -s <path to your project>/dist/

&lt;projectname&gt;

.frappliance /System/Library/CoreServices/Front Row.app/Contents/PlugIns/
  1. Restart Frontrow.

At this point, you should be able to see your plugin in Frontrow.

(this is not finished. Crap I have to go. Saving for now.)