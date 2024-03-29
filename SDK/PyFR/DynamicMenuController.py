import objc
import Foundation
import AppKit

from BackRow import *
from Utilities import ControllerUtilities

# in individual menu item with text, a function to be called when activated, and an optionional argument to be passed to the function
class DynamicMenuItem(ControllerUtilities):
      def __init__(self,title,func,arg=None,metadata_func=None,folder=False):
            self.title=title
            self.func=func
            self.arg=arg
            self.metadata_func=metadata_func
            self.folder = folder

      def Activate(self, controller):
            #self.log("In activate for menu item %s" % self.title)
            self.func(controller, self)

      def GetMetadata(self, controller):
            #self.log("In GetMetadata for menu item %s" % self.title)
            if self.metadata_func is not None:
                  return self.metadata_func(controller, self.arg)
            else:
                  return None
            
# simple container class for a menu, elements of the items list may contain menu items or another Menu instance for submenus
class DynamicMenu(ControllerUtilities):
      def __init__(self,page_title,items=[],metadata_func=None):
          self.page_title=page_title
          self.items=items
          self.metadata_func=metadata_func
          
      def AddItem(self,item):
          self.items.append(item)

      def GetRightText(self):
            return ""

      def GetMetadata(self, controller):
            self.log("In GetMetadata for menu  %s" % self.page_title.encode("ascii","replace"))
            if self.metadata_func is not None:
                  return self.metadata_func(controller, self.page_title)
            else:
                  return None

BRMenuListItemProvider = objc.protocolNamed('BRMenuListItemProvider')
class DynamicMenuDataSource(NSObject, BRMenuListItemProvider,ControllerUtilities):

      def initWithController_Menu_(self, ctrlr, menu):
            self.ctrlr = ctrlr
            self.menu = menu
            return self.init()
      
      def itemCount(self):
            return len(self.menu.items)

      def titleForRow_(self,row):
            if row >= len(self.menu.items):
                  return None
            return self.menu.items[row].title
    
      def itemForRow_(self,row):
            #self.log("Called itemForRow %d" % row)
            if row >= len(self.menu.items):
                  return None

            if self.menu.items[row].folder:
                  result=BRTextMenuItemLayer.folderMenuItem()
            else:
                  result=BRTextMenuItemLayer.menuItem()

            result.setTitle_(self.menu.items[row].title)
            return result

      def itemSelected_(self, row):
            if row >= len(self.menu.items):
                  return 

            self.menu.items[row].Activate(self.ctrlr)

      #  return a preview controller of some type, perhaps BRMetaDataPreviewController
      #  see PyeTV source for example!
      def previewControlForItem_(self, row):
            if row >= len(self.menu.items):
                  return None
            if self.menu.items[row].folder:
                  return None # fixme: could have metadata func here too!
            else:
                  return self.menu.items[row].GetMetadata(self.ctrlr)


      def RemoveItem(self,item):
            self.items.remove(item)
            self.refreshControllerForModelUpdate()


    # Dont care about these below.
      def heightForRow_(self,row):
            return 0.0

      def rowSelectable_(self, row):
            return True


class DynamicMenuController(BRMediaMenuController,ControllerUtilities):
    def initWithMenu_(self, menu):
          self=super(DynamicMenuController,self).init()
          if self is None:
                return None
          self.title= menu.page_title 
          self.addLabel_(menu.page_title)
          self.setListTitle_( menu.page_title )
          self.ds = DynamicMenuDataSource.alloc().initWithController_Menu_(self,menu)
          self.list().setDatasource_(self.ds)
          return self

    def willBePushed(self):
          #self.log("Pushing menu page %s,%s" % (self.title,self))
          self.list().reload()
          return BRMenuController.willBePushed(self)

    def willBePopped(self):
          #self.log("popping menu page %s, %s" % (self.title,self))
          return BRMenuController.willBePopped(self)

    def itemSelected_(self, row):
          return self.ds.itemSelected_(row)

    def previewControlForItem_(self, row):
          return self.ds.previewControlForItem_(row)

    def rowSelectable_(self,row):
          return True






