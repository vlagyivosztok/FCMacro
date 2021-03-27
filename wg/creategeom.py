#region globals
import FreeCAD as App
g_UserMacroDir = (App.getUserMacroDir()).replace('\\','/')
g_wg_dir = g_UserMacroDir+"wg"
#endregion globals

#region imports
import os
try:
    import sys
    #import site
    #import inspect
    #from operator import xor
    #from PySide import QtGui #QWidget
    #from PySide import QtUiTools #QUiLoader
    #from PySide import QtCore #QFile, Qt
    from math import sqrt
    from pyquaternion import Quaternion
    from shapely.geometry import Point, Polygon
except:
    os.system(g_wg_dir+'\import-error.vbs')
    raise Exception("Quit macro / creategeom.py")
#endregion imports


class CreateGeom():
    '''
    huzalelrendezes Gr1, Gr2
    1. groove-nak megfelelo FCSTD megnyitasa
    2. meretek atadasa a modellnek
    3. Body elhelyezese a horony kozeppontjaban
    4. horony kontur lekerdezese osztopontokkal
    5. korok poziciojanak elkeszitese
    6. korok elkeszitese, konturpontok vizsgalata, hogy belul van-e

      '''
    
    def __init__(self):
        #print('WiresInGroove init')

        self.obj_MainWidget = None

    def create2D(self):
        pass


    def dummy(self):
        print('dbg','WiresInGroove dummy',self.obj_MainWidget.GeomInput)
