import math as m
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk             # This has all the code for GUIs.
import tkinter.font as font      # This lets us use different fonts.
from tkinter import ttk
from tkinter.filedialog import askopenfile, askopenfilenames
import matplotlib
matplotlib.use("TkAgg")

scanner_files = tuple()
gps_file = str()
preprocessed = []


def center_window_on_screen():
    x_cord = int((screen_width/2) - (width/2))
    y_cord = int((screen_height/2) - (height/2))
    root.geometry("{}x{}+{}+{}".format(width, height, x_cord, y_cord))


def import_scanner():
    """ files = askopenfilenames(filetypes=(('Text files', '*.txt'),
                                        ('All files', '*.*')),
                             title='Select Input File'
                             )
    fileList = root.tk.splitlist(files)
    print('Files = ', fileList) """
    global scanner_files
    scanner_files = open_multiple_files()
    e1.insert(0, ", ".join(scanner_files))


def import_GPS():
    global gps_file
    gps_file = open_file()
    e2.insert(0, gps_file.name)


def open_multiple_files():
    return askopenfilenames(parent=root)


def open_file():
    return askopenfile(mode='r')


def plot(data):
    x = data[:, 1]
    y = data[:, 2]
    z = data[:, 3]

    fig = Figure(figsize=(10, 10))
    a = fig.add_subplot(111, projection="3d")
    a.scatter(x, y, z, c=z, cmap="rainbow")

    a.set_title("3D plot")
    a.set_xlabel('x-axis')
    a.set_ylabel('y-axis')
    a.set_zlabel('z-axis')
    a.view_init(None, 120)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()


def load_data():
    data = list()

    for filename in scanner_files:
        data.append(np.loadtxt(filename))

    return data


def load_gps():
    return np.loadtxt(gps_file.name, skiprows=1)


def preprocess():
    global preprocessed
    data = load_data()
    for i in range(len(data)):
        data[i][:, 0] = data[i][:, 0] + (i * 538)

    merged = data[0]
    for file_input in data[1:]:
        merged = np.concatenate((merged, file_input))

    merged = merged[np.lexsort((merged[:, 0], merged[:, 1]))]

    # We keep only 4 columns: (profile, X, Y, Z)

    merged = merged[:, 1:5]

    preprocessed = merged
    return merged


def georeference():
    preprocess()
    translation_vector = np.array([0.14, 0.249, -0.076])
    rotation_matrix = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    result = np.empty((preprocessed.shape[0], 4))
    for i in range(preprocessed.shape[0]):
        result[i] = np.array(
            [preprocessed[i][0], *(rotation_matrix.dot(preprocessed[i][1:]) + translation_vector)])

    gps_result = np.empty((result.shape[0], 4))

    counter = 0

    for i in range(500):
        # Get data from GPS

        gps = load_gps()

        angles = np.array(gps[i, 7:10])
        gps_coordinates = np.array(gps[i, 1:4])

        # Calculate rotation matrix
        rotation_matrix = gps_rotation_matrix(
            heading=angles[2], pitch=angles[1], roll=angles[0])

        # Select by profile number
        results_by_profile = result[result[:, 0] == i, :][:, 1:]

        # Apply transformation to points belonging to that profiles
        for j in range(results_by_profile.shape[0]):
            gps_result[counter] = np.array(
                [0, *(results_by_profile[j].dot(rotation_matrix) + gps_coordinates)])
            counter += 1

    return gps_result


def gps_rotation_matrix(heading, pitch, roll):
    """
    Utility function to calculate rotation matrix
    """
    Rheading = np.array([
        [m.cos(heading), -m.sin(heading), 0],
        [m.sin(heading), m.cos(heading), 0],
        [0, 0, 1]
    ])

    Rpitch = np.array([
        [m.cos(pitch), 0, m.sin(pitch)],
        [0, 1, 0],
        [-m.sin(pitch), 0, m.cos(pitch)],
    ])

    Rroll = np.array([
        [1, 0, 0],
        [0, m.cos(roll), -m.sin(roll)],
        [0, m.sin(roll), m.cos(roll)],
    ])

    return Rheading * Rpitch * Rroll


def next():
    start_frame.forget()
    viewer_frame.pack(fill='both', expand=1)


def change_to_start():
    start_frame.pack(fill='both', expand=1)
    viewer_frame.forget()


def visualize3D():
    viewer_frame.forget()
    start_frame.forget()
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


# btn_back = tk.Button(plot3D_frame,
#                    text='Back home',
#                   bg='#2980b9',
#                  fg='#000000',
#                 relief='flat',
#                font=font_small,
#               command=back)
# btn_back.pack(pady=20)

btn_georef = tk.Button(plot3D_frame,
                       text='Georefrencing',
                       bg='#2980b9',
                       fg='#000000',
                       relief='flat',
                       font=font_small,
                       command=lambda: plot(georeference()))
btn_georef.pack(pady=20)


# the start frame needs to be shown when the program starts.

start_frame.pack(fill='both', expand=1)

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Import scanner data ", command=import_scanner)
filemenu.add_command(label="Import Gps data", command=import_GPS)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)


menubar.add_cascade(label="File", menu=filemenu)
editmenu = tk.Menu(menubar, tearoff=0)

editmenu.add_command(label="data visualization",
                     command=visualize3D)
menubar.add_cascade(label="Visualization", menu=editmenu)


root.config(menu=menubar)

root.mainloop()
