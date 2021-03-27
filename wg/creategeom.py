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
    App.open(u"D:/_EGYETEMI/DIPLOMA/OpenCASCADE/16.FCStd")

    App.ActiveDocument.getObjectsByLabel("StatCore0")[0].setDatum("Di",9)
    App.ActiveDocument.getObjectsByLabel("StatCore0")[0].setDatum("T",9)


    {'accepted': True, 'groove': 'Gr1', 'tab1': {'values': {'Di': 10.0, 'T': 10.0, 'Do': 10.0, 'L': 10.0}, 'accepted': True},
    'tab2': {'values': {'H1': 10.0, 'H2': 10.0, 'H3': 10.0, 'H4': 10.0, 'B1': 10.0, 'B2': 10.0, 'R': 10.0, 'D': 10.0}, 'accepted': True},
    'tab3': {'values': {'It': 1.0, 'Wd': 1.0, 'Wdo': 1.0, 'G': 1.0}, 'accepted': True},
    'tab4': {'values': {}, 'accepted': False}}

      '''
    
    def __init__(self):
        #print('WiresInGroove init')
        self.FcSTD = ''
        self.tab1 = {}
        self.tab2 = {}
        self.tab3 = {}

        #tab2Gr1: {'H1': D1, 'H2': D2, 'H3': D3, 'H4': D4, 'B1': D6, 'B2': D7, 'R': D8, 'D': D9}
        #tab2Gr2: ['H1' D1,'H2' D2, 'H3' D3 ,'H4' D4 ,'B1' D5 ,'B2' D6 ,'B3' D7 ,'B4' D8 ,'R' D9]

        self.obj_MainWidget = None

    def create2D(self):
        #ertekek atvetele self.obj_MainWidget.GeomInput-bol
        #rint('dbg','WiresInGroove dummy',self.obj_MainWidget.GeomInput)
        self.FcSTD = g_wg_dir+'\\'+self.obj_MainWidget.GeomInput['groove']+'.FCSTD'
        self.tab1 = self.obj_MainWidget.GeomInput['tab1']
        self.tab2 = self.obj_MainWidget.GeomInput['tab2']
        self.tab3 = self.obj_MainWidget.GeomInput['tab3']

        if App.ActiveDocument == None:
            App.open(self.FcSTD)
            for key in ['Di','T']:
                #rint(key,(self.tab1['values'])[key]) 
                App.ActiveDocument.getObjectsByLabel("StatCore0")[0].setDatum(key,(self.tab1['values'])[key])
        else:
            print('dbg, open: ',App.ActiveDocument.Name)            

        if self.obj_MainWidget.GeomInput['groove'] == 'Gr1':
            for key in ['B1','B2','H1','H2','H3','D']:
                App.ActiveDocument.getObjectsByLabel("Sketch005")[0].setDatum(key,(self.tab2['values'])[key])

        if self.obj_MainWidget.GeomInput['groove'] == 'Gr2':
            for key in ['B1','B2','H1','H2','H3','D']:
                App.ActiveDocument.getObjectsByLabel("Sketch005")[0].setDatum(key,(self.tab2['values'])[key])        

        if self.obj_MainWidget.GeomInput['groove'] == 'Gr3':
            print('Gr3 not implemented yet')        
        
        
        App.ActiveDocument.recompute()
        self.obj_MainWidget.ui.Cb_4_CreatArrang.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
        self.obj_MainWidget.ui.Cb_4_CreatGeom.setEnabled(True)

    def dummy(self):
        print('dbg','WiresInGroove dummy',self.obj_MainWidget.GeomInput)
