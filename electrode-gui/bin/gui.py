#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, BOTH
import Tkinter as tk
from ttk import Frame, Button, Style, Checkbutton, Label, Entry
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import numpy as np
import nibabel as nib
from os import path
import os
import sys
sys.path.append(path.abspath('../util'))
from ct2mip import ct2mip
from mip2vox import mip2vox
from interpol import interpol
from geodesic3D_hybrid_lite import geodesic3D_hybrid
from elec_snap import elec_snap

DATA_DIR = '../tests/test_ct2mip/data/'
patient_id = 'HUP64'

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)  
        self.parent = parent
        self.press = None
        self.load_frame()
        self.load_mip()
        self.plot_mip()

        global var1
        var1 = tk.BooleanVar()    
        rotateButton = Checkbutton(self, text = "Rotate", variable = var1, command=self.checkbutton_value)
        rotateButton.place(x=200, y=0)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=0, y=0)

        interpolButton = Button(self, text="Interpolate!", command=self.interpolate)
        interpolButton.place(x=0, y=40)

        resetButton = Button(self, text="Reset", command=self.resett)
        resetButton.place(x=0, y=80)

        logo_path = '%s/logo.png'%(DATA_DIR)
        logo = Image.open(logo_path)
        logo = ImageTk.PhotoImage(logo)
        label1 = Label(self, image=logo)
        label1.place(x=470, y=0)
        label1.image = logo

        label_a = Label(self, text= "A:")
        label_a.place(x=190, y=20)
        global coord_a
        coord_a = Entry(self)
        coord_a.place(x=200, y=20)
        label_b = Label(self, text= "B:")
        label_b.place(x=190, y=40)
        global coord_b
        coord_b = Entry(self)
        coord_b.place(x=200, y=40)
        label_c = Label(self, text= "C:")
        label_c.place(x=190, y=60)
        global coord_c
        coord_c = Entry(self)
        coord_c.place(x=200, y=60)
        label_d = Label(self, text= "D:")
        label_d.place(x=190, y=80)
        global coord_d
        coord_d = Entry(self)
        coord_d.place(x=200, y=80)

        global count
        count = 0

    def load_frame(self):
        self.parent.title("Electrode GUI")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        
    def load_mip(self):

        # dilation_command = '$ANTSPATH/ImageMath 3 %s_BrainExtractionMaskDilated.nii.gz MD %s_BrainExtractionMask.nii.gz 1'%(patient_id, patient_id)
        # os.system(dilation_command)

        ct_filename = '%s/%s_CTIEEG_deformed.nii.gz'%(DATA_DIR, patient_id)
        # ct_filename = '%s/%s_unburied_electrode_seg.nii.gz'%(DATA_DIR, patient_id)
        img = nib.load(os.path.expanduser(ct_filename))
        global ct_data
        ct_data = img.get_data()

        ## IN REAL CODE CHANGE THE NAME OF THE MASK TO 'BrainExtractionMaskDilated.nii.gz'
        mask_filename = '%s/%s_BrainSegmentationMaskDilated.nii.gz'%(DATA_DIR, patient_id)
        # mask_filename = '%s/%s_brain_mask.nii.gz'%(DATA_DIR, patient_id)
        img = nib.load(os.path.expanduser(mask_filename))
        global mask_data
        mask_data = img.get_data()
        mask_data_inv = mask_data.astype(bool)
        mask_data_inv = np.invert(mask_data_inv)

        np.copyto(ct_data, mask_data, where=mask_data_inv)

    def plot_mip(self):

        global theta
        global phi
        theta = 0
        phi = 0
        mip = ct2mip(ct_data, 1, theta, phi)

        f = Figure(figsize=(5,5), dpi=100)
        global a
        a = f.add_subplot(111)
        a.imshow(mip)

        global canvas
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def drag_mip(self):
        self.cidpress = canvas.mpl_connect('button_press_event', self.on_press)
        self.cidmotion = canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cidrelease = canvas.mpl_connect('button_release_event', self.on_release)

    def stop_drag_mip(self):
        canvas.mpl_disconnect(self.cidpress)
        canvas.mpl_disconnect(self.cidmotion)
        canvas.mpl_disconnect(self.cidrelease)

    def on_press(self, event):
        self.press = event.xdata, event.ydata

    def on_motion(self, event):
        try:
            xpress, ypress = self.press
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            theta = -dx * 0.5
            phi = dy * 0.5
            mip = ct2mip(ct_data, 1, theta, phi)
            a.imshow(mip)
            canvas.show()
        except Exception:
            pass

    def on_release(self, event):
        # on release we reset the press data
        xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        theta = -dx * 0.5
        phi = dy * 0.5
        mip = ct2mip(ct_data, 1, theta, phi)
        a.imshow(mip)
        canvas.show()
        self.press = None

    def checkbutton_value(self):
        if var1.get() == True:
           self.drag_mip()
           self.stop_click_mip()
        else:
            self.stop_drag_mip()
            self.click_mip()
    
    def on_click(self, event):
        if event.inaxes is not None:
            xcord, ycord = event.xdata, event.ydata
            xcord = round(xcord)
            ycord = round(ycord)
            global count
            count += 1
            if count == 1:
                global A
                A = (xcord, ycord)
                coord_a.insert(0, str(A))
            if count == 2:
                global B
                B = (xcord, ycord)
                coord_b.insert(0, str(B))
            if count == 3:
                global C
                C = (xcord, ycord)
                coord_c.insert(0, str(C))
            if count == 4:
                global D
                D = (xcord, ycord)
                coord_d.insert(0, str(D))
            if count == 5:
                coord_a.delete(0,12)
                coord_b.delete(0,12)
                coord_c.delete(0,12)
                coord_d.delete(0,12)
                count = 0
        else:
            print 'Clicked ouside axes bounds but inside plot window'

    def click_mip(self):
        self.mippress = canvas.mpl_connect('button_press_event', self.on_click)

    def stop_click_mip(self):
        canvas.mpl_disconnect(self.mippress)

    def interpolate(self):
        A_vox = mip2vox(A[0], A[1], theta, phi, ct_data)
        B_vox = mip2vox(B[0], B[1], theta, phi, ct_data)
        C_vox = mip2vox(C[0], C[1], theta, phi, ct_data)
        D_vox = mip2vox(D[0], D[1], theta, phi, ct_data)
        # elec_coord = geodesic3D_hybrid(A_vox, B_vox, D_vox, C_vox, 8, 8, mask_data)
        elec_coord = interpol(A_vox, B_vox, C_vox, 8, 8)
        snap_coords = elec_snap(elec_coord, ct_data)
        for point in snap_coords:
            ct_data[point[0]-2:point[0]+2, point[1]-2:point[1]+2, point[2]-2:point[2]+2] = 5000
        mip = ct2mip(ct_data, 1, theta, phi)
        a.imshow(mip)
        canvas.show()

    def resett(self):
        mip = ct2mip(ct_data, 1, 0, 0)
        a.imshow(mip)
        canvas.show()

def main():
    root = tk.Tk()
    root.geometry("800x800+300+300")
    app = Example(root)
    root.mainloop()  

if __name__ == '__main__':
    main()