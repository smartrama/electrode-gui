#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, BOTH
import Tkinter as tk
from ttk import Frame, Button, Style, Scale
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

        global count
        count = 0
        def on_click(event):
            if event.inaxes is not None:
                xcord, ycord = event.xdata, event.ydata
                global count
                count += 1

                if count == 1:
                    A = (xcord, ycord)
                    print 'A: %s' % str(A)
                if count == 2:
                    B = (xcord, ycord)
                    print 'B: %s' % str(B)
                if count == 3:
                    C = (xcord, ycord)
                    print 'C: %s' % str(C)
                if count == 4:
                    D = (xcord, ycord)
                    print 'D: %s' % str(D)
                if count == 5:
                    count = 0
            else:
                print 'Clicked ouside axes bounds but inside plot window'

        f.canvas.callbacks.connect('button_press_event', on_click)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=0, y=0)

        def theta_change(thet):
            global theta
            global phi
            theta = float(thet)
            mip = ct2mip(ct_data, 2, theta, phi)
            a.imshow(mip)
            canvas.show()

        def phi_change(ph):
            global theta
            global phi
            phi = float(ph)
            mip = ct2mip(ct_data, 2, theta, phi)
            a.imshow(mip)
            canvas.show()

        thet = 0
        theta_slider = Scale(self, from_=0, to=360, orient=tk.HORIZONTAL, command=theta_change, variable=thet)
        theta_slider.place(x=120, y=0) 

        ph = 0
        phi_slider = Scale(self, from_=0, to=360, orient=tk.HORIZONTAL, command=phi_change, variable=ph)
        phi_slider.place(x=120, y=30)  
        
def main():
  
    root = Tk()
    root.geometry("800x800+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()