#!/usr/bin/env python

import eigenpy
eigenpy.switchToNumpyArray()

import subprocess
import time
import sys
sys.path.append('/home/lscherrer/workspace/install/lib/python3.6/site-packages/ospi')

import ospi.motion_parser as mtp
import ospi.viewer_utils as vw
import ospi.wrapper as wr

from pinocchio import RobotWrapper

# The path to the model meshes
mesh_path = 'models/whole_body/obj'
# The path to the model and the filename
filename = 'models/whole_body/wholebodyOLI.osim'
# Create a wrapper specific to the whole-body model
# The wrapper parse the OpenSim model and builds pinocchio model and data
wb_model = wr.Wrapper(filename, mesh_path, name='whole-body_model10')

# call the gepetto viewer server
gvs = subprocess.Popen('gepetto-gui')
print('Loading the viewer ...')
time.sleep(5)

# Init the viewer and add the model to it
"""viewer = vw.Viewer('viewer', wb_model)
viewer.setVisibility(wb_model.name + "/floor", "ON")
viewer.display(wb_model.q0, wb_model.name)"""

r = RobotWrapper(wb_model.model, collision_model = None, visual_model = wb_model.geom_model, verbose=False)
r.initViewer()
r.loadViewerModel("skeleton")
r.display(wb_model.q0)
time.sleep(10)
# Add the floor and scale it
r.viewer.gui.addFloor('hpp-gui/floor')
r.viewer.gui.setScale('hpp-gui/floor', [0.5, 0.5, 0.5])
r.viewer.gui.setColor('hpp-gui/floor', [0.7, 0.7, 0.7, 1.])
r.viewer.gui.setLightingMode('hpp-gui/floor', 'OFF')

# See axis
#r.viewer.JointFrames(wb_model.name)

# parse motion:
timeParser, q, colheaders, qOsim = mtp.parseMotion(wb_model.model, wb_model.joint_transformations, 'OLI_F_3.mot', 'quat')

#r.display(qOsim) # marche pas, a debugger
#time.sleep(10)

t = 0.0


def playMotions(first=0, last=1, step=3, t=0):
    for i in range(first, last, step):
        #viewer.setVisibility("OLI", "ON")
        #viewer.display(q[i].T, wb_model.name)
        r.display(q[i].T)
        time.sleep(0.01)


time.sleep(4)
playMotions(0, 396, 1, 0.0025)
#playMotions(0,100, 1, 0.0025)

time.sleep(4)
#gvs.terminate()
