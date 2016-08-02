#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, BOTH
import Tkinter as tk
from ttk import Frame, Button, Style
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import nibabel as nib
from os import path
import sys
sys.path.append(path.abspath('../../util'))
from ct2mip import ct2mip

DATA_DIR = 'data/'
patient_id = 'HUP64'
theta = 0
phi = 0

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("MIP")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        seg_filename = '%s/%s_unburied_electrode_seg.nii.gz'%(DATA_DIR, patient_id)
        img = nib.load(path.expanduser(seg_filename))
        ct_data = img.get_data()
        global theta
        global phi
        theta = 0
        phi = 0
        mip = ct2mip(ct_data, 2, theta, phi)

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.imshow(mip)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=0, y=0)

        def theta_changep():
            global theta
            global phi
            theta += 15    
            mip = ct2mip(ct_data, 2, theta, phi)
            a.imshow(mip)
            canvas.show()

        def theta_changem():
            global theta
            global phi
            theta -= 15    
            mip = ct2mip(ct_data, 2, theta, phi)
            a.imshow(mip)
            canvas.show()

        def phi_changep():
            global theta
            global phi
            phi += 15    
            mip = ct2mip(ct_data, 2, theta, phi)
            a.imshow(mip)
            canvas.show()

        def phi_changem():
            global theta
            global phi
            phi -= 15    
            mip = ct2mip(ct_data, 2, theta, phi)
            a.imshow(mip)
            canvas.show()

        theta_plus = Button(self, text="Theta +", command=theta_changep)
        theta_plus.place(x=120, y=0)
        theta_minus = Button(self, text="Theta -", command=theta_changem)
        theta_minus.place(x=240, y=0)
        phi_plus = Button(self, text="Phi +", command=phi_changep)
        phi_plus.place(x=120, y=30)
        phi_minus = Button(self, text="Phi -", command=phi_changem)
        phi_minus.place(x=240, y=30)

def main():
  
    root = Tk()
    root.geometry("800x800+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()