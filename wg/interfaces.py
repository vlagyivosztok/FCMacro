import FreeCAD as App
g_UserMacroDir = (App.getUserMacroDir()).replace('\\','/')
g_wg_dir = g_UserMacroDir+"wg"


#region imports
import os
try:
    import sys
    from PySide import QtGui
    from PySide import QtUiTools 
    from PySide import QtCore
    from threading import Timer

except:
    os.system(g_wg_dir+'\import-error.vbs')
    raise Exception("Quit macro / interfaces.py")
#endregion imports

class BackToMain(QtGui.QWidget):
    def __init__(self):
        super(BackToMain, self).__init__()
        self.loader = QtUiTools.QUiLoader()
        self.file = QtCore.QFile(g_wg_dir+"/BackToMain.ui")
        self.file.open(QtCore.QFile.ReadOnly)
        self.Widget = self.loader.load(self.file)
        self.file.close()
        self.Widget.CB_Back.clicked.connect(self.BackOnClick)
        self.Widget.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
        self.obj_MainWidget = None

    def BackOnClick(self):
        self.obj_MainWidget.Show_()

    def Show_(self):
        if self.obj_MainWidget.isVisible():
            self.obj_MainWidget.hide()    
        self.Widget.show()

class CheckResults(QtGui.QWidget):
    def __init__(self):
        self.loader = QtUiTools.QUiLoader()
        self.file = QtCore.QFile(g_wg_dir+"/chktext.ui")
        self.file.open(QtCore.QFile.ReadOnly) 
        self.Widget = self.loader.load(self.file)
        self.file.close()
        self.Widget.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
        self.obj_MainWidget = None
        self.Tab = ''

        self.GeomInput = {}
        self.checkOutput = []
        self.checktexts = {}
        self.checklist = {}

        self.checklist['tab1Gr0']=[1,2]
        self.checklist['tab2Gr1']=[11,12,13,14]
        self.checklist['tab2Gr2']=[13,14,21,22]
        self.checklist['tab3Gr1']=[31,32]
        self.checklist['tab3Gr2']=[31,33]
        
        self.checktexts[1] ="if ((self.GeomInput['tab1'])['values'])['Di'] < ((self.GeomInput['tab1'])['values'])['T']*2:" \
            "self.checkOutput.append('Check the relation between Di and T!')"
        self.checktexts[2] ="if ((self.GeomInput['tab1'])['values'])['L'] < ((self.GeomInput['tab1'])['values'])['Di']:" \
            'self.checkOutput.append("Check the relation between L and Di!")'
         
        self.checktexts[11] ="if ((self.GeomInput['tab2'])['values'])['B2'] < ((self.GeomInput['tab2'])['values'])['B1']:" \
            "self.checkOutput.append('Check the relation between B1 and B2!')"
        self.checktexts[12] ="if ((self.GeomInput['tab2'])['values'])['D'] < ((self.GeomInput['tab2'])['values'])['B2']:" \
            "self.checkOutput.append('Check the relation between B2 and D!')"
        self.checktexts[13] ="if (((self.GeomInput['tab2'])['values'])['H1']+((self.GeomInput['tab2'])['values'])['H2']) > ((self.GeomInput['tab2'])['values'])['H3']:" \
            "self.checkOutput.append('Check the relation between H1, H2 and H3!')"
       
        self.checktexts[14] ="if 'T' in (self.GeomInput['tab1'])['values']:\n\t" \
                "if ((self.GeomInput['tab1'])['values'])['T'] < ((self.GeomInput['tab2'])['values'])['H4']:" \
                "self.checkOutput.append('Check the relation between T (prev. tab) and H4!')\n" \
                "else:\n\tself.checkOutput.append('Previous tab/tabs are not filled! <T>')\n\t" \
                "self.checkOutput.append('Checking is limited only on given input!')"
        self.checktexts[22] ="if ((self.GeomInput['tab2'])['values'])['B4'] < ((self.GeomInput['tab2'])['values'])['B2']: " \
            "self.checkOutput.append('Check the relation between B2 and B4!')"

        self.checktexts[31] ="if ((self.GeomInput['tab3'])['values'])['It'] > (((self.GeomInput['tab3'])['values'])['Wd'])/2: " \
            "self.checkOutput.append('Check the relation between It and Wd!')"
        
        self.checktexts[32] ="if 'D' in (self.GeomInput['tab2'])['values']:\n\t" \
                "if ((self.GeomInput['tab3'])['values'])['Wd'] > ((self.GeomInput['tab2'])['values'])['D']/5: " \
                "self.checkOutput.append('Check the relation between D (prev. tab) and Wd!')\n" \
                "else: \n\tself.checkOutput.append('Previous tab/tabs are not filled! <D>')\n\t" \
                "self.checkOutput.append('Checking is limited only on given input!')"                
        self.checktexts[33] ="if 'B4' in (self.GeomInput['tab2'])['values']:\n\t" \
                "if ((self.GeomInput['tab3'])['values'])['Wd'] > ((self.GeomInput['tab2'])['values'])['B4']/5:" \
                "self.checkOutput.append('Check the relation between B4 (prev. tab) and Wd!')\n" \
                "else: \n\tself.checkOutput.append('Previous tab/tabs are not filled! <B4>')\n\t" \
                "self.checkOutput.append('Checking is limited only on given input!')"

        self.Widget.Cb_AccAnyway.clicked.connect(self.Accept)
        self.Widget.Cb_BackToValues.clicked.connect(self.Hide_)

    def Init(self):
        ''' Ez az init a mereteket vizsgalo szovegeket hajtja vegre
        es adja ki az eredmenyeket '''
        self.checkOutput = []
        self.Tab = self.obj_MainWidget.MyDataTabs.CurrTab
        self.Gr = self.obj_MainWidget.MyDataTabs.CurrGr
        TabGr =   self.Tab+self.Gr        

        for index in self.checklist[TabGr]:
            if index in self.checktexts:
                exec(self.checktexts[index])

        self.Widget.TB_Chktext.setText('')
        if not len(self.checkOutput):
            self.checkOutput.append ("The values seem to be OK.")
        else:
            self.checkOutput.insert(0,"")
            self.checkOutput.insert(0,"(There are no strict rules. You can accept anyway.)")
            self.checkOutput.insert(0,"Please consider the following comments!")
        for text in self.checkOutput:
            self.Widget.TB_Chktext.append(text)
        self.Widget.show() 

    def Hide_(self):
        self.Widget.hide() 

    def Accept(self):
        ''' GeomInput-ban allitja lap jelzojet elfogadottra es meghivja
        az elfogadott allapoto beallito eljarast '''
        Tab = self.obj_MainWidget.MyDataTabs.CurrTab
        if Tab == 'tab2':
            (self.obj_MainWidget.GeomInput[Tab])['accepted'] = True
            self.obj_MainWidget.ui.Cb_2_AccNext.setEnabled(False)
            self.obj_MainWidget.ui.Cb_2_CreatGroove.setEnabled(True)
            self.obj_MainWidget.valuesAccepted()
        else:
            (self.obj_MainWidget.GeomInput[Tab])['accepted'] = True
        self.Widget.hide()
        self.obj_MainWidget.valuesAccepted()


