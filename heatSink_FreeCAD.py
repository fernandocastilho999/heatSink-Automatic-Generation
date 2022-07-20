# import libraries
import FreeCAD, Draft
import numpy as np

# A) Data
# number of fins
a = 4; b = 8
for j in np.arange(b-a+1):
    N = j + a 
    # Operating conditions
    Pow = 20. # [W]
    LPM = 25. # [LPM]
    # a = 2; b = 20
    # geometric data
    H = 0.076;  L = .105; W = .044
    Hf = .06; Hb = H - Hf
    rtb = 0.6
    # velocity and air properties
    Ts = 80 ; Too=20 ; ks = 237 
    rho = 1 ; mu = 18.1e-6 ; Pr = 0.7 ; ka = 26e-3

    # B) Geometric Calculations
    b = L / ( N*(rtb+1)-1 )
    t = b*rtb

    # C) Create Document
    name = "heatSink"
    App.newDocument(name)
    App.setActiveDocument(name)
    App.ActiveDocument=App.getDocument(name)
    Gui.ActiveDocument=Gui.getDocument(name)

    spec = ('-'+str("{:02d}".format(N))+'f')
    # D) Draw Base
    R1 = Draft.makeRectangle(L,W) ; #R1.label = 'rect1'
    B = Draft.extrude(R1, FreeCAD.Vector(0, 0, H)) ; B.Label = 'base'

    # E) Draw Fins
    for i in range(N-1):
        R2 = Draft.makeRectangle(b,W) 
        R2 = Draft.move(R2, FreeCAD.Vector( i*(t+b) + t, 0 , H ) ) ; R2.Label = 'rect2'
        FS = Draft.extrude(R2, FreeCAD.Vector(0, 0, -Hf)) ; FS.Label = 'finSpace'
        HS = Draft.cut(B,FS) ; HS.Label = 'finCut'
        B = HS
    B.Label = 'heatSink'
    ###########################################################33

    # Recalculate and show Axometric View
    App.activeDocument().recompute()
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")
    # Save file
    dir = "/home/fernando/workspace/engineering/freecad/out/"
    fname = dir+name+spec
    
    # Delete old Files
    import os
    if os.path.exists(fname+".FCStd"): os.remove(fname+".FCStd") 
    else: pass
    App.getDocument(name).saveAs(fname+".FCStd")

    # Export file 
    Part.export([B], fname+'.stp')
    Part.export([B], fname+'.stl')
    # Close file
    App.closeDocument(name)
