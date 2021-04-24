#region globals
import FreeCAD as App
import FreeCADGui as Gui
g_UserMacroDir = (App.getUserMacroDir()).replace('\\','/')
g_wg_dir = g_UserMacroDir+"wg"
#endregion globals

#region imports
import os
try:
    #import sys
    import Draft
    from math import sqrt
    from pyquaternion import Quaternion
    from pyquaternion.quaternion import np
    from copy import copy, deepcopy
    from shapely.geometry import Point, Polygon
    import time
except:
    os.system(g_wg_dir+'\import-error.vbs')
    raise Exception("Quit macro / creategeom.py")
#endregion imports


class CreateGeom():
    ''' A geometriat elkeszito osztaly. Innen hivjuk a FreeCAD eljarasait '''
    def __init__(self):
        self.FcSTD = ''
        self.tab1 = {}
        self.tab2 = {}
        self.tab3 = {}
        self.gr_cont_pts = []
        self.Bd_Wires_spl = []
        self.obj_MainWidget = None

    def createGroove(self):
        ''' A megfelelo file betoltese, meretek alkalmazasa magra, horonyra '''
        try:
            self.FcSTD = g_wg_dir+'/'+self.obj_MainWidget.GeomInput['groove']+'.FCSTD'
            for doc in App.listDocuments():
                if App.listDocuments()[doc].FileName != self.FcSTD:
                    App.closeDocument(doc)
            
            if App.ActiveDocument == None:
                App.open(self.FcSTD)
            if App.ActiveDocument.FileName != self.FcSTD:
                return False
            self.tab1 = self.obj_MainWidget.GeomInput['tab1']
            self.tab2 = self.obj_MainWidget.GeomInput['tab2'] 

            for key in ['Di','T']:
                App.ActiveDocument.getObjectsByLabel("StatCore0")[0].setDatum(key,(self.tab1['values'])[key])
            App.ActiveDocument.getObjectsByLabel("StatCore0")[0].solve()
            App.ActiveDocument.recompute()

            if self.obj_MainWidget.GeomInput['groove'] == 'Gr1':
                for key in ['B1','B2','H1','H2','H3', 'D']:
                    App.ActiveDocument.getObjectsByLabel("Sketch005")[0].setDatum(key,(self.tab2['values'])[key])
                App.ActiveDocument.getObjectsByLabel("Sketch005")[0].solve()
                App.ActiveDocument.getObjectsByLabel("Sketch006")[0].solve()
                App.ActiveDocument.getObjectsByLabel("Sketch009")[0].solve()
                App.ActiveDocument.recompute()
                self.Bmax = max((self.tab2['values'])['B2'],(self.tab2['values'])['D'])

            elif self.obj_MainWidget.GeomInput['groove'] == 'Gr2':
                for key in ['B1','B2','H1','H2','H4']:
                    App.ActiveDocument.getObjectsByLabel("Sketch005")[0].setDatum(key,(self.tab2['values'])[key])
                App.ActiveDocument.getObjectsByLabel("Sketch005")[0].solve()
                App.ActiveDocument.getObjectsByLabel("Sketch")[0].solve()
                App.ActiveDocument.getObjectsByLabel("Sketch006")[0].solve()
                App.ActiveDocument.recompute()
                self.Bmax = max((self.tab2['values'])['B2'],(self.tab2['values'])['B4'])

                for key in ['R','B4']:
                    App.ActiveDocument.getObjectsByLabel("Sketch")[0].setDatum(key,(self.tab2['values'])[key])
                App.ActiveDocument.getObjectsByLabel("Sketch")[0].solve()
                App.ActiveDocument.getObjectsByLabel("Sketch006")[0].solve()         
                App.ActiveDocument.recompute()
            
            self.plane_h = (self.tab1['values'])['L'] + self.Bmax
            self.v_gr_base = App.Vector(0,float(App.ActiveDocument.getObjectsByLabel("Sketch006")[0].getDatum("Ymid")),0)

            App.ActiveDocument.getObjectsByLabel('DatumPlane001')[0].Placement.Base.z = (self.tab1['values'])['L']
            App.ActiveDocument.getObjectsByLabel('DatumPlane')[0].Placement.Base.z = self.plane_h

            App.ActiveDocument.recompute() 
            return True
        except:
            return False

    def createArrang(self):     
        
        try:
            list_ = App.ActiveDocument.Objects
            del_item = ['Bd_Points','Bd_Wires','Bd_InsLay','Bd_InsComp']
            body_list = []
            feature_list =[]
            for elem1 in list_:
                for elem2 in del_item:
                    if elem1.Name == elem2:
                        body_list.append(elem1)
                        for 	elem3 in elem1.OutList:
                            if elem3.TypeId != 'App::Origin':
                                feature_list.append(elem3)
            for elem in feature_list:
                App.ActiveDocument.removeObject(elem.Name)

            for elem in body_list:
                App.ActiveDocument.removeObject(elem.Name)
            self.tab3 = self.obj_MainWidget.GeomInput['tab3']
            self.A  = ((self.obj_MainWidget.GeomInput['tab3'])['values'])['Wdo'] + ((self.obj_MainWidget.GeomInput['tab3'])['values'])['G']    # = Dk + Lr Wdo+G
            self.y_incr = self.A*sqrt(3)/2 
            self.Dk = ((self.obj_MainWidget.GeomInput['tab3'])['values'])['Wdo']
            self.Dw = ((self.obj_MainWidget.GeomInput['tab3'])['values'])['Wd']

            self.point_collection = []

            self.Bd_Wires_Dw = []

            self.Bd_InsLay_Dwo = []
            self.Bd_InsLay_Dw = []

            self.Bd_InsComp_Gr = []
            self.Bd_InsComp_Dwo = []

            if self.obj_MainWidget.GeomInput['groove'] == 'Gr1':
                self.gr_cont_pts = self.groove_contour(App.ActiveDocument.getObjectsByLabel("Sketch006")[0])

            elif self.obj_MainWidget.GeomInput['groove'] == 'Gr2':
                self.gr_cont_pts = self.groove_contour(App.ActiveDocument.getObjectsByLabel("Sketch006")[0])

            self.Bd_Points = App.ActiveDocument.addObject('PartDesign::Body','Bd_Points')
            self.Bd_Points.Placement.Base = self.v_gr_base

            self.Bd_Wires = App.ActiveDocument.addObject('PartDesign::Body','Bd_Wires')
            self.Bd_InsLay = App.ActiveDocument.addObject('PartDesign::Body','Bd_InsLay')
            self.Bd_InsComp = App.ActiveDocument.addObject('PartDesign::Body','Bd_InsComp')

            self.wloc_in_groove()

            App.ActiveDocument.recompute()
            return True
        except:
            return False

    def createGeom(self):
        ''' kicsit hosszu, de egy teljes, megbonthatatlan szekvencia '''
        #try:
        guide1 = [] 
        guide2 = []
        spline1_pts = []
        spline2_pts = []
        pl = App.Placement()
        Bd_InsLay_spl = []

        print('1')

        coreL = App.ActiveDocument.getObject('DatumPlane001').Placement.Base.z
        test1 = App.ActiveDocument.getObject('Bd_Guide')
        items = []	
        pt_data=()	
        sp2_counter = 0
        counter_act = 0
        dist = 0.0
        divider = int(0.1*coreL) 
        Ls_points = []	
        Ls_curves = []
        tmp = []
        print('2')
        self.Ymax = float(App.ActiveDocument.getObjectsByLabel("Sketch006")[0].getDatum("Ymax"))
        self.Ymid = float(App.ActiveDocument.getObjectsByLabel("Sketch006")[0].getDatum("Ymid"))

        for step in [0,0.1,0.5,0.9,0.92,0.94,0.96,0.98,0.99,1,1.02]:
            guide1.append(App.Vector(0,self.Ymid,coreL * step))
            guide2.append(App.Vector(0,self.Ymax,coreL * step))
        print('3')
        App.ActiveDocument.recompute()
        pts = App.ActiveDocument.getObjectsByLabel("Sketch010")[0].Shape.discretize(int(App.ActiveDocument.getObjectsByLabel("Sketch010")[0].Shape.Length))
        for pt in pts:
                guide1.append(pt)
        pts = App.ActiveDocument.getObjectsByLabel("Sketch011")[0].Shape.discretize(int(App.ActiveDocument.getObjectsByLabel("Sketch011")[0].Shape.Length))
        for pt in pts:
                guide2.append(pt)
        print('4')
        spline1 = Draft.makeBSpline(guide1,closed=False,face=False,support=None)
        spline2 = Draft.makeBSpline(guide2,closed=False,face=False,support=None)
        App.ActiveDocument.recompute()
        spline1_pts = spline1.Shape.discretize(int(spline1.Shape.Length )) 
        spline2_pts = spline2.Shape.discretize(int(spline2.Shape.Length /0.5))
        App.ActiveDocument.removeObject(spline1.Name)
        App.ActiveDocument.removeObject(spline2.Name)
        App.ActiveDocument.recompute()

        """ Draft.makeWire(spline1_pts)         #-----------------------------------------bemutatohoz
        Draft.makeWire(spline2_pts)
        App.ActiveDocument.recompute()
        raise Exception ("---")  """                       

        BD_points = App.ActiveDocument.getObject('Bd_Points')

        for item in BD_points.OutList:
            if (item.Name).find('point') >= 0:
                Ls_points.append(item)
        Bd_curvesPoints = App.ActiveDocument.addObject('PartDesign::Body','Bd_curvesPoints')        #---------------------bemutatohoz

        firstLoop = True

        for index, item in enumerate(spline1_pts):
            pt_data=[]	
            if index +1 < len(spline1_pts):
                subtr = item.sub(spline2_pts[counter_act])
                dist = sqrt(subtr.x*subtr.x+subtr.y*subtr.y+subtr.z*subtr.z)
                sp2_counter= counter_act 
                while sp2_counter < counter_act+divider+1 and sp2_counter < len(spline2_pts):
                    subtr = item.sub(spline2_pts[sp2_counter])
                    if sqrt(subtr.x*subtr.x+subtr.y*subtr.y+subtr.z*subtr.z) < dist:
                        dist = sqrt(subtr.x*subtr.x+subtr.y*subtr.y+subtr.z*subtr.z)
                        counter_act = sp2_counter
                    else:
                        pass
                    sp2_counter += 1

                if item.z > 0.1*coreL:
                    divider = int(0.49*coreL)
                if item.z > 0.5*coreL:
                    divider = int(0.89*coreL)
                if item.z > 0.95*coreL:
                    divider = int(0.01*coreL)
                if item.z > 1.02*coreL:
                    divider = 5
                if self.plane_h - item.z < 0.02*self.plane_h:
                        divider = 5

                if not index%divider or index == len(spline1_pts)-2:
                    pt_data.append(item)
                    pt_data.append(spline2_pts[counter_act])
                    pt_data.append(spline1_pts[index+1].sub(item))
                    items.append(pt_data)

                    quat1 = self.def_quaternion(App.Vector(0,1,0),pt_data[1].sub(pt_data[0]), True)
                    mx_rot1_inv = (quat1.inverse).rotation_matrix
                    vect1= App.Vector(mx_rot1_inv.dot(pt_data[2]))
                    vect2 = App.Vector(np.insert(np.delete(vect1,1,False),1,0,False))
                
                    quat2 = self.def_quaternion(App.Vector(0,0,1),vect2,True)

                    BD_points.Placement.Base = pt_data[0]
                    BD_points.Placement.Rotation = self.quat_rot(quat1*quat2)
                    App.ActiveDocument.recompute()

                    for index, point in enumerate(Ls_points):
                        if firstLoop:
                            tmp = []
                            tmp.append(point.getGlobalPlacement().Base)
                            Ls_curves.append(tmp)

                        if not firstLoop:
                            Ls_curves[index].append(point.getGlobalPlacement().Base)

                    firstLoop = False

        for curve in Ls_curves:          #  #pontok megjelenitese, Bd-t is bekapcsolni   #---------------------bemutatohoz    
            for pt in curve: 
                pt2 = Bd_curvesPoints.newObject('PartDesign::Point','pt')
                pt2.Placement.Base = pt
        App.ActiveDocument.recompute()


        for curvepoints in Ls_curves:
            spl_Wires = Draft.makeBSpline(curvepoints,closed=False,face=False,support=None)
            self.Bd_Wires_spl.append(spl_Wires)
            self.Bd_Wires.addObject(spl_Wires)
        raise Exception ("---")
        App.ActiveDocument.recompute()
        
        spl_Insul = Draft.makeBSpline(curvepoints,closed=False,face=False,support=None)
        Bd_InsLay_spl.append(spl_Insul)
        self.Bd_InsLay.addObject(spl_Insul)
        App.ActiveDocument.recompute()            


        pl.Base = self.v_gr_base
        pl.Rotation=(0,0,0,1)
        rmax = (self.Ymax-self.v_gr_base[1])*1.2    # 
        circ_Wires = Draft.makeCircle(radius=rmax,placement=pl,face=False,support=None)
        self.Bd_Wires.addObject(circ_Wires)

        pl = BD_points.Placement
        circ_Insul = Draft.makeCircle(radius=rmax,placement=pl,face=False,support=None)
        self.Bd_InsLay.addObject(circ_Insul)
        App.ActiveDocument.recompute()

        pad1 = self.Bd_Wires.newObject("PartDesign::Pad","Pad")
        pad1.Profile = circ_Wires
        pad1.Length = 2
        pad1.Reversed = 1
        App.ActiveDocument.recompute()

        for index, item in enumerate(self.Bd_Wires_spl):
            print(index+1, ' form ',len(self.Bd_Wires_spl), ' wires' )

            adPipeWire = self.Bd_Wires.newObject("PartDesign::AdditivePipe","AdditivePipe")
            adPipeWire.Profile = self.Bd_Wires_Dw[index]

            adPipeWire.Spine =item, ['Edge1']
            adPipeWire.Mode= 'Auxiliary'
            adPipeWire.AuxilleryCurvelinear = False
            adPipeWire.AuxillerySpineTangent = False

            if not index:
                adPipeWire.AuxillerySpine =  (self.Bd_Wires_spl[1], ['Edge1'])
            else:
                adPipeWire.AuxillerySpine =  (self.Bd_Wires_spl[index-1], ['Edge1'])
            App.ActiveDocument.recompute()
        
        Gui.ActiveDocument.getObject(self.Bd_Wires.Name).Visibility=False

        pad2 = self.Bd_InsLay.newObject("PartDesign::Pad","Pad")
        pad2.Profile = circ_Insul
        pad2.Length = 2
        pad2.Reversed = 0
        App.ActiveDocument.recompute()

        for index, item in enumerate(Bd_InsLay_spl):
            print(index+1, ' form ',len(Bd_InsLay_spl), ' insulation layers 1/2' )

            adPipeWire = self.Bd_InsLay.newObject("PartDesign::AdditivePipe","AdditivePipe")
            adPipeWire.Profile = self.Bd_InsLay_Dwo[index] 

            adPipeWire.Spine =item, ['Edge1']
            
            adPipeWire.Mode= 'Auxiliary'
            adPipeWire.AuxilleryCurvelinear =False
            adPipeWire.AuxillerySpineTangent = False
            if not index:
                adPipeWire.AuxillerySpine =  (Bd_InsLay_spl[1], ['Edge1'])
            else:
                adPipeWire.AuxillerySpine =  (Bd_InsLay_spl[index-1], ['Edge1'])
            
            App.ActiveDocument.recompute()

        for index, item in enumerate(Bd_InsLay_spl):
            print(index+1, ' form ',len(Bd_InsLay_spl), ' insulation layers 2/2' )

            adPipeWire = self.Bd_InsLay.newObject("PartDesign::SubtractivePipe","SubtractivePipe")
            adPipeWire.Profile = self.Bd_InsLay_Dw[index]

            adPipeWire.Spine =item, ['Edge1']

            adPipeWire.Mode= 'Auxiliary'
            adPipeWire.AuxilleryCurvelinear = False
            adPipeWire.AuxillerySpineTangent = False
            if not index:
                adPipeWire.AuxillerySpine =  (Bd_InsLay_spl[1], ['Edge1'])
            else:
                adPipeWire.AuxillerySpine =  (Bd_InsLay_spl[index-1], ['Edge1'])

            App.ActiveDocument.recompute()

        Gui.ActiveDocument.getObject(self.Bd_InsLay.Name).Visibility=False

        sk1 = App.ActiveDocument.getObjectsByLabel('grooveFull')[0] 
        pts1 = sk1.Shape.discretize(int(sk1.Shape.Length/0.04))
        wire = Draft.makeWire(pts1,face=False)
        App.ActiveDocument.getObject('Bd_InsComp').addObject(wire)
        pad = App.ActiveDocument.getObject('Bd_InsComp').newObject('PartDesign::Pad','Pad')
        pad.Profile = App.ActiveDocument.getObject(wire.Name)
        pad.Length = (self.tab1['values'])['L']
        
        App.ActiveDocument.recompute()


        for item in self.Bd_InsComp_Dwo:
            pad = App.ActiveDocument.getObject('Bd_InsComp').newObject('PartDesign::Pocket','Pocket')
            pad.Profile = App.ActiveDocument.getObject(item.Name)
            pad.Length = (self.tab1['values'])['L']
            pad.Reversed = 1
        
        App.ActiveDocument.recompute()

        Gui.ActiveDocument.getObject("Pocket001").Visibility=True 
        App.ActiveDocument.getObjectsByLabel('Sketch006')[0]
        Gui.ActiveDocument.getObject(App.ActiveDocument.getObjectsByLabel('Sketch006')[0].Name).Visibility=False
        Gui.ActiveDocument.getObject(App.ActiveDocument.getObjectsByLabel('StatCore0')[0].Name).Visibility=False
        
        Gui.ActiveDocument.getObject(self.Bd_Wires.Name).Visibility=True
        Gui.ActiveDocument.getObject(self.Bd_InsLay.Name).Visibility=True
        Gui.ActiveDocument.getObject(self.Bd_InsComp.Name).Visibility=True

        return True
        #except:
        return False

    def def_quaternion(self,v1_, v2_, quat = False):
        ''' v1_, v2_ App.Vector, egyikbol a masikba forgato quaterniont allitja elo,
        quat True-ra quaternionba, Flase-ra FreeCAD Rotation-ban '''
        v1 = deepcopy(v1_)
        v2 = deepcopy(v2_)
        v1.normalize(), v2.normalize()

        if(abs(v1.dot(v2)-1) < 0.0001):
            new_q = Quaternion(axis=[0, 0, 1], degrees=0)
            if quat:
                return new_q
            else:
                return_tuple = (round(new_q[1],6),round(new_q[2],6),round(new_q[3],6),round(new_q[0],6))
                return return_tuple

        elif(abs(v1.dot(v2)+1) < 0.0001):
            new_q=(Quaternion(axis=[0, 0, 1], degrees=0)).inverse
            if quat:
                return new_q
            else:
                return_tuple = (round(new_q[1],6),round(new_q[2],6),round(new_q[3],6),round(new_q[0],6))
                return return_tuple

        else:
            v = v1+v2
            v.normalize()
            x_vect = v1.cross(v2)
            q_w = sqrt((pow(v1.Length,2)) * (pow(v2.Length,2))) + v1.dot(v2)
            new_q = Quaternion(q_w, x_vect[0], x_vect[1], x_vect[2])
            if quat:
                return new_q
            else:
                return_tuple = (round(new_q[1],6),round(new_q[2],6),round(new_q[3],6),round(new_q[0],6))
                return return_tuple


    def quat_rot(self,quat):
        ''' Quaterniont alakit FreeCAD Rotation-re '''
        if type(quat) == Quaternion:
            return_tuple = (round(quat[1],6),round(quat[2],6),round(quat[3],6),round(quat[0],6))
            return return_tuple
        else:
            return None

    def groove_contour(self, cont):
        ''' Az atadott konturt diszkretizalja 0,6 mm-es szakaszokra es a keletkezett pontokat visszaadja '''
        App.ActiveDocument.recompute()
        Shp = cont.Shape 
        return Shp.discretize(int(Shp.Length/0.6))

    def wloc_in_groove(self):
        ''' hozalpoziciok szamlaloja '''
        x=0
        y=0
        y_sign = 1
        condition1 = True
        condition2 = True

        while condition1:
            condition1 = (y>=0)
            while condition2:
                condition2 = False
                while self.wire_condition(x,y):
                    condition2 = True
                    x += 1
                x=0
                y+=(1*y_sign)
            y_sign = -1
            y = y_sign
            condition2 = True


    def wire_condition(self,x,y):
        ''' x,y koordinataju pont kore a kulso atmerovel rajzolt korrol megallapitja,
        hogy a hornyon belul helyezkedik-e el. Ha igen, elhelyezi egy adatszerkezetben
        a pontot es a szukseges koroket a geometria elkeszitesehez '''
        pnts = []
        if y%2:
            x_circ = (x + 0.5)*self.A
            y_circ = y*self.y_incr
        else:
            x_circ = x*self.A
            y_circ = y*self.y_incr

        pl = App.Placement()
        pl.Rotation=(0,0,0,1)
        pl.Base=App.Vector(x_circ,y_circ+self.v_gr_base[1],0)
        circ = Draft.makeCircle(radius=self.Dk/2,placement=pl,face=False,support=None)
        App.ActiveDocument.recompute()
        circ_cont = circ.Shape.discretize(int(circ.Shape.Length/0.1))
        for pnt_ in circ_cont:
            pnts.append((pnt_[0],pnt_[1],pnt_[2]))

        App.ActiveDocument.recompute()

        if Polygon(self.gr_cont_pts).contains(Polygon(pnts)):
            self.Bd_InsLay_Dwo.append(circ)
            self.Bd_InsLay.addObject(self.Bd_InsLay_Dwo[-1])            
            
            circ = Draft.makeCircle(radius=self.Dk/2,placement=pl,face=False,support=None)
            self.Bd_InsComp_Dwo.append(circ)
            self.Bd_InsComp.addObject(self.Bd_InsComp_Dwo[-1])

            circ = Draft.makeCircle(radius=self.Dw/2,placement=pl,face=False,support=None)
            self.Bd_Wires_Dw.append(circ)
            self.Bd_Wires.addObject(self.Bd_Wires_Dw[-1])

            circ = Draft.makeCircle(radius=self.Dw/2,placement=pl,face=False,support=None)
            self.Bd_InsLay_Dw.append(circ)
            self.Bd_InsLay.addObject(self.Bd_InsLay_Dw[-1])

            pl.Base.y -= self.v_gr_base[1]
            self.point_collection.append(self.Bd_Points.newObject('PartDesign::Point','point'))
            self.point_collection[-1].Placement = pl
            pl.Base.y += self.v_gr_base[1]

            if x_circ != 0:
                pl = App.Placement()
                pl.Rotation=(0,0,0,1)
                pl.Base=App.Vector(-x_circ,y_circ+self.v_gr_base[1],0)

                circ = Draft.makeCircle(radius=self.Dk/2,placement=pl,face=False,support=None)
                self.Bd_InsLay_Dwo.append(circ)
                self.Bd_InsLay.addObject(self.Bd_InsLay_Dwo[-1])            
                
                circ = Draft.makeCircle(radius=self.Dk/2,placement=pl,face=False,support=None)
                self.Bd_InsComp_Dwo.append(circ)
                self.Bd_InsComp.addObject(self.Bd_InsComp_Dwo[-1])

                circ = Draft.makeCircle(radius=self.Dw/2,placement=pl,face=False,support=None)
                self.Bd_Wires_Dw.append(circ)
                self.Bd_Wires.addObject(self.Bd_Wires_Dw[-1])

                self.obj_MainWidget.countOfWires = len(self.Bd_Wires_Dw)

                circ = Draft.makeCircle(radius=self.Dw/2,placement=pl,face=False,support=None)
                self.Bd_InsLay_Dw.append(circ)
                self.Bd_InsLay.addObject(self.Bd_InsLay_Dw[-1])

                pl.Base.y -= self.v_gr_base[1]
                self.point_collection.append(self.Bd_Points.newObject('PartDesign::Point','point'))
                self.point_collection[-1].Placement = pl

        else:
            App.ActiveDocument.removeObject(circ.Name)
            return False
        App.ActiveDocument.recompute()
        return True


'''     def circ_contour(self,x,y,r):
        Megrajzol egy kort az adott pontban es sugarral
        pl = App.Placement()
        pl.Rotation.Q=(0,0,0,1)
        pl.Base=App.Vector(x,y+self.v_gr_base[1],0)
        
        return Draft.makeCircle(radius=r,placement=pl,face=False,support=None) '''