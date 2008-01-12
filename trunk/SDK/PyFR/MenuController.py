import objc
import Foundation
import AppKit

from BackRow import *
from Utilities import ControllerUtilities

# in individual menu item with text, a function to be called when activated, and an optionional argument to be passed to the function
class MenuItem(ControllerUtilities):
      def __init__(self,title,func,arg=None,metadata_func=None,subtitle=""):
            self.title=title
            self.subtitle=subtitle
            self.func=func
            self.arg=arg
            self.metadata_func=metadata_func

      def Activate(self, controller):
          self.log("In activate for menu item %s" % self.title)
          self.func(controller, self.arg)

      def GetMetadata(self, controller):
            self.log("In GetMetadata for menu item %s" % self.title)
            if self.metadata_func is not None:
                  return self.metadata_func(controller, self.arg)
            else:
                  return None
            

# simple container class for a menu, elements of the items list may contain menu items or another Menu instance for submenus
class Menu:
      def __init__(self,page_title,items=[],subtitle=""):
          self.page_title=page_title
          self.items=items
          self.subtitle=subtitle
          
      def AddItem(self,item):
          self.items.append(item)

# used to duck-type Menus (to indicate an item is a submenu)
def IsMenu(a):
      return hasattr(a,'page_title')

BRMenuListItemProvider = objc.protocolNamed('BRMenuListItemProvider')
class MenuDataSource(NSObject, BRMenuListItemProvider,ControllerUtilities):
    def init(self):
        self._names = [("Item 1",True), 
                       ("Item 2",True), 
                       ("Item 3",False)]
        return NSObject.init(self)

    def initWithController_Menu_(self, ctrlr, menu):
        self.ctrlr = ctrlr
        self.menu = menu
        return self.init()

    def itemCount(self):
        return len(self.menu.items)
  
    def titleForRow_(self,row):
        if row >= len(self.menu.items):
            return None
        if IsMenu(self.menu.items[row]):
              return self.menu.items[row].page_title
        else:
              return self.menu.items[row].title
    
    def itemForRow_(self,row):
        if row >= len(self.menu.items):
            return None

        if IsMenu(self.menu.items[row]):
            if self.menu.items[row].subtitle == "":  
                  result=BRTextMenuItemLayer.folderMenuItem()
                  result.setTitle_(self.menu.items[row].page_title)
            else:
                  # note, this should work but doesn't as the title obscures the subtitle!
                  result=BRTwoLineTextMenuItemLayer.alloc().init()
                  result.setTitle_(self.menu.items[row].page_title) # FIXME: use folder icon!?
                  result.setSubtitle_(self.menu.items[row].subtitle)
        else:
            if self.menu.items[row].subtitle == "":  
                  result=BRTextMenuItemLayer.menuItem()
            else:
                  # note, this should work but doesn't as the title obscures the subtitle!
                  result=BRTwoLineTextMenuItemLayer.alloc().init()
                  result.setSubtitle_(self.menu.items[row].subtitle)
            result.setTitle_(self.menu.items[row].title)
        return result

    def itemSelected_(self, row):
        if IsMenu(self.menu.items[row]):
            con = MenuController.alloc().initWithMenu_(self.menu.items[row])
            self.ctrlr.stack().pushController_(con)
        else:
            self.menu.items[row].Activate(self.ctrlr)

#  should return a preview controller of some type, perhaps
#  BRMetaDataPreviewController BRMetaDataLayer BRMetaDataControl(seems
#  to work for now, but that is really contained in something I
#  haven't identified yet)
    def previewControlForItem_(self, row):
        if IsMenu(self.menu.items[row]):
              return None # fixme: could have metadata func here too!
        else:
              return self.menu.items[row].GetMetadata(self.ctrlr)


    # Dont care aboutr these below.
    def heightForRow_(self,row):
        return 0.0

    def rowSelectable_(self, row):
        return True

class MenuController(BRMediaMenuController,ControllerUtilities):

    def initWithMenu_(self, menu):
        BRMenuController.init(self)
        self.setListTitle_( menu.page_title )
        self.ds = MenuDataSource.alloc().initWithController_Menu_(self,menu)
        self.list().setDatasource_(self.ds)
        return self

    def willBePushed(self):
        self.list().reload()
        return BRMenuController.willBePushed(self)

    def itemSelected_(self, row):
          return self.ds.itemSelected_(row)

    def previewControlForItem_(self, row):
          return self.ds.previewControlForItem_(row)

    def rowSelectable_(self,row):
          return True





