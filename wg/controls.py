# -*- coding: utf-8 -*-

#region globals
import FreeCAD as App
g_UserMacroDir = (App.getUserMacroDir()).replace('\\','/')
g_wg_dir = g_UserMacroDir+"wg"
#endregion globals


#region imports
import os
try:
    import sys
    import site
    import inspect
    from importlib import import_module
    from math import sqrt
    from distutils.sysconfig import get_python_lib
    from shapely.geometry import Point, Polygon
    from pyquaternion import Quaternion #inspect.isclass(Quaternion)
    from PySide import QtGui #QWidget
    from PySide import QtUiTools #QUiLoader
    from PySide import QtCore #QFile
    #import Draft
except:
    os.system(g_wg_dir+'\import-error.vbs')
    raise Exception("Quit macro / interfaces.py")
#endregion imports

class Controls():
    def __init__(self):
        print('Controls init')
        #print(self.dim_selected)

    # meg a nem class-bol jon
    def show_(self, to_show, to_hide):
        to_hide.Hide_()
        to_show.Show_()

    def get_object(self,obj_):
        self.obj_ = obj_
        print(obj_.__name__(), dir(obj_))
    ''' def show_BackToMain(self):
        MyMainWidget.Hide_()
        BackToMain.Show_


    #region functions
    def show_BackToMain():
        pass

    def show_Main():
        MyBackToMain
        MyMainWidget.Show_() '''