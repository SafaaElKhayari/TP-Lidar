from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.messagebox import *
import numpy as np
import pandas as pd
import codecs
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Create a window
window = Tk()

# Window geometry
window.geometry("2500x1000")

path = StringVar()


def open_file():
    file = askopenfile(mode='r', filetypes=[('Python Files', '*.asc')])
    if file is not None:
        content = file.read()
        # print(type(content))
    with codecs.open(file.name, encoding='utf-8-sig') as f:
        table = np.loadtxt(f)
        # print(table)
    path.set("File path: "+file.name)
    plot(table)


def plot(table):
    df = pd.DataFrame(table, columns=['X', 'Y', 'Z'])
    x = df.X
    y = df.Y
    z = df.Z
    # df.plot.scatter(x='X',y='Y',c='Z');

    # 2D PLOT
    fig, a = plt.subplots(figsize=(50, 50))
    a = fig.add_subplot(111)
    a.scatter(x, y, c=z)
    a.set_title("Nuage de points en 2D", fontsize=16)

    canvas = FigureCanvasTkAgg(fig, master=window)

    canvas.get_tk_widget().pack()
    canvas.draw()

    # 3D PLOT
    # fig2 = plt.figure(figsize=(300,200))
    # ax3d = fig2.add_subplot(projection='3d')

    # ax3d.scatter(x, y, z)
    # ax3d.set_title("Nuage de points en 3D", fontsize=16)

    # canvas2 = FigureCanvasTkAgg(fig2, master=window)
    # canvas2.get_tk_widget().pack()
    # canvas2.draw()


bouton = Button(window, text="Importer", command=lambda: open_file(), pady=10)
bouton.pack()

label = Label(window, textvariable=path, pady=20)
label.pack()


window.mainloop()
