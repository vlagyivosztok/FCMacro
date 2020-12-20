class ParametricRectangle:
    def __init__(self,obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyFloat","Length")
        obj.addProperty("App::PropertyFloat","Width")
 
    def execute(self,obj):
        import Part,FreeCAD
        if(obj.Length == 0) or (obj.Width == 0):
            return
            
        v1 = FreeCAD.Vector(0,0,0)
        v2 = FreeCAD.Vector(obj.Length, 0,0)
        v3 = FreeCAD.Vector(obj.Length, obj.Width,0)
        v4 = FreeCAD.Vector(0,obj.Width,0)
        
        e1 = Part.Line(v1,v2).toShape()
        e2 = Part.Line(v2,v3).toShape()
        e3 = Part.Line(v3,v4).toShape()
        e4 = Part.Line(v4,v1).toShape()
        
        w = Part.Wire([e1,e2,e3,e4])
        
        f = Part.Face(w)
        
        f.Placement = obj.Placement
        
        obj.Shape = f
        
               