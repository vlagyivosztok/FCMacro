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
    import Draft        #FreeCAD, Part, PartDesign,
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
        #rint('WiresInGroove init')
        self.FcSTD = ''
        self.tab1 = {}
        self.tab2 = {}
        self.tab3 = {}
        self.gr_cont_pts = []
        self.wire_collection = []

        #tab2Gr1: {'H1': D1, 'H2': D2, 'H3': D3, 'H4': D4, 'B1': D6, 'B2': D7, 'R': D8, 'D': D9}
        #tab2Gr2: ['H1' D1,'H2' D2, 'H3' D3 ,'H4' D4 ,'B1' D5 ,'B2' D6 ,'B3' D7 ,'B4' D8 ,'R' D9]

        self.obj_MainWidget = None

    def createGroove(self):
        #ertekek atvetele self.obj_MainWidget.GeomInput-bol
        #rint('dbg','WiresInGroove dummy',self.obj_MainWidget.GeomInput)
        ''' 
         '''
        
        self.FcSTD = g_wg_dir+'/'+self.obj_MainWidget.GeomInput['groove']+'.FCSTD'
        #rint(App.listDocuments())
        for doc in App.listDocuments():
            #rint(doc, App.listDocuments()['Gr1'].FileName, self.FcSTD)
            if App.listDocuments()[doc].FileName != self.FcSTD:
                App.closeDocument(doc)
        #rint('dbg App.closeDocument')
        #return False  App.listDocuments()['Gr1'].FileName

            #ellenorizni, hogy van-e nyitott Document
        
        if App.ActiveDocument == None:
            App.open(self.FcSTD)
        if App.ActiveDocument.FileName != self.FcSTD:
            return False
        self.tab1 = self.obj_MainWidget.GeomInput['tab1']
        self.tab2 = self.obj_MainWidget.GeomInput['tab2'] 
        #rint('dbg App.open(self.FcSTD)')
        ''' try: '''
        if not self.clearGroove():
            return False
        #rint('dbg self.clearGroove')
        #rint(self.tab1['values'])
        #rint('core')
        for key in ['Di','T']:
            #rint('dbg', key, (self.tab1['values'])[key])
                
            App.ActiveDocument.getObjectsByLabel("StatCore0")[0].setDatum(key,(self.tab1['values'])[key])
        #meretek atadasa a sketchnek
        #sk.solve() App.ActiveDocument.getObjectsByLabel("Sketch005")[0].solve()
        App.ActiveDocument.getObjectsByLabel("StatCore0")[0].solve()
        App.ActiveDocument.recompute()
        #rint('core ready')

        if self.obj_MainWidget.GeomInput['groove'] == 'Gr1':
            #rint('Gr1 Sketch005')
            for key in ['B1','B2','H1','H2','H3', 'D']:
                #rint('dbg', key, (self.tab2['values'])[key])
                App.ActiveDocument.getObjectsByLabel("Sketch005")[0].setDatum(key,(self.tab2['values'])[key])
            App.ActiveDocument.getObjectsByLabel("Sketch005")[0].solve()
            App.ActiveDocument.getObjectsByLabel("Sketch006")[0].solve()
            App.ActiveDocument.recompute()
            self.Bmax = max((self.tab2['values'])['B2'],(self.tab2['values'])['D'])
            #rint('Sketch005 ready')            

        elif self.obj_MainWidget.GeomInput['groove'] == 'Gr2':
            #rint('Gr2 Sketch005')
            for key in ['B1','B2','H1','H2','H4']:
                App.ActiveDocument.getObjectsByLabel("Sketch005")[0].setDatum(key,(self.tab2['values'])[key])
                #rint('dbg', key,(self.tab2['values'])[key])
            App.ActiveDocument.getObjectsByLabel("Sketch005")[0].solve()
            App.ActiveDocument.getObjectsByLabel("Sketch")[0].solve()
            App.ActiveDocument.getObjectsByLabel("Sketch006")[0].solve()
            App.ActiveDocument.recompute()
            self.Bmax = max((self.tab2['values'])['B2'],(self.tab2['values'])['B4'])
            #rint('Sketch005 ready')

            #rint('Gr2 Sketch')
            for key in ['R','B4']:
                App.ActiveDocument.getObjectsByLabel("Sketch")[0].setDatum(key,(self.tab2['values'])[key])
                #rint('dbg', key,(self.tab2['values'])[key])
            App.ActiveDocument.getObjectsByLabel("Sketch")[0].solve()
            App.ActiveDocument.getObjectsByLabel("Sketch006")[0].solve()         
            App.ActiveDocument.recompute()
            #rint('Sketch ready')

        elif self.obj_MainWidget.GeomInput['groove'] == 'Gr3':
            #rint('Gr3 not implemented yet')
            raise Exception("not implemented...")                    

        #minden geometria valtozas utan:        
        App.ActiveDocument.recompute()
        print('max B %s' % self.Bmax)
        #rint('recompute')

        #Body a sketch origojaba: Sketch006 Ymid, Ydir
        #App.Vector(App.ActiveDocument.getObjectsByLabel("Sketch006")[0].getDatum("Ymid"),0)
        self.v_gr_base = App.Vector(0,App.ActiveDocument.getObjectsByLabel("Sketch006")[0].getDatum("Ymid"),0)
        """ nem forditjuk el, csak pozicioba helyezzuk ??? """
        #self.v_gr_dir = App.Vector(0,App.ActiveDocument.getObjectsByLabel("Sketch006")[0].getDatum("Ydir"),0)
        #self.v_dir = self.v_gr_dir.sub(self.v_gr_base).normalize()
        #self.base_dir = App.Vector(0,1,0)
        #rint(self.v_gr_base,self.v_dir)
        App.ActiveDocument.getObject("C_BdWires").Placement.Base = self.v_gr_base
        App.ActiveDocument.getObject("C_BdWires").Placement.Rotation = (0,0,0,1) #(0,0,1,0)
        #App.ActiveDocument.getObject("C_BdWires").Placement.Rotation = self.def_quaternion(self.base_dir,self.v_dir)
        
        App.ActiveDocument.recompute()
        #rint('CS placed')
        return True
        ''' except:
            return False '''

    def closeGr(self):
        ''' ResetEnabled, ha tab2 reset, modell becsuk (ha nyitva van), mentes neklul '''
        pass

    def clearGroove(self):
        ''' try: '''
        for obj in App.ActiveDocument.getObject('C_BdWires').OutList:
            if App.ActiveDocument.getObject(obj.Name).TypeId == 'Part::Part2DObjectPython':
                App.ActiveDocument.removeObject(obj.Name)
        #rint('groove cleared')
        return True
        ''' except:
            return False '''

    def createArrang(self):     
        #meretek atadasa
        self.tab3 = self.obj_MainWidget.GeomInput['tab3']
        self.A  = ((self.obj_MainWidget.GeomInput['tab3'])['values'])['Wdo'] + ((self.obj_MainWidget.GeomInput['tab3'])['values'])['G']    # = Dk + Lr Wdo+G
        self.y_incr = self.A*sqrt(3)/2      #y_incr = A*sqrt(3)/2
        self.Dk = ((self.obj_MainWidget.GeomInput['tab3'])['values'])['Wdo']  #Dk = Dh + 2*Hsz
        self.Dw = ((self.obj_MainWidget.GeomInput['tab3'])['values'])['Wd']
        self.plane_h = (self.tab1['values'])['L'] + self.Bmax 
        

        self.wire_collection = []
        self.insul_collection = []
        self.point_collection = []
        ''' >>> for obj in App.ActiveDocument.getObject('C_BdWires').OutList:
     	#rint(obj.Name)
        >>> for obj in App.ActiveDocument.getObject('C_BdWires').OutList:
     	App.ActiveDocument.removeObject(obj.Name)
        >>> for obj in App.ActiveDocument.getObject('C_BdWires').OutList:
        if App.ActiveDocument.getObject(obj.Name).TypeId == 'Part::Part2DObjectPython':
    	#rint(obj.Name)
        '''

        ''' try: '''
        if not self.clearGroove():
            return 'clearGroove False'
    #sketch kontur bekerese         App.ActiveDocument.getObjectsByLabel("Sketch006")[0]
        """ 
        Egy masik bodyba pontokat a körök közepére. 
         """
        if self.obj_MainWidget.GeomInput['groove'] == 'Gr1':
            self.gr_cont_pts_ = self.groove_contour(App.ActiveDocument.getObjectsByLabel("Sketch006")[0])
            #rint('dbg',gr_cont_pts_)
            #rint('dbg Gr1 Sketch points',self.gr_cont_pts_)

        elif self.obj_MainWidget.GeomInput['groove'] == 'Gr2':
            self.gr_cont_pts_ = self.groove_contour(App.ActiveDocument.getObjectsByLabel("Sketch006")[0])
            #rint('dbg Gr2 Sketch points',self.gr_cont_pts_)


        elif self.obj_MainWidget.GeomInput['groove'] == 'Gr3':
            #rint('Gr3 not implemented yet')
            raise Exception("not implemented...")             


        self.gr_cont_pts = []
        for pts in self.gr_cont_pts_:
            self.vec1 = (App.Vector(self.v_gr_base[0],self.v_gr_base[1])).sub(App.Vector(pts[0],pts[1]))
            self.gr_cont_pts.append((self.vec1[0],-self.vec1[1]))               #x-re tukrozes------------------------------
        #rint('dbg points move',self.gr_cont_pts)

        self.Bd_Points = App.ActiveDocument.addObject('PartDesign::Body','Points')
        self.Bd_Points.Placement.Base = self.v_gr_base
        self.Bd_Points.Placement.Rotation = (0,0,0,1)

        self.wloc_in_groove()

        #a vegen a gombok beallitasa
        self.obj_MainWidget.ui.Cb_4_CreatArrang.setStyleSheet("background:rgb(144,238,144);font: bold 12px")
        self.obj_MainWidget.ui.Cb_4_CreatGeom.setEnabled(True)
        return 'gombok, vege True'
        ''' except:
            return False '''
    
        #datum plane Placement
        App.ActiveDocument.getObject('DatumPlane').Placement.Base.z = self.plane_h
        App.ActiveDocument.getObject('Pad').Length = (self.tab1['values'])['L']

        #innen a huzalok letrehozasa#################################################################################################################
        #pontok self.Bd_Points-ban
        #huzal korok
        #

    def dummy(self):
        pass
     #rint('dbg','WiresInGroove dummy',self.obj_MainWidget.GeomInput)

    def def_quaternion(v1, v2):
        """ Quaternion v1 es v2 kozott, Tuple-t ad vissza FreeCAD formatumban """
        v1.normalize(), v2.normalize()

        if(abs(v1.dot(v2)-1) < 0.0001):
                #parhuzamos, irany marad
            print('azonos')
            return_tuple = (0.0,0.0,0.0,1.0)
            return return_tuple

        elif(abs(v1.dot(v2)+1) < 0.0001):
            print('ellentetes')
            new_q = Quaternion(axis=[0, 1, 0], degrees=180) # (pyquaternion)
            print(new_q)
            return_tuple = (round(new_q[1],6),round(new_q[2],6),round(new_q[3],6),round(new_q[0],6))
            return return_tuple

    def groove_contour(self, cont): # a horony geometria bekerese
        #rint(type(cont))
        App.ActiveDocument.recompute()
        Shp = cont.Shape        #App.ActiveDocument.getObjectsByLabel("Sketch006")[0]
        #rint(type(Shp))
        return Shp.discretize(int(Shp.Length/0.6))

    def wloc_in_groove(self): # huzal poziciok szamlaloja a horonyban
        #rint('dbg wloc_in_groove')
        x=0
        y=0
        # y basic incr
        y_sign = 1
        condition1 = True
        condition2 = True
        
        while condition1:    #level1: first pos. y, then neg. y
            condition1 = (y>=0)
            while condition2:#level 2 counting y
                condition2 = False
                while self.wire_condition(x,y): #level 3 counting x
                    condition2 = True
                    x += 1
                x=0
                y+=(1*y_sign)
            y_sign = -1
            y = y_sign
            condition2 = True


    def wire_condition(self,x,y): # huzal vizsgalata, hogy a hornyon belul helyezkedik-e el
        #global A, y_incr, gr_cont_pts, Dk, self.wire_collection
        #rint('dbg wire_condition')
        pnts = []
        if y%2: # paratlan
        #centers of circles
            x_circ = (x + 0.5)*self.A
            y_circ = y*self.y_incr
        else: #paros
            x_circ = x*self.A
            y_circ = y*self.y_incr

        circ_cont = self.circ_contour(x_circ,y_circ,self.Dk/2)    #a kor konturpontjait adja vissza

        for pnt_ in circ_cont:
            pnts.append((pnt_[0],pnt_[1],pnt_[2]))
        
        App.ActiveDocument.recompute()

        if Polygon(self.gr_cont_pts).contains(Polygon(pnts)):
            App.ActiveDocument.getObject("C_BdWires").addObject(self.wire_collection[-1])
            #point in the circle
            self.point_collection.append(self.Bd_Points.newObject('PartDesign::Point','point'))
            self.point_collection[-1].Placement = self.wire_collection[-1].Placement
            
            """ Pontok2.append(Test.newObject('PartDesign::Point',pont[0]))
            Test.getObject(pont[0]).Placement.Base.x = pont[1]
            Test.getObject(pont[0]).Placement.Base.y = pont[2]
            Test.getObject(pont[0]).Placement.Base.z = pont[3] """
            #mirrored: a vizsgalat csak az x tengely pozitiv ertekeire tortenik. A tukrozotteket automatikusan hozza tesszuk.
            if x_circ != 0:
                pl = App.Placement()
                pl.Rotation.Q=(0,0,0,1)
                pl.Base=App.Vector(-x_circ,-y_circ,0)
                self.wire_collection.append(Draft.makeCircle(radius=self.Dk/2,placement=pl,face=False,support=None))
                App.ActiveDocument.getObject("C_BdWires").addObject(self.wire_collection[-1])
                self.point_collection.append(self.Bd_Points.newObject('PartDesign::Point','point'))
                self.point_collection[-1].Placement = self.wire_collection[-1].Placement
                #rint(self.wire_collection[-1].Name)
        else:
            App.ActiveDocument.removeObject(self.wire_collection[-1].Name)
            self.wire_collection.pop()
            return False
        App.ActiveDocument.recompute()
        return True


    def circ_contour(self,x,y,r): # a kordinatakkal es sugarral kort rajzol, berakja a wire bodyba, es visszaadja a konturpontjait (lokalis??)

        #global self.wire_collection
        pl = App.Placement()
        pl.Rotation.Q=(0,0,0,1)
        pl.Base=App.Vector(x,-y,0)
        self.wire_collection.append(Draft.makeCircle(radius=r,placement=pl,face=False,support=None))
 
        return self.wire_collection[-1].Shape.discretize(int(self.wire_collection[-1].Shape.Length/0.1))