class MainWidget(QtGui.QMainWindow):
    class DataTabs:
        ''' Adatszerkezet, mely az osszes lapot es azok adatait tarolja, beallitja
        es a vegen atadja '''
        def __init__(self):
            self.parent = None
            self.datatabs =  {}
            for key in ['tab1Gr0','tab2Gr0','tab2Gr1','tab2Gr2','tab3Gr0','tab3Gr1','tab3Gr2','tab4Gr0']:
                self.datatabs[key]= {}
            (self.datatabs['tab1Gr0'])['tabconf']='Gr0'
            (self.datatabs['tab2Gr0'])['tabconf']='Gr0'
            (self.datatabs['tab3Gr0'])['tabconf']='Gr0'
            self.CurrTab = ''   
            self.allTab = ['tab1','tab2','tab3','tab4']
            self.CurrGr = ''
   
        def getTabWidgets(self,tabname,dictname,widgets,labels = None):
            ''' MainWidget __init__ eljarasa ezen keresztul adja at a vezerlo elemeket, megfelelo,
            praktikusan csomagolt adatszerkezetekbe '''
            (self.datatabs[tabname])[dictname]= widgets
            if labels != None and type(widgets) is dict: 
                    (self.datatabs[tabname])['ObjLabels']= dict(zip(labels,widgets.values())) 

        def setCurrTabGr(self,Tab,Gr):
            ''' Az aktualisan kivalasztott tab es groove beallitasa, hogy az adatszerkezet tudja,
            mi az aktualis '''
            if Gr == '':
                self.CurrTab = Tab.objectName()
                if self.CurrTab == 'tab2' or self.CurrTab == 'tab3':
                    RbList = [self.parent.ui.Gr1,self.parent.ui.Gr2]
                    self.CurrGr = ''                
                    for Rb in RbList:
                        if Rb.isChecked() :
                            self.CurrGr = 'Gr'+str((RbList.index(Rb))+1)
                    if self.CurrGr == '':
                        self.CurrGr = 'Gr0'
                else:
                    self.CurrGr = 'Gr0'
            else:
                self.CurrGr = Gr.objectName()
            if self.CurrGr != 'Gr0':
                self.WidgetVisib()

        def WidgetVisib(self):
            ''' A valtozo darabszamu szukseges ertekbado widgeteket allitja be szukseg szerint.
            A spinboxok lathatosagat viszi at a labelekre '''
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames']):
                (self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'][key].setHidden(False)
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels']):
                widgetL = ((((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]).objectName()).replace('Sp','L')
                self.parent.ui.findChild(QtGui.QLabel, widgetL).setText(key)
                self.parent.ui.findChild(QtGui.QLabel, widgetL).setHidden(False)
            if 'ObjHide' in (self.datatabs[self.CurrTab+self.CurrGr]):
                for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjHide']):
                    self.parent.ui.findChild(QtGui.QDoubleSpinBox, key).setHidden(True)
                    widgetL = ((((self.datatabs[self.CurrTab+self.CurrGr])['ObjHide'])[key]).objectName()).replace('Sp','L')
                    self.parent.ui.findChild(QtGui.QLabel, widgetL).setHidden(True)

        def resetEnabled(self):
            ''' tabon torteno visszafele haladas es ertek beadas utan az utana levo minden, mar elfogadott
            erteket nem elfogadottra allit: szinek, aktiv-inaktiv allapot '''
            self.parent.GeomInput['accepted'] =False
            self.parent.ui.tabWidget.setTabEnabled(3, False)  
            self.parent.ui.Cb_4_CreatArrang.setStyleSheet("background:rgb(255,255,224);font: bold 12px") #utolso lap gombja sarga
            self.parent.ui.L2_Message.setText('Message:')
            self.parent.ui.L4_Message1.setText('Message:')
            self.parent.ui.L4_Message2.setText('Message:')
            self.parent.ui.Cb_4_CreatGeom.setEnabled(False)
            
            next_ = False
            for key in ['tab1','tab2','tab3']:
                if (next_ or self.CurrTab == key):
                    next_ = True
                    (self.parent.GeomInput[key])['accepted'] =False
                    (self.parent.GeomInput[key])['checkGr'] =False
                    self.setgreen(key)
                    if key == 'tab2':
                        self.parent.ui.Cb_2_CreatGroove.setStyleSheet("background:rgb(255,255,224);font: bold 12px")
                        self.parent.ui.Cb_2_CreatGroove.setEnabled(False)

        def setgreen(self, Tab):
            ''' spinboxok szinet az ertek alapjan allitja be. !=0: zold '''
            for widget in (self.datatabs[Tab+'Gr0'])['ObjNames'].values():
                if widget.value() != 0:
                    widget.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
            self.AccNextEnable(Tab)      
        
        def checkZeros(self,TabGr, _obj= None):
            ''' beadaskor ellenorzi, hogy nulla lett-e beadva es pirosra allit.
            Ha egy sem nulla, akkor tovabengedi a vezerlest '''
            if _obj != None:
                if _obj.value() == 0.0:
                    _obj.setStyleSheet("background-color:red;font: bold 12px")
                    return False    
            checkvalues = 0
            sum_obj = 0
            if TabGr == '' and _obj != None: 
                TabGr = self.CurrTab+self.CurrGr
            for widget in ((self.datatabs[TabGr])['ObjNames'].values()):
                sum_obj += 1
                if widget.value() != 0.0:
                    checkvalues += 1
                    widget.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
            if checkvalues == sum_obj:
                return True
            else:
                return False

        def AccNextEnable(self,Tab ='', _obj= None) :
            ''' aktivalja az Acc/Next gombot '''
            if Tab == '':
                tabGr = self.CurrTab+self.CurrGr
            else:      
                tabGr = Tab + (self.datatabs[Tab+'Gr0'])['tabconf']
            if self.checkZeros(tabGr, _obj):  
                if 'ObjContr' in self.datatabs[tabGr]:
                    for widget in ((self.datatabs[tabGr])['ObjContr'].values()):
                        widget.setEnabled(True)
            else:
                if 'ObjContr' in self.datatabs[tabGr]:
                    for widget in ((self.datatabs[tabGr])['ObjContr'].values()):
                        widget.setEnabled(False)

        def corr_tabs(self,_obj):
            ''' Az aktualis beadas fuggvenyeben az erintett DblSpB ertekeket aktualizalja.
            itt kenyszeriti ki a geometriai osszefuggesek betartasat
            '''
            self.LabelObjs = {}
            self.ObjLabels = {}
            self.testSeq = []
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels']):
                self.ObjLabels[((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]] = key
                self.LabelObjs[key] = ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]
                if ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key] == _obj:
                    _sender = key

            if (self.CurrTab+self.CurrGr) == 'tab1Gr0':
                if self.ObjLabels[_obj] == 'Di' and self.LabelObjs['Di'].value() > 0:
                    if self.LabelObjs['T'].value() > 0:
                        self.LabelObjs['Do'].setValue(self.LabelObjs['Di'].value()+2*self.LabelObjs['T'].value())
                if self.ObjLabels[_obj] == 'Do'and self.LabelObjs['Do'].value() > 0:
                    if self.LabelObjs['T'].value() > 0 and self.LabelObjs['Do'].value() > self.LabelObjs['T'].value():
                        self.LabelObjs['Di'].setValue(self.LabelObjs['Do'].value()-2*self.LabelObjs['T'].value())
                if self.ObjLabels[_obj] == 'T'and self.LabelObjs['T'].value() > 0:                    
                    if self.LabelObjs['Di'].value() > 0:
                        self.LabelObjs['Do'].setValue(self.LabelObjs['Di'].value()+2*self.LabelObjs['T'].value())                
                    elif self.LabelObjs['Do'].value() > 0 and self.LabelObjs['Do'].value() > self.LabelObjs['T'].value():
                        self.LabelObjs['Di'].setValue(self.LabelObjs['Do'].value()-2*self.LabelObjs['T'].value())

            elif (self.CurrTab+self.CurrGr) == 'tab2Gr1':
                if _sender == 'R':
                    self.testSeq = ['D','RH']
                if _sender == 'D':
                    self.testSeq = ['R','RH']
                if _sender == 'H3':
                    self.testSeq = ['H3R']
                if _sender == 'H4':
                    self.testSeq = ['H4R']
                for test in self.testSeq:
                    if test == 'R':
                        self.LabelObjs['R'].setValue(self.LabelObjs['D'].value()/2)
                    if test == 'D':
                        self.LabelObjs['D'].setValue(self.LabelObjs['R'].value()*2)
                    if test == 'RH':
                        if self.LabelObjs['H3'].value() > 0 and self.LabelObjs['R'].value() > 0:
                              self.LabelObjs['H4'].setValue(self.LabelObjs['H3'].value()+self.LabelObjs['R'].value())
                        elif self.LabelObjs['H4'].value() > 0 and self.LabelObjs['R'].value() > 0 and self.LabelObjs['H4'].value()>self.LabelObjs['R'].value():
                              self.LabelObjs['H3'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['R'].value())                        
                    if test == 'H3R':   
                        if self.LabelObjs['H3'].value() > 0 and self.LabelObjs['R'].value()> 0:
                            self.LabelObjs['H4'].setValue(self.LabelObjs['H3'].value()+self.LabelObjs['R'].value())
                        if self.LabelObjs['H3'].value() > 0 and self.LabelObjs['H4'].value()> 0:
                            if self.LabelObjs['H4'].value() > self.LabelObjs['H3'].value():
                                self.LabelObjs['R'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['H3'].value())
                                self.testSeq.append('D')
                    if test == 'H4R':   
                        if self.LabelObjs['H4'].value() > 0 and self.LabelObjs['R'].value()> 0:
                            if self.LabelObjs['H4'].value() > self.LabelObjs['R'].value():
                                self.LabelObjs['H3'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['R'].value())
                        if self.LabelObjs['H4'].value() > 0 and self.LabelObjs['H3'].value()> 0:
                            if self.LabelObjs['H4'].value() > self.LabelObjs['H3'].value():
                                self.LabelObjs['R'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['H3'].value())
                                self.testSeq.append('D')

            elif (self.CurrTab+self.CurrGr) == 'tab2Gr2':
                if _sender == 'H3':
                    if self.LabelObjs['H3'].value() > 0 and self.LabelObjs['R'].value() > 0:
                        self.LabelObjs['H4'].setValue(self.LabelObjs['H3'].value()+self.LabelObjs['R'].value())
                if _sender == 'H4':
                    control = self.LabelObjs['R'].value()+self.LabelObjs['H1'].value()+self.LabelObjs['H2'].value()
                    if self.LabelObjs['H4'].value() > 0 and self.LabelObjs['R'].value() > 0 and  self.LabelObjs['H4'].value() > control:
                        self.LabelObjs['H3'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['R'].value())
                if _sender == 'B3':
                    if self.LabelObjs['H3'].value() > 0 and self.LabelObjs['R'].value() > 0:
                        self.LabelObjs['B4'].setValue(self.LabelObjs['B3'].value()+self.LabelObjs['R'].value()*2)
                if _sender == 'B4':
                    if self.LabelObjs['B4'].value() > 0 and self.LabelObjs['R'].value() > 0 and  self.LabelObjs['B4'].value() > self.LabelObjs['R'].value()*2:
                        self.LabelObjs['B3'].setValue(self.LabelObjs['B4'].value()-self.LabelObjs['R'].value()*2)
                if _sender == 'R':
                    control = self.LabelObjs['R'].value()+self.LabelObjs['H1'].value()+self.LabelObjs['H2'].value()
                    if self.LabelObjs['B3'].value() > 0 and self.LabelObjs['R'].value() > 0:
                        self.LabelObjs['B4'].setValue(self.LabelObjs['B3'].value()+self.LabelObjs['R'].value()*2)
                    elif self.LabelObjs['B4'].value() > 0 and self.LabelObjs['R'].value() > 0 and  self.LabelObjs['B4'].value() > self.LabelObjs['R'].value()*2:
                        self.LabelObjs['B3'].setValue(self.LabelObjs['B4'].value()-self.LabelObjs['R'].value()*2)                        
                    if self.LabelObjs['H3'].value() > 0 and self.LabelObjs['R'].value() > 0:
                        self.LabelObjs['H4'].setValue(self.LabelObjs['H3'].value()+self.LabelObjs['R'].value())
                    elif self.LabelObjs['H4'].value() > 0 and self.LabelObjs['R'].value() > 0 and  self.LabelObjs['H4'].value() > control:
                        self.LabelObjs['H3'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['R'].value())                                                            
                    

            elif (self.CurrTab+self.CurrGr) == 'tab3Gr1' or (self.CurrTab+self.CurrGr) == 'tab3Gr2': 
                if self.ObjLabels[_obj] == 'It' and self.LabelObjs['It'].value() > 0:
                    if self.LabelObjs['Wd'].value() > 0:
                        self.LabelObjs['Wdo'].setValue(self.LabelObjs['Wd'].value()+self.LabelObjs['It'].value()*2)
                    elif self.LabelObjs['Wdo'].value() > 0 and  self.LabelObjs['Wdo'].value() > self.LabelObjs['It'].value()*2:
                        self.LabelObjs['Wd'].setValue(self.LabelObjs['Wdo'].value()-self.LabelObjs['It'].value()*2)    
                
                if self.ObjLabels[_obj] == 'Wd' and self.LabelObjs['Wd'].value() > 0:
                    if self.LabelObjs['It'].value() > 0:
                        self.LabelObjs['Wdo'].setValue(self.LabelObjs['Wd'].value()+self.LabelObjs['It'].value()*2)
                    elif self.LabelObjs['Wdo'].value() > 0 and self.LabelObjs['Wdo'].value() > self.LabelObjs['Wd'].value():
                        self.LabelObjs['It'].setValue((self.LabelObjs['Wdo'].value()-self.LabelObjs['Wd'].value())/2)

                if self.ObjLabels[_obj] == 'Wdo' and self.LabelObjs['Wdo'].value() > 0:
                    if self.LabelObjs['It'].value() > 0 and self.LabelObjs['Wdo'].value() > self.LabelObjs['It'].value()*2:
                        self.LabelObjs['Wd'].setValue(self.LabelObjs['Wdo'].value()-self.LabelObjs['It'].value()*2)
                    elif self.LabelObjs['Wd'].value() > 0 and self.LabelObjs['Wd'].value() < self.LabelObjs['Wdo'].value():
                        self.LabelObjs['It'].setValue((self.LabelObjs['Wdo'].value()-self.LabelObjs['Wd'].value())/2)                
 
    def __init__(self): #MainWidget
        super(MainWidget, self).__init__()
        self.file = QtCore.QFile(g_wg_dir+"/MainDialog.ui")
        self.file.open(QtCore.QFile.ReadOnly)
        self.ui=QtUiTools.QUiLoader().load(self.file)
        self.file.close()        
        self.setCentralWidget(self.ui)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.MyDataTabs = self.DataTabs()
        self.MyDataTabs.parent = self

        self.obj_BackToMain = None
        self.obj_CheckResults = None
        self.obj_WiresInGroove = None
        self.countOfWires = 0

        tabname = ''        
        _dict = {}

        self.GeomInput = {}
        self.GeomInput['accepted'] = False
        self.GeomInput['groove'] = ''
        for key in ['tab1','tab2','tab3','tab4']:
            self.GeomInput[key] = {}
            self.GeomInput[key] = {'values':{},'accepted':False, 'checkGr': False  }

        self.setWindowTitle("WINDING GEOM FreeCAD extension - - - Operating FreeCAD is disabled - - -")
        #region static images
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/tab1.jpg")
        self.ui.S1_L1.setPixmap(self.pixmap)

        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-1_prev.jpg")
        self.ui.L_Groove1.setPixmap(self.pixmap)
 
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-2_prev.jpg")
        self.ui.L_Groove2.setPixmap(self.pixmap)
        #endregion static images

        #region initial styles
        self.ui.Cb_1_AccNext.setEnabled(False)
        self.ui.Cb_2_AccNext.setEnabled(False)
        self.ui.Cb_2_CreatGroove.setEnabled(False)
        self.ui.Cb_3_AccNext.setEnabled(False)           
        self.ui.Cb_4_CreatGeom.setEnabled(False)

        self.ui.Sp_1_Di.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_1_T.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_1_Do.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_1_L.setStyleSheet("background:rgb(255,255,224)")

        self.ui.Sp_2_D1.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D2.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D3.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D4.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D5.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D6.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D7.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D8.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_2_D9.setStyleSheet("background:rgb(255,255,224)")

        self.ui.Cb_2_CreatGroove.setStyleSheet("background:rgb(255,255,224);font: bold 12px")        

        self.ui.Sp_3_D1.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D2.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D3.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D4.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D5.setStyleSheet("background:rgb(255,255,224)")

        self.ui.Cb_4_CreatArrang.setStyleSheet("background:rgb(255,255,224);font: bold 12px")
        self.ui.Cb_4_CreatGeom.setStyleSheet("background:rgb(255,255,224);font: bold 12px")

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

        self.ui.L_3_D1.setHidden(True)
        self.ui.L_3_D2.setHidden(True)
        self.ui.L_3_D3.setHidden(True)
        self.ui.L_3_D4.setHidden(True)
        self.ui.L_3_D5.setHidden(True)

        self.ui.Sp_3_D1.setHidden(True)
        self.ui.Sp_3_D2.setHidden(True)
        self.ui.Sp_3_D3.setHidden(True)
        self.ui.Sp_3_D4.setHidden(True)
        self.ui.Sp_3_D5.setHidden(True)

        self.ui.L_3_expl.setText('')

        #region send widgets to DataTabs
        tabname = 'tab1Gr0'
        _dict[self.ui.Sp_1_Di.objectName()] = self.ui.Sp_1_Di   #{'D1':}
        _dict[self.ui.Sp_1_T.objectName()] = self.ui.Sp_1_T #{'T':}
        _dict[self.ui.Sp_1_Do.objectName()] = self.ui.Sp_1_Do   #{'Do':}
        _dict[self.ui.Sp_1_L.objectName()] = self.ui.Sp_1_L #{'L':}

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['Di','T','Do','L'])

        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',{self.ui.Cb_1_AccNext.objectName():self.ui.Cb_1_AccNext})

        #tab2Gr_ widgets to dict
        _dict = {}
        tabname = 'tab2Gr0'
        _dict[self.ui.Sp_2_D1.objectName()] = self.ui.Sp_2_D1
        _dict[self.ui.Sp_2_D2.objectName()] = self.ui.Sp_2_D2
        _dict[self.ui.Sp_2_D3.objectName()] = self.ui.Sp_2_D3
        _dict[self.ui.Sp_2_D4.objectName()] = self.ui.Sp_2_D4
        _dict[self.ui.Sp_2_D5.objectName()] = self.ui.Sp_2_D5
        _dict[self.ui.Sp_2_D6.objectName()] = self.ui.Sp_2_D6
        _dict[self.ui.Sp_2_D7.objectName()] = self.ui.Sp_2_D7
        _dict[self.ui.Sp_2_D8.objectName()] = self.ui.Sp_2_D8
        _dict[self.ui.Sp_2_D9.objectName()] = self.ui.Sp_2_D9

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict)

        _dict = {}
        tabname = 'tab2Gr1'
        _dict[self.ui.Sp_2_D1.objectName()] = self.ui.Sp_2_D1
        _dict[self.ui.Sp_2_D2.objectName()] = self.ui.Sp_2_D2
        _dict[self.ui.Sp_2_D3.objectName()] = self.ui.Sp_2_D3
        _dict[self.ui.Sp_2_D4.objectName()] = self.ui.Sp_2_D4
        _dict[self.ui.Sp_2_D6.objectName()] = self.ui.Sp_2_D6
        _dict[self.ui.Sp_2_D7.objectName()] = self.ui.Sp_2_D7
        _dict[self.ui.Sp_2_D8.objectName()] = self.ui.Sp_2_D8
        _dict[self.ui.Sp_2_D9.objectName()] = self.ui.Sp_2_D9

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['H1','H2','H3','H4','B1','B2','R','D'])

        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',{self.ui.Cb_2_AccNext.objectName():self.ui.Cb_2_AccNext})
        self.MyDataTabs.getTabWidgets(tabname,'ObjCheck',{self.ui.Cb_2_CreatGroove.objectName():self.ui.Cb_2_CreatGroove}) 
        
        self.MyDataTabs.getTabWidgets(tabname,'ObjHide',{self.ui.Sp_2_D5.objectName():self.ui.Sp_2_D5} )

        _dict = {}
        tabname = 'tab2Gr2'
        _dict[self.ui.Sp_2_D1.objectName()] = self.ui.Sp_2_D1
        _dict[self.ui.Sp_2_D2.objectName()] = self.ui.Sp_2_D2
        _dict[self.ui.Sp_2_D3.objectName()] = self.ui.Sp_2_D3
        _dict[self.ui.Sp_2_D4.objectName()] = self.ui.Sp_2_D4
        _dict[self.ui.Sp_2_D5.objectName()] = self.ui.Sp_2_D5
        _dict[self.ui.Sp_2_D6.objectName()] = self.ui.Sp_2_D6
        _dict[self.ui.Sp_2_D7.objectName()] = self.ui.Sp_2_D7
        _dict[self.ui.Sp_2_D8.objectName()] = self.ui.Sp_2_D8
        _dict[self.ui.Sp_2_D9.objectName()] = self.ui.Sp_2_D9

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['H1','H2','H3','H4','B1','B2','B3','B4','R'])

        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',{self.ui.Cb_2_AccNext.objectName():self.ui.Cb_2_AccNext})  #Cb_2_CreatGroove
        self.MyDataTabs.getTabWidgets(tabname,'ObjCheck',{self.ui.Cb_2_CreatGroove.objectName():self.ui.Cb_2_CreatGroove})

        #tab3Gr_ widgets to dict
        _dict = {}
        tabname = 'tab3Gr0'
        _dict[self.ui.Sp_3_D1.objectName()] = self.ui.Sp_3_D1
        _dict[self.ui.Sp_3_D2.objectName()] = self.ui.Sp_3_D2
        _dict[self.ui.Sp_3_D3.objectName()] = self.ui.Sp_3_D3
        _dict[self.ui.Sp_3_D4.objectName()] = self.ui.Sp_3_D4
        _dict[self.ui.Sp_3_D5.objectName()] = self.ui.Sp_3_D5
        
        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict)

        _dict = {}
        tabname = 'tab3Gr1'
        _dict[self.ui.Sp_3_D1.objectName()] = self.ui.Sp_3_D1   
        _dict[self.ui.Sp_3_D2.objectName()] = self.ui.Sp_3_D2 
        _dict[self.ui.Sp_3_D3.objectName()] = self.ui.Sp_3_D3
        _dict[self.ui.Sp_3_D4.objectName()] = self.ui.Sp_3_D4   


        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['It','Wd','Wdo','G'])
        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',{self.ui.Cb_3_AccNext.objectName():self.ui.Cb_3_AccNext})
        self.MyDataTabs.getTabWidgets(tabname,'ObjHide',{self.ui.Sp_3_D5.objectName():self.ui.Sp_3_D5} ) 
        
        _dict = {}
        tabname = 'tab3Gr2'
        _dict[self.ui.Sp_3_D1.objectName()] = self.ui.Sp_3_D1   
        _dict[self.ui.Sp_3_D2.objectName()] = self.ui.Sp_3_D2 
        _dict[self.ui.Sp_3_D3.objectName()] = self.ui.Sp_3_D3
        _dict[self.ui.Sp_3_D4.objectName()] = self.ui.Sp_3_D4   
 

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['It','Wd','Wdo','G'])
        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',{self.ui.Cb_3_AccNext.objectName():self.ui.Cb_3_AccNext})
        self.MyDataTabs.getTabWidgets(tabname,'ObjHide',{self.ui.Sp_3_D5.objectName():self.ui.Sp_3_D5} ) 

        #region events
        self.ui.Cb_1_GtFc.clicked.connect(self.GtFc_onClick)
        self.ui.Cb_2_GtFc.clicked.connect(self.GtFc_onClick)
        self.ui.Cb_3_GtFc.clicked.connect(self.GtFc_onClick)
        self.ui.Cb_4_GtFc.clicked.connect(self.GtFc_onClick)

        self.ui.Cb_1_AccNext.clicked.connect(self.AccNext_Clicked)
        self.ui.Cb_2_AccNext.clicked.connect(self.AccNext_Clicked)
        self.ui.Cb_3_AccNext.clicked.connect(self.AccNext_Clicked)       

        self.ui.Gr1.clicked.connect(self.Rb_Groove_onClick)
        self.ui.Gr2.clicked.connect(self.Rb_Groove_onClick)

        self.ui.Cb_1_exitWg.clicked.connect(self.closeEvent)
        self.ui.Cb_2_exitWg.clicked.connect(self.closeEvent)
        self.ui.Cb_3_exitWg.clicked.connect(self.closeEvent)
        self.ui.Cb_4_exitWg.clicked.connect(self.closeEvent)

        self.ui.Cb_2_CreatGroove.clicked.connect(self.createGroove)

        self.ui.Cb_4_CreatArrang.clicked.connect(self.createArrang)
        self.ui.Cb_4_CreatGeom.clicked.connect(self.createGeom)    

        self.ui.tabWidget.currentChanged.connect(self.tabChange)
        self.ui.tabWidget.setTabEnabled(3, False)

        self.ui.Sp_1_Di.installEventFilter(self)
        self.ui.Sp_1_T.installEventFilter(self)
        self.ui.Sp_1_Do.installEventFilter(self)
        self.ui.Sp_1_L.installEventFilter(self)

        self.ui.Sp_2_D1.installEventFilter(self)
        self.ui.Sp_2_D2.installEventFilter(self)
        self.ui.Sp_2_D3.installEventFilter(self)
        self.ui.Sp_2_D4.installEventFilter(self)
        self.ui.Sp_2_D5.installEventFilter(self)
        self.ui.Sp_2_D6.installEventFilter(self)
        self.ui.Sp_2_D7.installEventFilter(self)
        self.ui.Sp_2_D8.installEventFilter(self)
        self.ui.Sp_2_D9.installEventFilter(self)

        self.ui.Sp_3_D1.installEventFilter(self)
        self.ui.Sp_3_D2.installEventFilter(self)
        self.ui.Sp_3_D3.installEventFilter(self)
        self.ui.Sp_3_D4.installEventFilter(self)
        self.ui.Sp_3_D5.installEventFilter(self)        
        #endregion events

        self.MyDataTabs.CurrTab = self.ui.tabWidget.currentWidget().objectName()  
        self.MyDataTabs.CurrGr = 'Gr0'

        self.testvalues()           ##############################################  TESTVALUES
        #rint('dbg',self.GeomInput)        
                      
    def createGroove(self):
        ''' CreateGeom, fajl betoltes, meretek alkalmazasa magra, horonyra
        hiba nelkuli visszateres eseten tovabbengedi a vezerlest '''
        if self.obj_CreateGeom.createGroove():
            self.ui.Cb_2_CreatGroove.setStyleSheet("background:rgb(153, 204, 255);font: bold 12px")
            (self.GeomInput['tab2'])['checkGr'] = True
            self.ui.Cb_2_AccNext.setEnabled(True)
            self.ui.L2_Message.setText('Message: Generating successful...')
        else:
            self.ui.L2_Message.setText('Message: An error occured...\nPlease try another dimensions!')


    def createArrang(self):
        ''' huzal elrendezes a horonyban meghivasa '''
        self.start_createArrang()

    
    def start_createArrang(self):
        ''' CreateGeom-bol eljaras meghivasa, eredmenny alapjan tovabbengedi a vezerlest
        vagy hibauzenet '''
        self.hide()
        resp = self.obj_CreateGeom.createArrang()
        if type(resp) != str:
            if resp:
                self.ui.Cb_4_CreatArrang.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
                self.ui.Cb_4_CreatGeom.setEnabled(True)
                self.ui.L4_Message1.setText('Message: Generating successful... \nCount of wires: '+str(self.countOfWires+1))
            
            else:
                self.ui.L4_Message1.setText('Message: An error occured...\nPlease try another dimensions!')
        self.show()            


    def createGeom(self):
        ''' Geometria elkeszites mgehivasa '''
        self.start_createGeom()


    def start_createGeom(self):
        self.hide()
        resp = self.obj_CreateGeom.createGeom()
        if type(resp) != str:
            if resp:
                self.ui.Cb_4_CreatGeom.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
                self.ui.L4_Message2.setText('Message: Generating successful...\nGeometry could be exported in FreeCAD menu'\
                    '\n->File->Export')

            else:
                self.ui.L4_Message2.setText('Message: An error occured...\nPlease try another dimensions!')
        self.show()

    def closeEvent(self, event):
        ''' kilepesi szandek kezelese '''
        reply = QtGui.QMessageBox.question(self, 'WINDING GEOM', 'Are you sure you want to close WINDING GEOM?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if type(event) != bool:
                event.accept()
            else:
                self.hide()
        else:
            if type(event) != bool:
                event.ignore()

    def eventFilter(self, obj, event):
        ''' beadas utan enter (2fele), vagy widget elhagyasa inditja az ellenorzest '''
        if event.type() == 6:
            if event.key() == 16777220 or event.key() == 16777221:  
                self.valueEntered(obj)
        if event.type() == 9:
            self.valueEntered(obj)
        return False

    def valueEntered(self, obj):
        ''' eventFilter utani vezerlesi szekvencia csomopont '''
        self.MyDataTabs.resetEnabled()
        self.MyDataTabs.corr_tabs(obj)
        self.MyDataTabs.AccNextEnable(self.MyDataTabs.CurrTab, obj)

    def testvalues(self):
        #rint('dbg','MainWidget testvalues')

        if True:
            self.ui.Sp_1_Di.setValue(120)    #----------------------####################### testvalues
            self.ui.Sp_1_T.setValue(30)
            self.ui.Sp_1_Do.setValue(120+2*30)
            self.ui.Sp_1_L.setValue(110)

            ''' self.ui.Sp_2_D1.setValue(1)     #H1
            self.ui.Sp_2_D2.setValue(1)     #H2
            self.ui.Sp_2_D3.setValue(11.5)     #H3
            self.ui.Sp_2_D4.setValue(13.5)     #H4        
            self.ui.Sp_2_D5.setValue(2)     #--     B1
            self.ui.Sp_2_D6.setValue(2)     #B1     B2
            self.ui.Sp_2_D7.setValue(4)     #B2     B3
            self.ui.Sp_2_D8.setValue(3.5)     #R     B4
            self.ui.Sp_2_D9.setValue(7) '''     #D      R """ 

            #Gr2:
            self.ui.Sp_2_D1.setValue(1)     #H1
            self.ui.Sp_2_D2.setValue(1)     #H2
            self.ui.Sp_2_D3.setValue(11.5)     #H3
            self.ui.Sp_2_D4.setValue(13.5)     #H4        
            self.ui.Sp_2_D5.setValue(2)     #--     B1
            self.ui.Sp_2_D6.setValue(4)     #B1     B2
            self.ui.Sp_2_D7.setValue(3)     #B2     B3
            self.ui.Sp_2_D8.setValue(7)     #R     B4
            self.ui.Sp_2_D9.setValue(2)     #D      R '''

            self.ui.Sp_3_D1.setValue(0.1)
            self.ui.Sp_3_D2.setValue(1.2)
            self.ui.Sp_3_D3.setValue(1.4)
            self.ui.Sp_3_D4.setValue(0.1)

        ''' self.GeomInput

        #tab2Gr1: {'H1': D1, 'H2': D2, 'H3': D3, 'H4': D4, 'B1': D6, 'B2': D7, 'R': D8, 'D': D9}
        #tab2Gr2: ['H1' D1,'H2' D2, 'H3' D3 ,'H4' D4 ,'B1' D5 ,'B2' D6 ,'B3' D7 ,'B4' D8 ,'R' D9]

        dbg {'accepted': False, 'groove': '', 'tab1': {'values': {'Di': 10.0, 'T': 10.0, 'Do': 30.0, 'L': 10.0}, 'accepted': False},
        'tab2': {'values': {'H1': 10.0, 'H2': 10.0, 'H3': 10.0, 'H4': 15.0, 'B1': 10.0, 'B2': 10.0, 'R': 5.0, 'D': 10.0}, 'accepted': False},
        'tab3': {'values': {'It': 1.0, 'Wd': 1.0, 'Wdo': 1.0, 'G': 0.1}, 'accepted': True},
        'tab4': {'values': {}, 'accepted': False}} '''
        
        if True:
            self.GeomInput['accepted'] = True
            self.GeomInput['groove'] = 'Gr1'

            self.GeomInput['tab1'] = {'values':{}}
            (self.GeomInput['tab1'])['values'] = {'Di': self.ui.Sp_1_Di.value(),
                                                'T': self.ui.Sp_1_T.value(),
                                                'Do': self.ui.Sp_1_Do.value(),
                                                'L': self.ui.Sp_1_L.value()}
            (self.GeomInput['tab1'])['accepted'] = True

            self.GeomInput['tab2'] = {'values':{}}
            (self.GeomInput['tab2'])['values'] = {'H1': self.ui.Sp_2_D1.value(),
                                                'H2': self.ui.Sp_2_D2.value(),
                                                'H3': self.ui.Sp_2_D3.value(),
                                                'H4': self.ui.Sp_2_D4.value(),
                                                'B1': self.ui.Sp_2_D6.value(),
                                                'B2': self.ui.Sp_2_D7.value(),
                                                'R': self.ui.Sp_2_D8.value(),
                                                'D': self.ui.Sp_2_D9.value()}
            (self.GeomInput['tab2'])['accepted'] = True

            self.GeomInput['tab3'] = {'values':{}}
            (self.GeomInput['tab3'])['values'] = {'It': self.ui.Sp_3_D1.value(),
                                                'Wd': self.ui.Sp_3_D2.value(),
                                                'Wdo': self.ui.Sp_3_D3.value(),
                                                'G': self.ui.Sp_3_D4.value()}
            (self.GeomInput['tab3'])['accepted'] = True
            #self.ui.tabWidget.setCurrentIndex(3)       #Show_ ban van
            self.ui.tabWidget.setTabEnabled(3, True)
            (self.GeomInput['tab2'])['checkGr'] = True                        




    def Show_(self):
        if self.obj_BackToMain.Widget.isVisible():
            self.obj_BackToMain.Widget.hide()
        self.show()



    def GtFc_onClick(self):
        self.obj_BackToMain.Show_()        

    def Rb_Groove_onClick(self):
        ''' A kivalasztott horonyfajta alapjan a tabok, vezerlovaltozok beallitasa '''
        self.ui.Gr1.setChecked(self.sender().objectName()==self.ui.Gr1.objectName())
        self.ui.Gr2.setChecked(self.sender().objectName()==self.ui.Gr2.objectName())
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/"+self.sender().objectName()+".jpg")
        self.ui.S2_L1.setPixmap(self.pixmap)
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/"+self.sender().objectName()+"_3.jpg")
        self.ui.S3_L1.setPixmap(self.pixmap)
        self.MyDataTabs.setCurrTabGr('',self.sender())
        if self.MyDataTabs.CurrGr == 'Gr1' or self.MyDataTabs.CurrGr == 'Gr2':
            self.ui.L_3_expl.setText("Explanation of dimension variables:<br><br>It: insulation thickness<br>Wd: wire diameter <br>" \
                "Wdo: insulated wire outer diameter<br>G: gap between Wdo")
        (self.MyDataTabs.datatabs['tab2Gr0'])['tabconf']=self.MyDataTabs.CurrGr
        (self.MyDataTabs.datatabs['tab3Gr0'])['tabconf']=self.MyDataTabs.CurrGr
        self.MyDataTabs.resetEnabled()
                

    def tabChange(self):
        ''' tab valtasaval vezerlo valtozo beallitasa '''
        self.MyDataTabs.setCurrTabGr(self.sender().currentWidget(),'')


    def AccNext_Clicked(self):
        ''' fontos vezerlesi csomopont '''
        Tab = self.MyDataTabs.CurrTab
        Gr = self.MyDataTabs.CurrGr
        TabGr =   Tab+Gr
        
        if (self.GeomInput[Tab])['accepted']:
            tabindex = self.MyDataTabs.allTab.index(Tab)
            self.ui.tabWidget.setCurrentIndex(tabindex+1)
            self.MyDataTabs.setCurrTabGr(self.ui.tabWidget.currentWidget(),'')
        else:
            for key in (self.MyDataTabs.datatabs[TabGr])['ObjLabels']:
                ((self.GeomInput[Tab])['values'])[key] = (((self.MyDataTabs.datatabs[TabGr])['ObjLabels'])[key]).value()
            self.obj_CheckResults.Init()
    
    def valuesAccepted(self):
        ''' Egy ertekbeadasi kor vege itt van. Valtozok ertekbeallitasa,
        widget allapotok beallitasa '''
        for Widget in (self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames']:
            (((self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames'])[Widget]).setStyleSheet("background:rgb(153, 204, 255);font: bold 12px")
        self.GeomInput['accepted'] = (self.GeomInput['tab1'])['accepted'] and (self.GeomInput['tab2'])['accepted'] and (self.GeomInput['tab3'])['accepted'] \
            and (self.GeomInput['tab2'])['checkGr']
        self.GeomInput['groove'] = self.MyDataTabs.CurrGr
        self.ui.tabWidget.setTabEnabled(3, self.GeomInput['accepted'])
