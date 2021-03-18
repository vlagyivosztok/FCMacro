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
    from operator import xor
    from PySide import QtGui #QWidget
    from PySide import QtUiTools #QUiLoader
    from PySide import QtCore #QFile, Qt
except:
    print('interfaces import')
    os.system(g_wg_dir+'\import-error.vbs')
    raise Exception("Quit macro / interfaces.py")
#endregion imports

class BackToMain(QtGui.QWidget):
    def __init__(self):
        #print('BackToMain init')
        super(BackToMain, self).__init__()
        self.loader = QtUiTools.QUiLoader()
        self.file = QtCore.QFile(g_wg_dir+"/BackToMain.ui")
        self.file.open(QtCore.QFile.ReadOnly)
        self.Widget = self.loader.load(self.file)
        self.file.close()
        self.Widget.CB_Back.clicked.connect(self.BackOnClick)
        self.Widget.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)

        #self.Widget.setWindowFlags(QtCore.Qt.WindowTitleHint)
        #self.Widget.setWindowFlags(self.Widget.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.obj_MainWidget = None

        #self.Widget.show()
    def BackOnClick(self):
        self.obj_MainWidget.Show_()

    def Show_(self):
        if self.obj_MainWidget.isVisible():
            self.obj_MainWidget.hide()    
        self.Widget.show()

class CheckResults(QtGui.QWidget):
    def __init__(self):
        super(CheckResults, self).__init__()
        self.loader = QtUiTools.QUiLoader()
        self.file = QtCore.QFile(g_wg_dir+"/chktext.ui")
        self.file.open(QtCore.QFile.ReadOnly) 
        self.Widget = self.loader.load(self.file)
        self.file.close()
        self.Widget.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
        self.GeomInput =  {}
        self.obj_MainWidget = None
        self.Tab = ''

        #region checktests
        self.GeomInput = {}
        self.checkOutput = []
        #self.checktext = ''
        self.checktexts = {}
        self.checklist = {}

        self.checktexts[1] ="if ((self.GeomInput['tab1'])['values'])['Di'] < ((self.GeomInput['tab1'])['values'])['T']*2: " \
            "self.checkOutput.append('Check the relation between Di and T!')"
        self.checktexts[2] ="if ((self.GeomInput['tab1'])['values'])['L'] < ((self.GeomInput['tab1'])['values'])['Di']: " \
            'self.checkOutput.append("Check the relation between L and Di!")'
         
        self.checktexts[11] ="if ((self.GeomInput['tab2'])['values'])['B2'] < ((self.GeomInput['tab2'])['values'])['B1']: " \
            "self.checkOutput.append('Check the relation between B1 and B2!')"
        self.checktexts[12] ="if ((self.GeomInput['tab2'])['values'])['D'] < ((self.GeomInput['tab2'])['values'])['B2']: " \
            "self.checkOutput.append('Check the relation between B2 and D!')"
        self.checktexts[13] ="if (((self.GeomInput['tab2'])['values'])['H1']+((self.GeomInput['tab2'])['values'])['H2']) > ((self.GeomInput['tab2'])['values'])['H3']: " \
            "self.checkOutput.append('Check the relation between H1, H2 and H3!')"
        self.checktexts[14] ="if ((self.GeomInput['tab1'])['values'])['T'] < ((self.GeomInput['tab2'])['values'])['H4']: " \
            "self.checkOutput.append('Check the relation between T (prev. tab) and H4!')"            

        self.checktexts[21] ="if ((self.GeomInput['tab2'])['values'])['Di'] < ((self.GeomInput['tab2'])['values'])['T']*2: " \
            "self.checkOutput.append('Check the relation between Di and T!')"
        self.checktexts[22] ="if ((self.GeomInput['tab2'])['values'])['B4'] < ((self.GeomInput['tab1'])['values'])['B2']: " \
            "self.checkOutput.append('Check the relation between B2 and B4!')" 
                                              

        #endregion checktests

        #region checklists
        self.checklist['tab1Gr0']=[1,2]
        self.checklist['tab2Gr1']=[11,12,13,14]
        self.checklist['tab2Gr2']=[13,14,21,22]
        self.checklist['tab2Gr3']=[13]
        # endregion checklists           

        self.Widget.Cb_AccAnyway.clicked.connect(self.Accept)
        self.Widget.Cb_BackToValues.clicked.connect(self.Hide_)
        
    def dummy(self):
        print('dummy')
    
    def Init(self):
        self.checkOutput = []
        self.GeomInput = self.obj_MainWidget.GeomInput
        self.Tab = self.obj_MainWidget.MyDataTabs.CurrTab
        self.Gr = self.obj_MainWidget.MyDataTabs.CurrGr
        TabGr =   self.Tab+self.Gr        

        #print('GeomInput',self.GeomInput)
        #self.checklist['tab1Gr0'] list
        #self.checktexts dict
        for index in self.checklist[TabGr]:
            print(index)
            exec(self.checktexts[index])

        #print(((self.GeomInput['tab1'])['values'])['Di'])
        #print(self.checkOutput)
        self.Widget.TB_Chktext.setText('')
        if not len(self.checkOutput):
            self.checkOutput.append ("The values seem to be OK.")
        else:
            self.checkOutput.insert(0,"")
            self.checkOutput.insert(0,"(There are no strict rules. You can accept anyway)")
            self.checkOutput.insert(0,"Please consider the following comments!")
        for text in self.checkOutput:
            self.Widget.TB_Chktext.append(text)
        print(self.checkOutput)
        self.Widget.show() 

    def Hide_(self):
    
        self.Widget.hide() 

    def Accept(self):   #self.GeomInput)
        self.GeomInput = self.obj_MainWidget.GeomInput
        self.Tab = self.obj_MainWidget.MyDataTabs.CurrTab
        (self.obj_MainWidget.GeomInput[self.Tab])['accepted'] = True
        print('accepted:True')
        self.Widget.hide()
        self.obj_MainWidget.valuesAccepted()
        #print(self.obj_MainWidget.GeomInput)

