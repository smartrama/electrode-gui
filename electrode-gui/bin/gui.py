#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, BOTH
import Tkinter as tk
from Tkinter import Grid
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
        self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.load_frame()
        self.load_mip()
        self.plot_mip()

        # Create rotate checkbutton
        global var1
        var1 = tk.BooleanVar()    
        rotateButton = Checkbutton(self, text = "Rotate", variable = var1, command=self.checkbutton_value1)
        rotateButton.grid(row=1, column=0, sticky=tk.E)

        # Create click checkbutton
        global var2
        var2 = tk.BooleanVar()    
        clickButton = Checkbutton(self, text = "Click", variable = var2, command=self.checkbutton_value2)
        clickButton.grid(row=1, column=1)

        # Create quit button
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.grid(row=0, column=0, sticky=tk.N+tk.W)

        # Create interpolate button
        interpolButton = Button(self, text="Interpolate!", command=self.interpolate)
        interpolButton.grid(row=3, column=0, sticky=tk.S+tk.W)

        # resetButton = Button(self, text="Reset", command=self.resett)
        # resetButton.grid(row=4,column=0)

        logo_path = '%s/logo.png'%(DATA_DIR)
        logo = Image.open(logo_path)
        logo = ImageTk.PhotoImage(logo)
        label1 = Label(self, image=logo)
        label1.grid(row=0, rowspan=4, column=4)
        label1.image = logo

        label_a = Label(self, text= "A:")
        label_a.grid(row=0, column=1, sticky=tk.E+tk.S)
        global coord_a
        coord_a = Entry(self)
        coord_a.grid(row=0, column=2, sticky=tk.W+tk.S)
        label_b = Label(self, text= "B:")
        label_b.grid(row=1, column=1, sticky=tk.E+tk.N)
        global coord_b
        coord_b = Entry(self)
        coord_b.grid(row=1, column=2, sticky=tk.W+tk.N)
        label_c = Label(self, text= "C:")
        label_c.grid(row=2, column=1, sticky=tk.E+tk.N)
        global coord_c
        coord_c = Entry(self)
        coord_c.grid(row=2, column=2, sticky=tk.W+tk.N)
        label_d = Label(self, text= "D:")
        label_d.grid(row=3, column=1, sticky=tk.E+tk.N)
        global coord_d
        coord_d = Entry(self)
        coord_d.grid(row=3, column=2, sticky=tk.W+tk.N)

        global count
        count = 0

    def load_frame(self):
        self.parent.title("Electrode GUI")
        self.style = Style()
        self.style.theme_use("default")
        self.grid()
        
    def load_mip(self):

        # dilation_command = '$ANTSPATH/ImageMath 3 %s_BrainExtractionMaskDilated.nii.gz MD %s_BrainExtractionMask.nii.gz 1'%(patient_id, patient_id)
        # os.system(dilation_command)

        ct_filename = '%s/%s_CTIEEG_deformed.nii.gz'%(DATA_DIR, patient_id)
        img = nib.load(os.path.expanduser(ct_filename))
        global ct_data
        ct_data = img.get_data()

        ## IN REAL CODE CHANGE THE NAME OF THE MASK TO 'BrainExtractionMaskDilated.nii.gz'
        mask_filename = '%s/%s_BrainSegmentationMaskDilated.nii.gz'%(DATA_DIR, patient_id)
        img = nib.load(os.path.expanduser(mask_filename))
        global mask_data
        mask_data = img.get_data()
        mask_data_inv = mask_data.astype(bool)
        mask_data_inv = np.invert(mask_data_inv)

        np.copyto(ct_data, mask_data, where=mask_data_inv)

        global min_z
        global min_y
        global min_x
        global max_z
        global max_y
        global max_x
        boundary = np.argwhere(mask_data == 1)
        min_x = min(boundary[::,0])
        min_y = min(boundary[::,1])
        min_z = min(boundary[::,2])
        max_x = max(boundary[::,0])
        max_y = max(boundary[::,1])
        max_z = max(boundary[::,2])

    def plot_mip(self):

        global theta
        global phi
        theta = 0
        phi = 0
        mip = ct2mip(ct_data, 1, theta, phi)

        global wind
        wind = 50

        f1 = Figure(figsize=(3,3), dpi=100)
        global a
        a = f1.add_subplot(111)
        a.xaxis.set_visible(False)
        a.yaxis.set_visible(False)
        a.imshow(mip)

        f2 = Figure(figsize=(1,1), dpi=100)
        global b
        b = f2.add_subplot(111)
        b.xaxis.set_visible(False)
        b.yaxis.set_visible(False)
        b.imshow(np.zeros((wind*2,wind*2)))

        f3 = Figure(figsize=(1,1), dpi=100)
        global c
        c = f3.add_subplot(111)
        c.xaxis.set_visible(False)
        c.yaxis.set_visible(False)
        c.imshow(np.zeros((wind*2,wind*2)))

        f4 = Figure(figsize=(1,1), dpi=100)
        global d
        d = f4.add_subplot(111)
        d.xaxis.set_visible(False)
        d.yaxis.set_visible(False)
        d.imshow(np.zeros((wind*2,wind*2)))

        global canvas
        canvas = FigureCanvasTkAgg(f1, self)
        canvas.show()
        canvas.get_tk_widget().grid(row=4, rowspan=3, column=1, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W)

        global canvas2
        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.show()
        canvas2.get_tk_widget().grid(row=4, rowspan=1, column=4, columnspan=1, sticky=tk.N+tk.E+tk.S+tk.W)

        global canvas3
        canvas3 = FigureCanvasTkAgg(f3, self)
        canvas3.show()
        canvas3.get_tk_widget().grid(row=5, rowspan=1, column=4, columnspan=1, sticky=tk.N+tk.E+tk.S+tk.W)

        global canvas4
        canvas4 = FigureCanvasTkAgg(f4, self)
        canvas4.show()
        canvas4.get_tk_widget().grid(row=6, rowspan=1, column=4, columnspan=1, sticky=tk.N+tk.E+tk.S+tk.W)

        for x in xrange(4):
            self.columnconfigure(x, weight=1)
        for y in xrange(4,8):
            self.rowconfigure(y, weight=1)

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

    def checkbutton_value1(self):
        if var1.get() == True:
           self.drag_mip()
           self.stop_click_mip()
           var2.set(False)

    def checkbutton_value2(self):
        if var2.get() == True:
            self.stop_drag_mip()
            self.click_mip()
            var1.set(False)
    
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
                global A_vox
                A_vox = mip2vox(A[0], A[1], theta, phi, ct_data)
                b.imshow(ct_data[A_vox[0],
                                min_y:max_y,
                                min_z:max_z], cmap="Greys_r")
                canvas2.show()
                c.imshow(ct_data[min_x:max_x,
                                A_vox[1],
                                min_z:max_z], cmap="Greys_r")
                canvas3.show()
                d.imshow(ct_data[min_x:max_x,
                                min_y:max_y,
                                A_vox[2]], cmap="Greys_r")
                canvas4.show()
            if count == 2:
                global B
                B = (xcord, ycord)
                coord_b.insert(0, str(B))
                global B_vox
                B_vox = mip2vox(B[0], B[1], theta, phi, ct_data)
                b.imshow(ct_data[B_vox[0],
                                min_y:max_y,
                                min_z:max_z], cmap="Greys_r")
                canvas2.show()
                c.imshow(ct_data[min_x:max_x,
                                B_vox[1],
                                min_z:max_z], cmap="Greys_r")
                canvas3.show()
                d.imshow(ct_data[min_x:max_x,
                                min_y:max_y,
                                B_vox[2]], cmap="Greys_r")
                canvas4.show()
            if count == 3:
                global C
                C = (xcord, ycord)
                coord_c.insert(0, str(C))
                global C_vox
                C_vox = mip2vox(C[0], C[1], theta, phi, ct_data)
                b.imshow(ct_data[C_vox[0],
                                min_y:max_y,
                                min_z:max_z], cmap="Greys_r")
                canvas2.show()
                c.imshow(ct_data[min_x:max_x,
                                C_vox[1],
                                min_z:max_z], cmap="Greys_r")
                canvas3.show()
                d.imshow(ct_data[min_x:max_x,
                                min_y:max_y,
                                C_vox[2]], cmap="Greys_r")
                canvas4.show()
            if count == 4:
                global D
                D = (xcord, ycord)
                coord_d.insert(0, str(D))
                global D_vox
                D_vox = mip2vox(D[0], D[1], theta, phi, ct_data)
                b.imshow(ct_data[D_vox[0],
                                min_y:max_y,
                                min_z:max_z], cmap="Greys_r")
                canvas2.show()
                c.imshow(ct_data[min_x:max_x,
                                D_vox[1],
                                min_z:max_z], cmap="Greys_r")
                canvas3.show()
                d.imshow(ct_data[min_x:max_x,
                                min_y:max_y,
                                D_vox[2]], cmap="Greys_r")
                canvas4.show()
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
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%sx%s+300+300"%(width, height))
    app = Example(root)
    root.mainloop()  

if __name__ == '__main__':
    main()