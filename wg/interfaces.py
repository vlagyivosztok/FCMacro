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
    #from wg.controls import Controls
    #import Draft
except:
    print('interfaces import')
    os.system(g_wg_dir+'\import-error.vbs')
    raise Exception("Quit macro / interfaces.py")
#endregion imports

class BackToMain(QtGui.QWidget):
    def __init__(self):
        #print('BackToMain init')
        #super(BackToMain, self).__init__()
        self.loader = QtUiTools.QUiLoader()
        self.file = QtCore.QFile(g_wg_dir+"/BackToMain.ui")
        self.file.open(QtCore.QFile.ReadOnly)
        self.Widget = self.loader.load(self.file)
        self.file.close()
        self.Widget.CB_Back.clicked.connect(self.BackOnClick)
        self.Widget.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.Widget.setWindowFlags(self.Widget.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)

    def get_MainWidget(self,obj_):
        self.obj_MainWidget = obj_

    def BackOnClick(self):
        self.obj_MainWidget.Show_()

    def Show_(self):
        if self.obj_MainWidget.isVisible():
            self.obj_MainWidget.hide()    
        self.Widget.show()

class MainWidget(QtGui.QMainWindow):
    def __init__(self):
        pass
        super(MainWidget, self).__init__()
        #print('MainWidget init')
        #self.loader = QtUiTools.QUiLoader()
        self.file = QtCore.QFile(g_wg_dir+"/MainDialog.ui")
        self.file.open(QtCore.QFile.ReadOnly)
        #self.Widget = self.loader.load(self.file)
        self.file.close()
          
        self.ui=QtUiTools.QUiLoader().load(self.file)
        self.setCentralWidget(self.ui)

        #print(type(self))

        ''' class Form(QtWidgets.QMainWindow):
        def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        self.ui=QtUiTools.QUiLoader().load(ui_file)
        self.setCentralWidget(self.ui) '''

        self.do_events = True

        self.dim_values =   {'Gr':0,    #dictionary
                            'Sp_2_D1':0.0,
                            'Sp_2_D2':0.0,
                            'Sp_2_D3':0.0,
                            'Sp_2_D4':0.0,
                            'Sp_2_D5':0.0,
                            'Sp_2_D6':0.0,
                            'Sp_2_D7':0.0,
                            'Sp_2_D8':0.0,
                            'Sp_2_D9':0.0
                            }
        
        #self.dim_selected = {'Gr':0,'Sp_2_D1':0,'Sp_2_D2':0,'Sp_2_D3':0,'Sp_2_D4':0,'Sp_2_D5':0,'Sp_2_D6':0,'Sp_2_D7':0,'Sp_2_D8':0,'Sp_2_D9':0}
        #("background:QColor(255,255,224)")
        #lightgreen 90 EE 90 144,238,144
        #red
        #Lightyellow FF FF E0 255,255,224
        #print(dir(self))

        self.Font = self.ui.Sp_1_Di.font()  #reset font type
        #print(dir(self.Font))
        self.Font.setBold(True)
        #self.Widget.closeEvent.connect(self.closeEvent)
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/1st-step-q.jpg")
        self.ui.S1_L1.setPixmap(self.pixmap)

        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-1_prev.jpg")
        self.ui.L_Groove1.setPixmap(self.pixmap)
 
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-2_prev.jpg")
        self.ui.L_Groove2.setPixmap(self.pixmap)

        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-2_prev.jpg")
        self.ui.L_Groove3.setPixmap(self.pixmap)

        self.ui.Sp_1_Di.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_1_T.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_1_Do.setStyleSheet("background:rgb(255,255,224)")
        
        self.ui.Cb_1_GtFc.clicked.connect(self.GtFc_onClick)
        self.ui.Cb_2_GtFc.clicked.connect(self.GtFc_onClick)
        self.ui.Cb_3_GtFc.clicked.connect(self.GtFc_onClick)                                

        self.ui.Rb_Groove1.clicked.connect(self.Rb_Groove1_onClick)
        self.ui.Rb_Groove2.clicked.connect(self.Rb_Groove2_onClick)
        self.ui.Rb_Groove3.clicked.connect(self.Rb_Groove3_onClick)

        self.ui.Sp_2_D1.valueChanged.connect(lambda: self.value_insert("Sp_2_D1"))
        self.ui.Sp_2_D2.valueChanged.connect(lambda: self.value_insert("Sp_2_D2"))
        self.ui.Sp_2_D3.valueChanged.connect(lambda: self.value_insert("Sp_2_D3"))
        self.ui.Sp_2_D4.valueChanged.connect(lambda: self.value_insert("Sp_2_D4"))
        self.ui.Sp_2_D5.valueChanged.connect(lambda: self.value_insert("Sp_2_D5"))
        self.ui.Sp_2_D6.valueChanged.connect(lambda: self.value_insert("Sp_2_D6"))
        self.ui.Sp_2_D7.valueChanged.connect(lambda: self.value_insert("Sp_2_D7"))
        self.ui.Sp_2_D8.valueChanged.connect(lambda: self.value_insert("Sp_2_D8"))
        self.ui.Sp_2_D9.valueChanged.connect(lambda: self.value_insert("Sp_2_D9"))

        self.ui.Sp_2_D1.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D2.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D3.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D4.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D5.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D6.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D7.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D8.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D9.setStyleSheet("background:rgb(255,255,224)")      

        self.ui.L_2_D1.setHidden(True)
        self.ui.L_2_D2.setHidden(True)
        self.ui.L_2_D3.setHidden(True)
        self.ui.L_2_D4.setHidden(True)
        self.ui.L_2_D5.setHidden(True)
        self.ui.L_2_D6.setHidden(True)
        self.ui.L_2_D7.setHidden(True)
        self.ui.L_2_D8.setHidden(True)
        self.ui.L_2_D9.setHidden(True)

        self.ui.Sp_2_D1.setHidden(True)
        self.ui.Sp_2_D2.setHidden(True)
        self.ui.Sp_2_D3.setHidden(True)
        self.ui.Sp_2_D4.setHidden(True)
        self.ui.Sp_2_D5.setHidden(True)
        self.ui.Sp_2_D6.setHidden(True)
        self.ui.Sp_2_D7.setHidden(True)
        self.ui.Sp_2_D8.setHidden(True)
        self.ui.Sp_2_D9.setHidden(True)

        #show a mainbol, Show_ val
        #self.ui.show()
        		#non modal	
        #self.exec_()	#modal
        #print(self.ui.CB_Back.Name)


    def closeEvent(self, e):
        res = QtGui.QMessageBox.question(None,"Close","Do you want to close the window?",QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        if res is QtGui.QMessageBox.No:
            e.ignore()


    def get_BackToMain(self,obj_):
        self.obj_BackToMain = obj_

    def GtFc_onClick(self):
        self.obj_BackToMain.Show_()

    def Show_(self):
        if self.obj_BackToMain.Widget.isVisible():
            self.obj_BackToMain.Widget.hide()    
        #self.ui.show()
        self.show()

#        self.ui.Sp_1_Di.setStyleSheet("background-color: red") ("background:QColor(255,255,224)")
    def Test(self):
        print('Di  ',self.ui.Sp_1_Di.font())
        print('Do  ',self.ui.Sp_1_Do.font())
        self.ui.Sp_1_Di.setStyleSheet("")
        self.ui.Sp_1_Di.setFont(self.Font)


    def get_globals(self, dim_selected):
        self.dim_selected = dim_selected
   
    
    def Rb_Groove1_onClick(self):
        self.ui.Rb_Groove1.setChecked(True)
        self.ui.Rb_Groove2.setChecked(False)
        self.ui.Rb_Groove3.setChecked(False)
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove1.jpg")
        self.ui.S2_L1.setPixmap(self.pixmap)
        self.dim_values ['Gr'] = 1

        self.ui.L_2_D1.setText("H1")
        self.ui.L_2_D2.setText("H2")
        self.ui.L_2_D3.setText("H3")
        self.ui.L_2_D4.setText("H4")
        self.ui.L_2_D6.setText("B1")
        self.ui.L_2_D7.setText("B2")
        self.ui.L_2_D8.setText("R")
        self.ui.L_2_D9.setText("D")

        self.ui.L_2_D1.setHidden(False)
        self.ui.L_2_D2.setHidden(False)
        self.ui.L_2_D3.setHidden(False)
        self.ui.L_2_D4.setHidden(False)
        self.ui.L_2_D5.setHidden(True)
        self.ui.L_2_D6.setHidden(False)
        self.ui.L_2_D7.setHidden(False)
        self.ui.L_2_D8.setHidden(False)
        self.ui.L_2_D9.setHidden(False)        

        self.ui.Sp_2_D1.setHidden(False)
        self.ui.Sp_2_D2.setHidden(False)
        self.ui.Sp_2_D3.setHidden(False)
        self.ui.Sp_2_D4.setHidden(False)
        self.ui.Sp_2_D5.setHidden(True)
        self.ui.Sp_2_D6.setHidden(False)
        self.ui.Sp_2_D7.setHidden(False)
        self.ui.Sp_2_D8.setHidden(False)
        self.ui.Sp_2_D9.setHidden(False)        

    def Rb_Groove2_onClick(self):
        self.ui.Rb_Groove1.setChecked(False)
        self.ui.Rb_Groove2.setChecked(True)
        self.ui.Rb_Groove3.setChecked(False)
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove2.jpg")
        self.ui.S2_L1.setPixmap(self.pixmap)
        self.dim_values ['Gr'] = 2

        self.ui.L_2_D1.setText("H1")
        self.ui.L_2_D2.setText("H2")
        self.ui.L_2_D3.setText("H3")
        self.ui.L_2_D4.setText("H4")
        self.ui.L_2_D5.setText("B1")
        self.ui.L_2_D6.setText("B2")
        self.ui.L_2_D7.setText("B3")
        self.ui.L_2_D8.setText("B4")
        self.ui.L_2_D9.setText("R")

        self.ui.L_2_D1.setHidden(False)
        self.ui.L_2_D2.setHidden(False)
        self.ui.L_2_D3.setHidden(False)
        self.ui.L_2_D4.setHidden(False)
        self.ui.L_2_D5.setHidden(False)
        self.ui.L_2_D6.setHidden(False)
        self.ui.L_2_D7.setHidden(False)
        self.ui.L_2_D8.setHidden(False)
        self.ui.L_2_D9.setHidden(False)        

        self.ui.Sp_2_D1.setHidden(False)
        self.ui.Sp_2_D2.setHidden(False)
        self.ui.Sp_2_D3.setHidden(False)
        self.ui.Sp_2_D4.setHidden(False)
        self.ui.Sp_2_D5.setHidden(False)
        self.ui.Sp_2_D6.setHidden(False)
        self.ui.Sp_2_D7.setHidden(False)
        self.ui.Sp_2_D8.setHidden(False)
        self.ui.Sp_2_D9.setHidden(False)                

    def Rb_Groove3_onClick(self):
        self.ui.Rb_Groove1.setChecked(False)
        self.ui.Rb_Groove2.setChecked(False)
        self.ui.Rb_Groove3.setChecked(True)
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/1st-step-q.jpg")
        self.ui.S2_L1.setPixmap(None)
        self.dim_values ['Gr'] = 3        

        self.ui.L_2_D1.setHidden(True)
        self.ui.L_2_D2.setHidden(True)
        self.ui.L_2_D3.setHidden(True)
        self.ui.L_2_D4.setHidden(True)
        self.ui.L_2_D5.setHidden(True)
        self.ui.L_2_D6.setHidden(True)
        self.ui.L_2_D7.setHidden(True)
        self.ui.L_2_D8.setHidden(True)
        self.ui.L_2_D9.setHidden(True)

        self.ui.Sp_2_D1.setHidden(True)
        self.ui.Sp_2_D2.setHidden(True)
        self.ui.Sp_2_D3.setHidden(True)
        self.ui.Sp_2_D4.setHidden(True)
        self.ui.Sp_2_D5.setHidden(True)
        self.ui.Sp_2_D6.setHidden(True)
        self.ui.Sp_2_D7.setHidden(True)
        self.ui.Sp_2_D8.setHidden(True)
        self.ui.Sp_2_D9.setHidden(True)

    def value_insert(self, DblSpb):
        #print(DblSpb, getattr(self.ui,DblSpb).value() ,self.dim_values['Gr'])
        if self.do_events:
            if self.dim_values['Gr'] == 1:
                self.corr_Gr1(DblSpb)
            elif self.dim_values['Gr'] == 2:
                pass
            elif self.dim_values['Gr'] == 3:
                pass        



        #dim_values['Gr'] fuggvenyeben az osszefuggesek szerint korrigalni.


        #self.dim_values [a] = getattr(self.ui,a).value()
        #print(self.dim_values)
        #print(dim_values [a])
        #print(self.ui.__name__())
        #print(type(self))
        #print(type(self.ui))
        #print (dir(self.ui))

#self.ui.Sp_2_D1.setStyleSheet("background:rgb(255,255,224)") lightgreen 90 EE 90 144,238,144 ("background-color: red")

    def corr_Gr1(self, DblSpb):
        self.do_events = False
        #print('corr_Gr1', DblSpb)
        if DblSpb == 'Sp_2_D3' and self.ui.Sp_2_D3.value() > 0: 
            print('corr: Sp_2_D3')
            self.ui.Sp_2_D4.setValue(self.ui.Sp_2_D3.value() + self.ui.Sp_2_D8.value())
            self.dim_values['Sp_2_D4'] = self.ui.Sp_2_D4.value()

        if DblSpb == 'Sp_2_D8' and self.ui.Sp_2_D8.value() > 0:
            self.ui.Sp_2_D9.setValue(self.ui.Sp_2_D8.value()*2)
            self.dim_values['Sp_2_D9'] = self.ui.Sp_2_D9.value()
            print(self.ui.Sp_2_D8.font())
            print(self.Font.Bold)
            self.ui.Sp_2_D8.setStyleSheet("background:rgb(144,238,144)")
            self.ui.Sp_2_D9.setStyleSheet("background:rgb(144,238,144)")
            self.ui.Sp_2_D8.setFont(self.Font) #setWeight(QFont::Bold)
            self.ui.Sp_2_D8.Weight.setBold(True)
            print(type(self.Font))
            self.ui.Sp_2_D9.setFont(self.Font)            

        if DblSpb == 'Sp_2_D9' and self.ui.Sp_2_D9.value() > 0:
            self.ui.Sp_2_D8.setValue(self.ui.Sp_2_D9.value()/2)
            self.dim_values['Sp_2_D8'] = self.ui.Sp_2_D8.value()
            self.ui.Sp_2_D8.setStyleSheet("background:rgb(144,238,144)")
            self.ui.Sp_2_D9.setStyleSheet("background:rgb(144,238,144)")

        self.ui.Sp_2_D3.setValue(self.ui.Sp_2_D4.value() + self.ui.Sp_2_D9.value())
        self.dim_values['Sp_2_D3'] = self.ui.Sp_2_D3.value()

        self.do_events = True
        """ self.ui.L_2_D1.setText("H1")
        self.ui.L_2_D2.setText("H2")
        self.ui.L_2_D3.setText("H3")
        self.ui.L_2_D4.setText("H4")
        self.ui.L_2_D6.setText("B1")
        self.ui.L_2_D7.setText("B2")
        self.ui.L_2_D8.setText("R")
        self.ui.L_2_D9.setText("D") """    

    def corr_Gr2(self):
        pass
    
    def corr_Gr3(self):
        pass
 