class MainWidget(QtGui.QMainWindow):
    class DataTabs:    #minden tab es az adatai, adatfeldolgozasa, lathatosagok

        def __init__(self):

            self.actStep = ''
            self.stepNr = {}
            self.stepobj = {}
            self.controltext = []
            self.filled = True
            
            self.parent = None
            self.datatabs =  {}

            self.dict = {}
            self.CurrTab = ''
            self.CurrGr = ''
            self._sender =''
            #print(self, 'DataTabs')
            #print(self.CurrTab,self.CurrGr)
            #print(type(self.datatabs))

            """ self.dict
            
            self.datatabs['WidgetLabel']= {}
            self.datatabs['WidgetName']= {} """
            
            #self.datatabs['tab1gr0'] = [{}]
            """ print('datatabs', type(self.datatabs))
            print('WidgetLabel', type(self.datatabs['WidgetLabel']))
            print('WidgetName', type(self.datatabs['WidgetName'])) """
            

      
        def getTab(self,name,widgets,labels): #string, dict
            self.datatabs[name]= {'ObjNames' : widgets, 
            'ObjLabels': (dict(zip(labels,widgets.values())))}

        def getTabControl(self,tabname,dictname,widgets):
            (self.datatabs[tabname])[dictname]= widgets

        def setCurrTabGr(self,Tab,Gr):     #isChecked()
            if Gr == '':
                self.CurrTab = Tab.objectName()
                if self.CurrTab == 'tab2':      # and (TabOrGr.objectName()).find('Gr')>=0:
                    RbList = [self.parent.ui.Gr1,self.parent.ui.Gr2,self.parent.ui.Gr3]
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

        def WidgetVisib(self):  #CurrTab es CurrGr allapotabol beallitja a lathatosagokat
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames']):
                #print('own: ',widget, 'parent: ',self.parent )
                #self.parent.ui.findChild(QtGui.QDoubleSpinBox, widget).setHidden(False)
                (self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'][key].setHidden(False)
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels']):
                widgetL = ((((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]).objectName()).replace('Sp','L')
                self.parent.ui.findChild(QtGui.QLabel, widgetL).setText(key)
                self.parent.ui.findChild(QtGui.QLabel, widgetL).setHidden(False)
                #print((((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'][widget]).objectName()).replace('Sp','L'))
            if 'ObjHide' in (self.datatabs[self.CurrTab+self.CurrGr]):
                for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjHide']):
                    #print('hide: ',widget, 'parent: ',self.parent)
                    self.parent.ui.findChild(QtGui.QDoubleSpinBox, key).setHidden(True)
                    widgetL = ((((self.datatabs[self.CurrTab+self.CurrGr])['ObjHide'])[key]).objectName()).replace('Sp','L')
                    self.parent.ui.findChild(QtGui.QLabel, widgetL).setHidden(True)

        def checkZeros(self, _obj):       #minden egyes valtozas utan ellenorizni, hogy egy sem zero, akkor accNext enabled, plusz a szinezes
            #print('helo', (self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'] )    #[self.CurrTab+self.CurrGr]
            self.checkvalues = 0
            self.sum_obj = 0
            for widget in (((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames']).values()):  #.itervalues()
                self.sum_obj += 1
                if widget == _obj:
                    if _obj.value() == 0.0:
                        _obj.setStyleSheet("background-color:red;font: bold 12px")
                    else:
                        _obj.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
                #print(widget.value()) #, widget.objectName()) #.value()
                if widget.value() != 0.0:
                    self.checkvalues += 1
                    widget.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
            #print(self.checkvalues, self.sum_obj)
            if self.checkvalues == self.sum_obj:
                return True
            else:
                return False
            #print(True)

        def AccNextEnable(self, _obj):
            #print(_obj.objectName()) #sender()
            """ for widget in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjContr'].values()):
                if widget == _obj and _obj.value() == 0.0 """

            if self.checkZeros(_obj):   #lehetne for nelkul is, jelenleg egy widget van benne
                for widget in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjContr'].values()):
                    widget.setEnabled(True)
            else:
                for widget in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjContr'].values()):
                    widget.setEnabled(False)

        def corr_tabs(self,_obj):
            #pass
            self.LabelObjs = {}
            self.ObjLabels = {}
            self.testSeq = []
            #print(_obj)
            #for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames']):
                #self.WidgetNames[key] = ((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'])[key]
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels']):
                self.ObjLabels[((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]] = key
                self.LabelObjs[key] = ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]
                #print(((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key])
                if ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key] == _obj:
                    #print(((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key])
                    #print(((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key],_obj, key )
                    self._sender = key      #Label
            #print(self._sender) #self.ObjLabels, self.LabelObjs, 

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
                if self._sender == 'R':
                    self.testSeq = ['D','RH']
                if self._sender == 'D':
                    self.testSeq = ['R','RH']
                if self._sender == 'H3':
                    self.testSeq = ['H3R']
                if self._sender == 'H4':
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
                if self._sender == 'R':
                    self.testSeq = ['H','B']
                if self._sender.find('H') >= 0:
                    self.testSeq = ['H','B']
                if self._sender.find('B') >= 0:
                    self.testSeq = ['B','H']
                for test in self.testSeq:
                    if test == 'H':
                        if self.LabelObjs['H3'].value() > 0 and self.LabelObjs['R'].value() > 0:
                            self.LabelObjs['H4'].setValue(self.LabelObjs['H3'].value()+self.LabelObjs['R'].value())
                        elif self.LabelObjs['H4'].value() > 0 and self.LabelObjs['R'].value() > 0 and self.LabelObjs['H4'].value()>self.LabelObjs['R'].value():
                            self.LabelObjs['H3'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['R'].value())
                        elif self.LabelObjs['H4'].value() > 0 and self.LabelObjs['H3'].value() > 0 and self.LabelObjs['H4'].value()>self.LabelObjs['H3'].value():
                            self.LabelObjs['R'].setValue(self.LabelObjs['H4'].value()-self.LabelObjs['H3'].value())

                    if test == 'B':                              
                        if self.LabelObjs['B3'].value() > 0 and self.LabelObjs['R'].value() > 0:
                              self.LabelObjs['B4'].setValue(self.LabelObjs['B3'].value()+self.LabelObjs['R'].value()*2)
                        elif self.LabelObjs['B4'].value() > 0 and self.LabelObjs['R'].value() > 0 and self.LabelObjs['B4'].value()>self.LabelObjs['R'].value()*2:
                              self.LabelObjs['B3'].setValue(self.LabelObjs['B4'].value()-self.LabelObjs['R'].value()*2)                                                
                        elif self.LabelObjs['B4'].value() > 0 and self.LabelObjs['B3'].value() > 0 and self.LabelObjs['B4'].value()>self.LabelObjs['B3'].value():
                            self.LabelObjs['R'].setValue((self.LabelObjs['B4'].value()-self.LabelObjs['B3'].value())/2)
                    
            elif (self.CurrTab+self.CurrGr) == 'tab2Gr3':
                pass

    def __init__(self):
        #super(MainWidget, self).__init__()
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.file = QtCore.QFile(g_wg_dir+"/MainDialog.ui")
        self.file.open(QtCore.QFile.ReadOnly)
        self.file.close()
        self.ui=QtUiTools.QUiLoader().load(self.file)
        self.setCentralWidget(self.ui)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        #self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.MyDataTabs = self.DataTabs()
        self.MyDataTabs.parent = self
        #print('parent: ',self.MyDataTabs.parent)
        #region variables
        self.do_events = True
        self.tabname = ''
        self.obj_BackToMain = None
        self.obj_CheckResults = None
        self.dict = {}
        self.currWidget = None 
        #self.tag = ''   #2. mezo, WLabel vagy WName
        self.GeomInput = {}
        for key in ['tab1','tab2','tab3','tab4']:
            self.GeomInput[key] = {}
            self.GeomInput[key] = {'values':{}}

        #region static images
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/tab1.jpg")
        self.ui.S1_L1.setPixmap(self.pixmap)

        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-1_prev.jpg")
        self.ui.L_Groove1.setPixmap(self.pixmap)
 
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-2_prev.jpg")
        self.ui.L_Groove2.setPixmap(self.pixmap)

        self.pixmap = QtGui.QPixmap(g_wg_dir+"/groove-2_prev.jpg")
        self.ui.L_Groove3.setPixmap(self.pixmap)
        #endregion static images

        #region initial styles
        self.ui.Cb_1_AccNext.setEnabled(False)
        self.ui.Cb_2_AccNext.setEnabled(False)
        self.ui.Cb_3_AccNext.setEnabled(False)              #-----------------------------------------------------------------

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


        #MyMainWidget.installEventFilter(MyMainWidget)

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

        self.MyDataTabs.actStep = self.ui.tabWidget.currentWidget().objectName()
        #print(self.MyDataTabs.actStep)
        #endregion intial styles

        #region send widgets to DataTabs
        self.tabname = 'tab1Gr0'
        self.dict[self.ui.Sp_1_Di.objectName()] = self.ui.Sp_1_Di   #{'D1':}
        self.dict[self.ui.Sp_1_T.objectName()] = self.ui.Sp_1_T #{'T':}
        self.dict[self.ui.Sp_1_Do.objectName()] = self.ui.Sp_1_Do   #{'Do':}
        self.dict[self.ui.Sp_1_L.objectName()] = self.ui.Sp_1_L #{'L':}

        self.MyDataTabs.getTab(self.tabname,self.dict,['Di','T','Do','L'])

        #self.dict[self.ui.Cb_1_GtFc.objectName()] = self.ui.Cb_1_GtFc
        #self.dict[self.ui.Cb_1_AccNext.objectName()] = self.ui.Cb_1_AccNext
        #self.dict[self.ui.Cb_1_exitWg.objectName()] = self.ui.Cb_1_exitWg
        self.MyDataTabs.getTabControl(self.tabname,'ObjContr',{self.ui.Cb_1_AccNext.objectName():self.ui.Cb_1_AccNext})

        self.dict = {}
        self.tabname = 'tab2Gr1'
        self.dict[self.ui.Sp_2_D1.objectName()] = self.ui.Sp_2_D1
        self.dict[self.ui.Sp_2_D2.objectName()] = self.ui.Sp_2_D2
        self.dict[self.ui.Sp_2_D3.objectName()] = self.ui.Sp_2_D3
        self.dict[self.ui.Sp_2_D4.objectName()] = self.ui.Sp_2_D4
        self.dict[self.ui.Sp_2_D6.objectName()] = self.ui.Sp_2_D6
        self.dict[self.ui.Sp_2_D7.objectName()] = self.ui.Sp_2_D7
        self.dict[self.ui.Sp_2_D8.objectName()] = self.ui.Sp_2_D8
        self.dict[self.ui.Sp_2_D9.objectName()] = self.ui.Sp_2_D9

        self.MyDataTabs.getTab(self.tabname,self.dict,['H1','H2','H3','H4','B1','B2','R','D'])

        #self.dict[self.ui.Cb_2_GtFc.objectName()] = self.ui.Cb_2_GtFc
        #self.dict[self.ui.Cb_2_AccNext.objectName()] = self.ui.Cb_2_AccNext
        #self.dict[self.ui.Cb_2_exitWg.objectName()] = self.ui.Cb_2_exitWg
        self.MyDataTabs.getTabControl(self.tabname,'ObjContr',{self.ui.Cb_2_AccNext.objectName():self.ui.Cb_2_AccNext}) 
        self.MyDataTabs.getTabControl(self.tabname,'ObjHide',{self.ui.Sp_2_D5.objectName():self.ui.Sp_2_D5} )

        self.dict = {}
        self.tabname = 'tab2Gr2'
        self.dict[self.ui.Sp_2_D1.objectName()] = self.ui.Sp_2_D1
        self.dict[self.ui.Sp_2_D2.objectName()] = self.ui.Sp_2_D2
        self.dict[self.ui.Sp_2_D3.objectName()] = self.ui.Sp_2_D3
        self.dict[self.ui.Sp_2_D4.objectName()] = self.ui.Sp_2_D4
        self.dict[self.ui.Sp_2_D5.objectName()] = self.ui.Sp_2_D5
        self.dict[self.ui.Sp_2_D6.objectName()] = self.ui.Sp_2_D6
        self.dict[self.ui.Sp_2_D7.objectName()] = self.ui.Sp_2_D7
        self.dict[self.ui.Sp_2_D8.objectName()] = self.ui.Sp_2_D8
        self.dict[self.ui.Sp_2_D9.objectName()] = self.ui.Sp_2_D9

        self.MyDataTabs.getTab(self.tabname,self.dict,['H1','H2','H3','H4','B1','B2','B3','B4','R'])
        self.MyDataTabs.getTabControl(self.tabname,'ObjContr',{self.ui.Cb_2_AccNext.objectName():self.ui.Cb_2_AccNext})

        #self.dict[self.ui.Cb_2_GtFc.objectName()] = self.ui.Cb_2_GtFc
        #self.dict[self.ui.Cb_2_AccNext.objectName()] = self.ui.Cb_2_AccNext
        #self.dict[self.ui.Cb_2_exitWg.objectName()] = self.ui.Cb_2_exitWg

        #self.MyDataTabs.getTabControl(self.tabname,{})
        self.dict = {}
        self.tabname = 'tab2Gr3'
        self.dict[self.ui.Sp_2_D1.objectName()] = self.ui.Sp_2_D1
        self.dict[self.ui.Sp_2_D2.objectName()] = self.ui.Sp_2_D2
        self.dict[self.ui.Sp_2_D3.objectName()] = self.ui.Sp_2_D3
        self.dict[self.ui.Sp_2_D4.objectName()] = self.ui.Sp_2_D4
        self.dict[self.ui.Sp_2_D5.objectName()] = self.ui.Sp_2_D5
        self.dict[self.ui.Sp_2_D6.objectName()] = self.ui.Sp_2_D6
        self.dict[self.ui.Sp_2_D7.objectName()] = self.ui.Sp_2_D7
        self.dict[self.ui.Sp_2_D8.objectName()] = self.ui.Sp_2_D8
        self.dict[self.ui.Sp_2_D9.objectName()] = self.ui.Sp_2_D9

        self.MyDataTabs.getTab(self.tabname,self.dict,['H1','H2','H3','H4','B1','B2','B3','B4','R'])
        self.MyDataTabs.getTabControl(self.tabname,'ObjContr',{self.ui.Cb_2_AccNext.objectName():self.ui.Cb_2_AccNext})

        #print(self.MyDataTabs.datatabs)

        #endregion send widgets              

        #region events
        self.ui.Cb_1_GtFc.clicked.connect(self.GtFc_onClick)
        self.ui.Cb_2_GtFc.clicked.connect(self.GtFc_onClick)
        self.ui.Cb_3_GtFc.clicked.connect(self.GtFc_onClick)

        self.ui.Cb_1_AccNext.clicked.connect(self.AccNext_Clicked)
        self.ui.Cb_2_AccNext.clicked.connect(self.AccNext_Clicked)
        self.ui.Cb_3_AccNext.clicked.connect(self.AccNext_Clicked)       

        self.ui.Gr1.clicked.connect(self.Rb_Groove_onClick)
        self.ui.Gr2.clicked.connect(self.Rb_Groove_onClick)
        self.ui.Gr3.clicked.connect(self.Rb_Groove_onClick)        

        self.ui.tabWidget.currentChanged.connect(self.tabChange)

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

        #endregion events

        self.MyDataTabs.CurrTab = self.ui.tabWidget.currentWidget().objectName()    #kezdoallapot beallitasa
        self.MyDataTabs.CurrGr = 'Gr0'
        #print('tabwidget', self.ui.tabWidget.currentWidget().objectName())
              
    def test(self):
        print(self.sender())

    def eventFilter(self, obj, event):
        #print(event.type(), obj)
        if event.type() == 6:
            if event.key() == 16777220 or event.key() == 16777221:   #2 fele enter
                #print('enter')
                self.valueEntered(obj)
        if event.type() == 9:
            #print('exit widget')
            self.valueEntered(obj)
        return False

    def valueEntered(self, obj):
        print('entered')
        if 'accepted' in self.GeomInput[self.MyDataTabs.CurrTab]:
            #print('van accepted')
            if (self.GeomInput[self.MyDataTabs.CurrTab])['accepted']:
                #print('accepted:True')
                (self.GeomInput[self.MyDataTabs.CurrTab])['accepted'] = False
                print('accepted:false')
        self.MyDataTabs.corr_tabs(obj)
        self.MyDataTabs.AccNextEnable(obj)


    def Show_(self):
        if self.obj_BackToMain.Widget.isVisible():
            self.obj_BackToMain.Widget.hide()

        self.ui.Sp_1_Di.setValue(10)    #----------------------testvalues
        self.ui.Sp_1_T.setValue(10)
        self.ui.Sp_1_Do.setValue(10)
        self.ui.Sp_1_L.setValue(10)

        self.ui.Sp_2_D1.setValue(10)
        self.ui.Sp_2_D2.setValue(10)
        self.ui.Sp_2_D3.setValue(10)
        self.ui.Sp_2_D4.setValue(10)
        self.ui.Sp_2_D5.setValue(10)
        self.ui.Sp_2_D6.setValue(10)
        self.ui.Sp_2_D7.setValue(10)
        self.ui.Sp_2_D8.setValue(10)
        self.ui.Sp_2_D9.setValue(10)

        self.show()

    def GtFc_onClick(self):
        self.obj_BackToMain.Show_()        

    def Rb_Groove_onClick(self):
        #self.sender().objectName()
        self.ui.Gr1.setChecked(self.sender().objectName()==self.ui.Gr1.objectName())
        self.ui.Gr2.setChecked(self.sender().objectName()==self.ui.Gr2.objectName())
        self.ui.Gr3.setChecked(self.sender().objectName()==self.ui.Gr3.objectName())
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/"+self.sender().objectName()+".jpg")
        self.ui.S2_L1.setPixmap(self.pixmap)
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/"+self.sender().objectName()+"_3.jpg")
        self.ui.S3_L1.setPixmap(self.pixmap)
        #print(self.sender().objectName())
        self.MyDataTabs.setCurrTabGr('',self.sender())        

    def tabChange(self):
        #print(self.sender().currentWidget().objectName())
        self.MyDataTabs.setCurrTabGr(self.sender().currentWidget(),'')

    def AccNext_Clicked(self):
        #self.GeomInput
        #self.MyDataTabs.CurrTab
        #self.MyDataTabs.CurrGr
        #self.valuesAccepted()
        Tab = self.MyDataTabs.CurrTab
        Gr = self.MyDataTabs.CurrGr
        TabGr =   Tab+Gr
        #print(TabGr)
        for key in (self.MyDataTabs.datatabs[TabGr])['ObjLabels']:
            ((self.GeomInput[Tab])['values'])[key] = (((self.MyDataTabs.datatabs[TabGr])['ObjLabels'])[key]).value()
        print(self.GeomInput)

        self.obj_CheckResults.Init()
    
    def valuesAccepted(self):
        #rgb(153, 204, 255)
        #self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr
        #print(self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames']
        #print((self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames'])
        for Widget in (self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames']:
            (((self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames'])[Widget]).setStyleSheet("background:rgb(153, 204, 255);font: bold 12px")