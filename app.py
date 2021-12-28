import tkinter as tk             # This has all the code for GUIs.
import tkinter.font as font      # This lets us use different fonts.
from tkinter import ttk


def center_window_on_screen():
    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))


def import_scanner():
    """
    :return: Nothing
    """


def import_GPS():
    """
    :return: Nothing
    """


def next():
    start_frame.forget()
    viewer_frame.pack(fill='both', expand=1)


def change_to_start():
    start_frame.pack(fill='both', expand=1)
    viewer_frame.forget()


def visualize3D():
    viewer_frame.forget()
    plot3D_frame.pack(fill='both', expand=1)


def back():
    viewer_frame.pack(fill='both', expand=1)
    plot3D_frame.forget()


def backgeo():
    viewer_frame.pack(fill='both', expand=1)
    geoRef_frame.forget()


def georef():
    plot3D_frame.forget()
    geoRef_frame.pack(fill='both', expand=1)


# set up the window
root = tk.Tk()
root.title("LIDAR point cloud viewer")
root.configure(bg='lightyellow')

# Set the icon used for your program
root.iconphoto(True,
               tk.PhotoImage(file='info.png'))

width, height = 600, 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_window_on_screen()

# create two frames
start_frame = tk.Frame(root)
viewer_frame = tk.Frame(root)
plot3D_frame = tk.Frame(root)
import0_frame = tk.Frame(start_frame, width=100, height=50)
import0_frame.pack(pady=0, padx=20)
import1_frame = tk.Frame(start_frame,  width=100, height=50)
import1_frame.pack(pady=20, padx=20)
import2_frame = tk.Frame(start_frame,  width=100, height=50)
import2_frame.pack(pady=20, padx=20)
geoRef_frame = tk.Frame(root)


#  fonts
font_large = font.Font(family='Georgia',
                       size='24',
                       weight='bold')
font_small = font.Font(family='Georgia',
                       size='12')


#  start frame
# image
img_lidar = tk.PhotoImage(file='lidar.png')
img_lidar = img_lidar.zoom(5)
img_lidar = img_lidar.subsample(32)
lbl_lidar_start = tk.Label(import0_frame,
                           image=img_lidar)

# the heading for this frame.
lbl_heading_start = tk.Label(import0_frame,
                             text='Import your data',
                             font=font_large)
lbl_lidar_start.pack(pady=0)
lbl_heading_start.pack(pady=0)

# Buttons

e1 = tk.Entry(import1_frame)
e1.pack(side=tk.LEFT, pady=20)
btn_import_scanner = tk.Button(import1_frame,
                               text='Import scanner data',
                               bg='#000000',
                               fg='#ffffff',
                               relief='flat',
                               font=font_small,
                               command=import_scanner)
btn_import_scanner.pack(pady=20, side=tk.LEFT)

e2 = tk.Entry(import2_frame)
e2.pack(side=tk.LEFT, pady=20)


btn_import_GPS = tk.Button(import2_frame,
                           text='Import GPS data',
                           bg='#000000',
                           fg='#ffffff',
                           relief='flat',
                           font=font_small,
                           command=import_GPS)
btn_import_GPS.pack(pady=20, side=tk.LEFT)

btn_next = tk.Button(start_frame,
                     text='NEXT',
                     bg='#2980b9',
                     fg='#000000',
                     relief='flat',
                     font=font_small,
                     command=next)
btn_next.pack(pady=20)


# viewer frame

img_vis = tk.PhotoImage(file='vis.png')
img_vis = img_vis.zoom(30)
img_vis = img_vis.subsample(30)
lbl_vis_start = tk.Label(viewer_frame,
                         image=img_vis)

# the heading for this frame.
lbl_heading_start = tk.Label(viewer_frame,
                             text='Visualize your data',
                             font=font_large)
lbl_vis_start.pack(pady=0)
lbl_heading_start.pack(pady=20)


btn_visualization = tk.Button(viewer_frame,
                              text='3D Visualization',
                              bg='#000000',
                              fg='#ffffff',
                              relief='flat',
                              font=font_small,
                              command=visualize3D)
btn_visualization.pack(pady=20)

# swap back to the start frame.
btn_back = tk.Button(viewer_frame,
                     text='Back home',
                     bg='#2980b9',
                     fg='#000000',
                     relief='flat',
                     font=font_small,
                     command=change_to_start)
btn_back.pack(pady=20)


# 3D VIS frame

# Label de frame 3D vis
lbl_vis3D = tk.Label(plot3D_frame,
                     text='Visualization 3D',
                     font=font_large)
lbl_vis3D.pack(pady=20)
lbl_vis3D.pack(pady=20)


btn_back = tk.Button(plot3D_frame,
                     text='Back home',
                     bg='#2980b9',
                     fg='#000000',
                     relief='flat',
                     font=font_small,
                     command=back)
btn_back.pack(pady=20)

btn_georef = tk.Button(plot3D_frame,
                       text='Georefrencing',
                       bg='#2980b9',
                       fg='#000000',
                       relief='flat',
                       font=font_small,
                       command=georef)
btn_georef.pack(pady=20)


# georef frame

lbl_vis3D = tk.Label(geoRef_frame,
                     text='Visualization 3D',
                     font=font_large)
lbl_vis3D.pack(pady=20)
lbl_vis3D.pack(pady=20)

btn_back = tk.Button(geoRef_frame,
                     text='Back',
                     bg='#2980b9',
                     fg='#000000',
                     relief='flat',
                     font=font_small,
                     command=backgeo)
btn_back.pack(pady=20)


# the start frame needs to be shown when the program starts.

start_frame.pack(fill='both', expand=1)

root.mainloop()
