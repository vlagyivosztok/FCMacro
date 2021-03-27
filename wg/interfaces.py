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
    from PySide import QtGui #QWidget
    from PySide import QtUiTools #QUiLoader
    from PySide import QtCore #QFile, Qt
except:
    os.system(g_wg_dir+'\import-error.vbs')
    raise Exception("Quit macro / interfaces.py")
#endregion imports

class BackToMain(QtGui.QWidget):
    def __init__(self):
       #rint('dbg','BackToMain init')
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
       #rint('dbg','BackOnClick')
        self.obj_MainWidget.Show_()

    def Show_(self):
       #rint('dbg','BackToMain Show_')
        if self.obj_MainWidget.isVisible():
            self.obj_MainWidget.hide()    
        self.Widget.show()

class CheckResults(QtGui.QWidget):
    def __init__(self):
       #rint('dbg',"CheckResults init")
        #super(CheckResults, self).__init__()
        self.loader = QtUiTools.QUiLoader()
        self.file = QtCore.QFile(g_wg_dir+"/chktext.ui")
        self.file.open(QtCore.QFile.ReadOnly) 
        self.Widget = self.loader.load(self.file)
        self.file.close()
        self.Widget.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
        self.obj_MainWidget = None
        self.Tab = ''

        #region checktests
        self.GeomInput = {}
        self.checkOutput = []
        #self.checktext = ''
        self.checktexts = {}
        self.checklist = {}
        
        
        

         
        ''' if 'D' in (self.GeomInput['tab2'])['values']
            ((self.GeomInput[Tab])['values'])[key] '''


        #endregion checktests

        #region checklists
        self.checklist['tab1Gr0']=[1,2]
        self.checklist['tab2Gr1']=[11,12,13,14]
        self.checklist['tab2Gr2']=[13,14,21,22]
        self.checklist['tab2Gr3']=[13]
        self.checklist['tab3Gr1']=[31,32]
        self.checklist['tab3Gr2']=[31,33]
        self.checklist['tab3Gr3']=[]
        # endregion checklists
        
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

    ''' def init_checktexts(self):
        self.GeomInput = self.obj_MainWidget.GeomInput      ############# ez miert van itt? mert pillanatnyilag nincs jobb otletem... '''
     
    def Init(self):
       #rint('dbg','CheckResults Init')
        self.checkOutput = []

        self.Tab = self.obj_MainWidget.MyDataTabs.CurrTab
        self.Gr = self.obj_MainWidget.MyDataTabs.CurrGr
        TabGr =   self.Tab+self.Gr        

        for index in self.checklist[TabGr]:
            if index in self.checktexts:
                exec(self.checktexts[index])


        ###rint('dbg',((self.GeomInput['tab1'])['values'])['Di'])
        ###rint('dbg',self.checkOutput)
        self.Widget.TB_Chktext.setText('')
        if not len(self.checkOutput):
            self.checkOutput.append ("The values seem to be OK.")
        else:
            self.checkOutput.insert(0,"")
            self.checkOutput.insert(0,"(There are no strict rules. You can accept anyway.)")
            self.checkOutput.insert(0,"Please consider the following comments!")
        for text in self.checkOutput:
            self.Widget.TB_Chktext.append(text)
        ###rint('dbg',self.checkOutput)
        self.Widget.show() 

    def Hide_(self):
       #rint('dbg','CheckResults Hide_')
        self.Widget.hide() 

    def Accept(self):
        #rint('dbg','CheckResults Accept')
        #rint('dbg',self.obj_MainWidget.GeomInput)
        Tab = self.obj_MainWidget.MyDataTabs.CurrTab
        (self.obj_MainWidget.GeomInput[Tab])['accepted'] = True
        self.Widget.hide()
        self.obj_MainWidget.valuesAccepted()
        #rint('dbg',self.obj_MainWidget.GeomInput)

