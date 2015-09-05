################################
# Author   : septicmk
# Date     : 2015/09/05 16:57:57
# FileName : visualization.py
################################

import sys
sys.path.append('/home/liuyao/VTK-6.2.0-Linux-64bit/bin')
from vtkpython import *
import math
import pandas as pd
from random import random

class vtkTimerCallback():
   def __init__(self):
       self.timer_count = 0
 
   def execute(self,obj,event):
       #print self.timer_count
       celllist = self.dataset[self.timer_count]
       for i in range(len(self.actorlist)):
           print str(i) + " " +  str(celllist[i]['pos'][0]) + " " + str(celllist[i]['pos'][1]) + " " + str(celllist[i]['pos'][2])
           self.actorlist[i].SetPosition(float(celllist[i]['pos'][0]),float(celllist[i]['pos'][1]),float(celllist[i]['pos'][2]));
           #self.actorlist[i].SetPosition(random()*20,random()*20,random()*20)
       iren = obj
       iren.GetRenderWindow().Render()
       self.timer_count += 1

class Visualization:
    
    def __init__(self):
        '''
        '''
        self.cell_table = pd.read_pickle("cell_table.pkl")
        self.cell_table.to_csv("cell_tabel.csv")
    def makeCells(self):
        '''
        using dataset to get cell list.
          return: A List consisting of [vtkActor]
        '''
        cellactorlist = []
        for i, row in self.cell_table.iterrows():
            spheresrc = vtk.vtkSphereSource()
            spheresrc.SetCenter(row[u'x'],row[u'y'],row[u'z']*7)
            spheresrc.SetRadius(row[u'size'])
            spheresrc.SetPhiResolution(25)
            spheresrc.SetThetaResolution(25)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(spheresrc.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            cellactorlist.append(actor)
        return cellactorlist
       
    def export2AVI(self):
        '''
        render the scence then export it to an AVI file
        '''
        
        cellactorlist = self.makeCells()
        # print len(cellactorlist) 
        ren = vtk.vtkRenderer()
        renwin = vtk.vtkRenderWindow()
        renwin.AddRenderer(ren)
        #iren = vtk.vtkRenderWindowInteractor()
        #iren.SetRenderWindow(renwin)
        
        for cellactor in cellactorlist:
            ren.AddActor(cellactor)
        
        ren.SetBackground(0,0,0,)
        renwin.SetSize(400,400)
        #iren.Initialize()
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(0.5)
        renwin.Render()
        #iren.Start()
        
        writer = vtk.vtkAVIWriter()
        w2i = vtk.vtkWindowToImageFilter()
        w2i.SetInput(renwin)
        writer.SetInputConnection(w2i.GetOutputPort())
        writer.SetFileName("cell_visualization.avi")
        
        writer.Start()
        for celllist in self.dataset:
            for i in range(len(cellactorlist)):
                cellactorlist[i].SetPosition(float(celllist[i]['pos'][0]),float(celllist[i]['pos'][1]),float(celllist[i]['pos'][2]))
            w2i.Modified()
            #writer.Write()
            writer.Write()
        writer.End()
        
    def debug(self):
        '''
        Debug
        '''
        cellactorlist = self.makeCells()
        # print len(cellactorlist) 
        ren = vtk.vtkRenderer()
        renwin = vtk.vtkRenderWindow()
        renwin.AddRenderer(ren)
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renwin)
        
        for cellactor in cellactorlist:
            ren.AddActor(cellactor)
        
        ren.SetBackground(0,0,0,)
        renwin.SetSize(400,400)
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(0.5)
        renwin.Render()
        iren.Initialize()
        #cb = vtkTimerCallback()
        #cb.actorlist = cellactorlist
        #cb.dataset = self.dataset
        #iren.AddObserver('TimerEvent', cb.execute)
        #timerId = iren.CreateRepeatingTimer(10)
        iren.Start()
        
if __name__ == '__main__':
    vis = Visualization()
    vis.debug()
    #vis.export2AVI()