class MainWidget(QtGui.QMainWindow):
    class DataTabs:    #minden tab es az adatai, adatfeldolgozasa, lathatosagok

        def __init__(self):
           #rint('dbg','DataTabs init')
            self.actStep = ''       #nem biztos, hogy kell
            #self.stepNr = {}
            #self.stepobj = {}
            #self.controltext = []
            #self.filled = True
            
            self.parent = None
            self.datatabs =  {}
            for key in ['tab1Gr0','tab2Gr0','tab2Gr1','tab2Gr2','tab2Gr3','tab3Gr0','tab3Gr1','tab3Gr2','tab3Gr3','tab4Gr0']:
                self.datatabs[key]= {}
            ###rint('dbg',self.datatabs)               #debug #rint
            #self.dict = {}
            self.CurrTab = ''   
            self.allTab = ['tab1','tab2','tab3','tab4']
            self.CurrGr = ''
            #self._sender =''
            ###rint('dbg',self, 'DataTabs')
            ###rint('dbg',self.CurrTab,self.CurrGr)
            ###rint('dbg',type(self.datatabs))

            """ self.dict
            
            self.datatabs['WidgetLabel']= {}
            self.datatabs['WidgetName']= {} """
            
            #self.datatabs['tab1gr0'] = [{}]
            """#rint('dbg','datatabs', type(self.datatabs))
           #rint('dbg','WidgetLabel', type(self.datatabs['WidgetLabel']))
           #rint('dbg','WidgetName', type(self.datatabs['WidgetName'])) """
      
        def getTabWidgets(self,tabname,dictname,widgets,labels = None): #string, dict, labels lehet None
            '''Ha van labels, akkor csinal egy ObjLabels Dict-t is'''      
            ###rint('dbg','DataTabs getTabWidgets') #, name, widgets,labels)
            #if dictname != '':
            ###rint('dbg',type(tabname),type(dictname),type(widgets))
            if type(widgets) is not dict:
                (self.datatabs[tabname])[dictname]= widgets
            else:
                (self.datatabs[tabname])[dictname]= widgets
                if labels != None:      #
                    (self.datatabs[tabname])['ObjLabels']= dict(zip(labels,widgets.values())) 
            ''' else:                      #ez a korabbi getTabControl
                (self.datatabs[tabname])[dictname]= widgets '''            

        def setCurrTabGr(self,Tab,Gr):     #isChecked()
            ''' Tab: object, Gr: string
            CurrTab es CurrGr beallitasa, hogy mindig az aktualis allapotot mutassak.
            Tab2-n es Tab3-n a Tab2 Gr Radiobutton szerinti allapotot allitja be CurrTab es CurrGr-be
            hivja: Rb_Groove_onClick, Gr kivalasztasa utan
            tabChange: kezi tab valtas utan
            AccNext_Clicked: AccNext / Next eseten tabot valt, meghivja ezt'''            
           #rint('dbg','DataTabs setCurrTabGr')
            if Gr == '':
                self.CurrTab = Tab.objectName()
                if self.CurrTab == 'tab2' or self.CurrTab == 'tab3':      # and (TabOrGr.objectName()).find('Gr')>=0:
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
            '''CurrTab es CurrGr allapotabol beallitja az akt. lathatosagokat   '''
           #rint('dbg','DataTabs VidgetVisib')
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames']):
                ###rint('dbg','own: ',widget, 'parent: ',self.parent )
                #self.parent.ui.findChild(QtGui.QDoubleSpinBox, widget).setHidden(False)
                (self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'][key].setHidden(False)
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels']):
                widgetL = ((((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]).objectName()).replace('Sp','L')
                self.parent.ui.findChild(QtGui.QLabel, widgetL).setText(key)
                self.parent.ui.findChild(QtGui.QLabel, widgetL).setHidden(False)
                ###rint('dbg',(((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'][widget]).objectName()).replace('Sp','L'))
            if 'ObjHide' in (self.datatabs[self.CurrTab+self.CurrGr]):
                for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjHide']):
                    ###rint('dbg','hide: ',widget, 'parent: ',self.parent)
                    self.parent.ui.findChild(QtGui.QDoubleSpinBox, key).setHidden(True)
                    widgetL = ((((self.datatabs[self.CurrTab+self.CurrGr])['ObjHide'])[key]).objectName()).replace('Sp','L')
                    self.parent.ui.findChild(QtGui.QLabel, widgetL).setHidden(True)

        def resetEnabled(self):
            #rint('dbg','DataTabs resetEnabled')
            #rint('dbg',self.parent.GeomInput)
            ''' egy DblSpB megvaltozott. Ekkor a sajat es
            a koveto tabok accepted false-ra allitja es a koveto tabokon minden nem nullat zoldre a
            a DataTabs [tabxGr0] listaja szerint. '''    
            self.parent.GeomInput['accepted'] =False
            self.parent.ui.tabWidget.setTabEnabled(3, False)
            self.parent.ui.Cb_4_CreatArrang.setStyleSheet("background:rgb(255,255,224);font: bold 12px")
            self.parent.ui.Cb_4_CreatGeom.setEnabled(False)
            #rint('dbg',self.parent.ui.Cb_4_CreatArrang.styleSheet())
            next_ = False
            for key in ['tab1','tab2','tab3']:
                if next_:
                    (self.parent.GeomInput[key])['accepted'] =False
                    self.checkZeros(key)
                elif self.CurrTab == key:
                    (self.parent.GeomInput[key])['accepted'] =False
                    next_ = True            
            #rint('dbg',self.parent.GeomInput)

        def checkZeros(self, Tab, _obj = None):
            '''Ha Tab-bal, _obj = None hivjak, akkor a tab-ot ellenorzi DataTabs [tabxGr0] listaja szerint
            minden nem 0-t zoldre allit
            Ha tab = '', _obj-jal hivjak, akkor az az aktualis widget. Az aktualis tabot nullakra ellenorizni
            ha ok, true.
             '''
           #rint('dbg','DataTabs checkZeros',Tab,_obj)
            ###rint('dbg','helo', (self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'] )    #[self.CurrTab+self.CurrGr]
            if _obj == None:
                for widget in ((self.datatabs[Tab+'Gr0'])['ObjNames']).values():
                    if widget.value() != 0:
                        widget.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
            else:
                if _obj.value() == 0.0:
                    _obj.setStyleSheet("background-color:red;font: bold 12px")
                    return False    
                checkvalues = 0
                sum_obj = 0
                for widget in (((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames']).values()):
                    sum_obj += 1
                    if widget.value() != 0.0:
                        checkvalues += 1
                        widget.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
                if checkvalues == sum_obj:
                    return True
                else:
                    return False

        def AccNextEnable(self, _obj):
            '''  '''
           #rint('dbg','DataTabs AccNextEnable')
            if self.checkZeros('',_obj):   #lehetne for nelkul is, jelenleg egy widget van benne
                ((self.datatabs[self.CurrTab+self.CurrGr])['ObjContr']).setEnabled(True)
            else:
                ((self.datatabs[self.CurrTab+self.CurrGr])['ObjContr']).setEnabled(False)

        def corr_tabs(self,_obj):
            ''' Az aktualis beadas fuggvenyeben az erintett DblSpB ertekeket aktualizalja.
            CurrTab, CurrGr kell hozza, _obj az aktualis Widget
            Tab1, Tab2Gr1, Gr2 Tab3Gr1 kesz , a tobbi megcsinalni'''
           #rint('dbg','DataTabs  corr_tabs')
            #pass
            self.LabelObjs = {}
            self.ObjLabels = {}
            self.testSeq = []
            ###rint('dbg',_obj)
            #for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames']):
                #self.WidgetNames[key] = ((self.datatabs[self.CurrTab+self.CurrGr])['ObjNames'])[key]
            for key in ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels']):
                self.ObjLabels[((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]] = key
                self.LabelObjs[key] = ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key]
                ###rint('dbg',((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key])
                if ((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key] == _obj:
                    ###rint('dbg',((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key])
                    ###rint('dbg',((self.datatabs[self.CurrTab+self.CurrGr])['ObjLabels'])[key],_obj, key )
                    _sender = key      #Label

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
                if _sender == 'R':
                    self.testSeq = ['H','B']
                if _sender.find('H') >= 0:
                    self.testSeq = ['H','B']
                if _sender.find('B') >= 0:
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

            elif (self.CurrTab+self.CurrGr) == 'tab3Gr1' or (self.CurrTab+self.CurrGr) == 'tab3Gr2':     #['It', 'Wd', 'Wdo']
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
                                        

    def __init__(self):
        #super(MainWidget, self).__init__()
       #rint('dbg','mainwidget init')
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.file = QtCore.QFile(g_wg_dir+"/MainDialog.ui")
        self.file.open(QtCore.QFile.ReadOnly)
        self.file.close()
        self.ui=QtUiTools.QUiLoader().load(self.file)
        self.setCentralWidget(self.ui)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.MyDataTabs = self.DataTabs()
        self.MyDataTabs.parent = self

        #region variables

        self.obj_BackToMain = None
        self.obj_CheckResults = None
        self.obj_WiresInGroove = None

        tabname = ''        
        _dict = {}
        #self.currWidget = None 
        #self.tag = ''   #2. mezo, WLabel vagy WName
        self.GeomInput = {}
        self.GeomInput['accepted'] = False
        self.GeomInput['groove'] = ''
        for key in ['tab1','tab2','tab3','tab4']:
            self.GeomInput[key] = {}
            self.GeomInput[key] = {'values':{},'accepted':False }
       #rint('dbg','self.GeomInput %s' %self.GeomInput)
        ###rint('dbg','MainWidget_init',self.GeomInput)
        #self.obj_CheckResults.GeomInput = self.GeomInput
        #self.ui.L_3_expl.setText("first row <br>second row")
        #WINDING GEOM FreeCAD extension
        self.setWindowTitle("WINDING GEOM FreeCAD extension - - - Operating FreeCAD is disabled - - -")
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

        self.ui.Sp_3_D1.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D2.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D3.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D4.setStyleSheet("background:rgb(255,255,224)")
        self.ui.Sp_3_D5.setStyleSheet("background:rgb(255,255,224)")


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

        self.MyDataTabs.actStep = self.ui.tabWidget.currentWidget().objectName()
        ###rint('dbg',self.MyDataTabs.actStep)
        #endregion intial styles

        #region send widgets to DataTabs
        tabname = 'tab1Gr0'
        _dict[self.ui.Sp_1_Di.objectName()] = self.ui.Sp_1_Di   #{'D1':}
        _dict[self.ui.Sp_1_T.objectName()] = self.ui.Sp_1_T #{'T':}
        _dict[self.ui.Sp_1_Do.objectName()] = self.ui.Sp_1_Do   #{'Do':}
        _dict[self.ui.Sp_1_L.objectName()] = self.ui.Sp_1_L #{'L':}

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['Di','T','Do','L'])

        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',self.ui.Cb_1_AccNext)

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

        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',self.ui.Cb_2_AccNext) 
        
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

        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',self.ui.Cb_2_AccNext)

        _dict = {}
        tabname = 'tab2Gr3'
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

        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',self.ui.Cb_2_AccNext)

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
        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',self.ui.Cb_3_AccNext)
        self.MyDataTabs.getTabWidgets(tabname,'ObjHide',{self.ui.Sp_3_D5.objectName():self.ui.Sp_3_D5} ) 
        
        _dict = {}
        tabname = 'tab3Gr2'
        _dict[self.ui.Sp_3_D1.objectName()] = self.ui.Sp_3_D1   
        _dict[self.ui.Sp_3_D2.objectName()] = self.ui.Sp_3_D2 
        _dict[self.ui.Sp_3_D3.objectName()] = self.ui.Sp_3_D3
        _dict[self.ui.Sp_3_D4.objectName()] = self.ui.Sp_3_D4   
 

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['It','Wd','Wdo','G'])
        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',self.ui.Cb_3_AccNext)
        self.MyDataTabs.getTabWidgets(tabname,'ObjHide',{self.ui.Sp_3_D5.objectName():self.ui.Sp_3_D5} ) 


        _dict = {}
        tabname = 'tab3Gr3'
        _dict[self.ui.Sp_3_D1.objectName()] = self.ui.Sp_3_D1   
        _dict[self.ui.Sp_3_D2.objectName()] = self.ui.Sp_3_D2 
        _dict[self.ui.Sp_3_D3.objectName()] = self.ui.Sp_3_D3   
        _dict[self.ui.Sp_3_D4.objectName()] = self.ui.Sp_3_D4
 

        self.MyDataTabs.getTabWidgets(tabname,'ObjNames',_dict,['It','Wd','Wdo','G'])
        self.MyDataTabs.getTabWidgets(tabname,'ObjContr',self.ui.Cb_3_AccNext)
        self.MyDataTabs.getTabWidgets(tabname,'ObjHide',{self.ui.Sp_3_D5.objectName():self.ui.Sp_3_D5})                      

        ###rint('dbg',self.MyDataTabs.datatabs)
        '''#rint('dbg','tab1Gr0',self.MyDataTabs.datatabs['tab1Gr0'])
       #rint('dbg','tab2Gr0',self.MyDataTabs.datatabs['tab2Gr0'])
       #rint('dbg','tab2Gr1',self.MyDataTabs.datatabs['tab2Gr1'])
       #rint('dbg','tab2Gr2',self.MyDataTabs.datatabs['tab2Gr2'])
       #rint('dbg','tab2Gr3',self.MyDataTabs.datatabs['tab2Gr3'])
       #rint('dbg','tab3Gr0',self.MyDataTabs.datatabs['tab3Gr0'])
       #rint('dbg','tab3Gr1',self.MyDataTabs.datatabs['tab3Gr1'])
       #rint('dbg','tab3Gr2',self.MyDataTabs.datatabs['tab3Gr2'])
       #rint('dbg','tab3Gr3',self.MyDataTabs.datatabs['tab3Gr3']) '''

        #endregion send widgets              

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
        self.ui.Gr3.clicked.connect(self.Rb_Groove_onClick)

        self.ui.Cb_1_exitWg.clicked.connect(self.closeEvent)
        self.ui.Cb_2_exitWg.clicked.connect(self.closeEvent)
        self.ui.Cb_3_exitWg.clicked.connect(self.closeEvent)
        self.ui.Cb_4_exitWg.clicked.connect(self.closeEvent)

        self.ui.Cb_4_CreatArrang.clicked.connect(self.test)    

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

        self.MyDataTabs.CurrTab = self.ui.tabWidget.currentWidget().objectName()    #kezdoallapot beallitasa
        self.MyDataTabs.CurrGr = 'Gr0'
        ###rint('dbg','tabwidget', self.ui.tabWidget.currentWidget().objectName())

        self.testvalues()           ##############################################  TESTVALUES
        #rint('dbg',self.GeomInput)
              
    def test(self):
        self.obj_CreateGeom.create2D()
        #rint('dbg',self.sender())

    def closeEvent(self, event = None):
        reply = QtGui.QMessageBox.question(self, 'WINDING GEOM', 'Are you sure you want to close WINDING GEOM?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if event != None:
                event.accept()
            #rint('Window closed')
            else:
                self.hide()

        else:
            if event != None:
                event.ignore()

    def eventFilter(self, obj, event):
        ###rint('dbg','MainWidget eventfliter')
        ###rint('dbg',event.type(), obj)
        if event.type() == 6:
            if event.key() == 16777220 or event.key() == 16777221:   #2 fele enter
                ###rint('dbg','enter')
                self.valueEntered(obj)
        if event.type() == 9:
            ###rint('dbg','exit widget')
            self.valueEntered(obj)
        return False

    def valueEntered(self, obj):    #koztes fuggveny, eventfilter es a kovetkezok koze
        '''1. Az aktualis es az utana levo osszes tab Geominput['tabx']['accepted']
        es a Geominput['accepted'] false-ra allitasa.
         '''
       #rint('dbg','MainWidget valueEntered')
        self.MyDataTabs.resetEnabled()
        self.MyDataTabs.corr_tabs(obj)
        self.MyDataTabs.AccNextEnable(obj)

    def testvalues(self):
        #rint('dbg','MainWidget testvalues')

        self.ui.Sp_1_Di.setValue(85)    #----------------------####################### testvalues
        self.ui.Sp_1_T.setValue(20)
        self.ui.Sp_1_Do.setValue(85+2*20)
        self.ui.Sp_1_L.setValue(110)

        self.ui.Sp_2_D1.setValue(1)
        self.ui.Sp_2_D2.setValue(1)
        self.ui.Sp_2_D3.setValue(10)
        self.ui.Sp_2_D4.setValue(10)
        self.ui.Sp_2_D5.setValue(10)
        self.ui.Sp_2_D6.setValue(1.5)
        self.ui.Sp_2_D7.setValue(4)
        self.ui.Sp_2_D8.setValue(10)
        self.ui.Sp_2_D9.setValue(6)

        self.ui.Sp_3_D1.setValue(1)
        self.ui.Sp_3_D2.setValue(1)
        self.ui.Sp_3_D3.setValue(1)
        self.ui.Sp_3_D4.setValue(1)

        ''' self.GeomInput

        #tab2Gr1: {'H1': D1, 'H2': D2, 'H3': D3, 'H4': D4, 'B1': D6, 'B2': D7, 'R': D8, 'D': D9}
        #tab2Gr2: ['H1' D1,'H2' D2, 'H3' D3 ,'H4' D4 ,'B1' D5 ,'B2' D6 ,'B3' D7 ,'B4' D8 ,'R' D9]

        dbg {'accepted': False, 'groove': '', 'tab1': {'values': {'Di': 10.0, 'T': 10.0, 'Do': 30.0, 'L': 10.0}, 'accepted': False},
        'tab2': {'values': {'H1': 10.0, 'H2': 10.0, 'H3': 10.0, 'H4': 15.0, 'B1': 10.0, 'B2': 10.0, 'R': 5.0, 'D': 10.0}, 'accepted': False},
        'tab3': {'values': {'It': 1.0, 'Wd': 1.0, 'Wdo': 1.0, 'G': 0.1}, 'accepted': True},
        'tab4': {'values': {}, 'accepted': False}} '''
        
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
        self.ui.tabWidget.setCurrentIndex(3)



    def Show_(self):
       #rint('dbg','MainWidget Show_')
        if self.obj_BackToMain.Widget.isVisible():
            self.obj_BackToMain.Widget.hide()
        self.show()
        ####################################################   TEST   TEST   TEST   TEST   TEST   TEST 
        self.ui.tabWidget.setTabEnabled(3, True)
        self.ui.tabWidget.setCurrentIndex(3)        ###########################################################################################


    def GtFc_onClick(self):
        self.obj_BackToMain.Show_()        

    def Rb_Groove_onClick(self):
       #rint('dbg','MainWidget Rb_Groove_onClick')
        #self.sender().objectName()
        self.ui.Gr1.setChecked(self.sender().objectName()==self.ui.Gr1.objectName())
        self.ui.Gr2.setChecked(self.sender().objectName()==self.ui.Gr2.objectName())
        self.ui.Gr3.setChecked(self.sender().objectName()==self.ui.Gr3.objectName())
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/"+self.sender().objectName()+".jpg")
        self.ui.S2_L1.setPixmap(self.pixmap)
        self.pixmap = QtGui.QPixmap(g_wg_dir+"/"+self.sender().objectName()+"_3.jpg")
        self.ui.S3_L1.setPixmap(self.pixmap)
        # explanation text to variables
        self.MyDataTabs.setCurrTabGr('',self.sender())
        ###rint('dbg',"self.MyDataTabs.CurrGr ", self.MyDataTabs.CurrGr)
        if self.MyDataTabs.CurrGr == 'Gr1' or self.MyDataTabs.CurrGr == 'Gr2':
            self.ui.L_3_expl.setText("Explanation of dimension variables:<br><br>It: insulation thickness<br>Wd: wire diameter <br>" \
                "Wdo: insulated wire outer diameter<br>G: gap between Wdo")
        elif self.MyDataTabs.CurrGr == 'Gr3':
            self.ui.L_3_expl.setText("Gr3 <br>first row <br>second row")
        ###rint('dbg',self.sender().objectName())
                

    def tabChange(self):
       #rint('dbg','MainWidget tabChange')
        self.MyDataTabs.setCurrTabGr(self.sender().currentWidget(),'')

    def AccNext_Clicked(self):
       #rint('dbg','MainWidget AccNext_Clicked')
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
        #rint('dbg','MainWidget valuesAccepted')
        #rint('dbg',self.GeomInput)
        for Widget in (self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames']:
            (((self.MyDataTabs.datatabs[self.MyDataTabs.CurrTab+self.MyDataTabs.CurrGr])['ObjNames'])[Widget]).setStyleSheet("background:rgb(153, 204, 255);font: bold 12px")
        self.GeomInput['accepted'] = (self.GeomInput['tab1'])['accepted'] and (self.GeomInput['tab2'])['accepted'] and (self.GeomInput['tab3'])['accepted']
        self.GeomInput['groove'] = self.MyDataTabs.CurrGr
        self.ui.tabWidget.setTabEnabled(3, self.GeomInput['accepted'])
        #rint('dbg',self.GeomInput)