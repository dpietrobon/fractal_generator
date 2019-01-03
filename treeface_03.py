# Tree Fractal Program with GUI
# Global variable FTW D:

from tkinter import *
import numpy as np
import math


def FractalTransform():
    global v
    global list_points
    v.set("Transforming ... ")
    root.update()
    num_points = int(len(list_points)/2)
    num_lines = int(num_points/2)
    h = canvas.winfo_height()
    w = canvas.winfo_width()
    complex_list = []
    center_points = []
    line_size = []
    angles = []

    # Transform list_points to a complex / Cartesian form --- scaled to the unit circle
    for n in range(0,num_points):
        complex_list.append(list_points[2*n]*(4/w)+1j*list_points[2*n+1]*(4/h))
    
    # Fractalize those points
    complex_list = np.array(complex_list)
    L = np.zeros(int(0.5*num_points**2),dtype=complex)
    
    for n in range(0,num_lines):
        cl_a = complex_list[2*n]
        cl_b = complex_list[2*n+1]
        angles.append(np.angle(cl_b-cl_a)-np.pi/2)
        print(angles)
        line_size.append(np.sqrt((cl_a.real-cl_b.real)**2+(cl_a.imag-cl_b.imag)**2))
        center_points.append(0.5*(cl_a + cl_b))
        L[(n*num_points):(n+1)*num_points] = np.exp(1j*angles[n])*line_size[n]*complex_list + center_points[n]

    DrawFractal(L)
    
    v.set("Transform complete.")

def DrawFractal(L):
    print(L)
    h = canvas.winfo_height()
    w = canvas.winfo_width()
    for n in range(0,int(len(L)/2)):
        canvas.create_line((L[2*n].real)*(w/4)+(w/2), -(L[2*n].imag)*(h/4)+(h/2), (w/4)*(L[2*n+1].real)+(w/2), (h/4)*-(L[2*n+1].imag)+(h/2))
    

def DoNothingOnClick(event):
    # We can't do nothing but we CAN set a equal to zero.
    a = 0

def exitWindow():
    root.destroy()

def clearWindow():
    canvas.delete(ALL)
    global list_points
    list_points = []
    if Axis_Button.config('relief')[-1] == "sunken":
        h = canvas.winfo_height()
        w = canvas.winfo_width()
        global x_axis
        global y_axis
        global oval
        x_axis = canvas.create_line(0, 0.5*h, w, h/2, dash=(4,2))
        y_axis = canvas.create_line(w/2, 0, w/2, h, dash=(4,2))
        coord = w/4, h/4, 3*w/4, 3*h/4
        oval = canvas.create_oval(coord,dash=(1,1))
        
def toggleLine():
    if Line_Button.config('relief')[-1] == 'sunken':
        Line_Button.config(relief="raised")
        canvas.bind('<Button-1>', DoNothingOnClick)
    else:
        Line_Button.config(relief="sunken")
        canvas.bind('<Button-1>', DrawLine)

def DrawAxis():
    if Axis_Button.config('relief')[-1] == 'sunken':
        Axis_Button.config(relief="raised")
        global x_axis
        global y_axis
        global oval
        canvas.after(0, canvas.delete, x_axis)
        canvas.after(0, canvas.delete, y_axis)
        canvas.after(0, canvas.delete, oval)
    else:
        Axis_Button.config(relief="sunken")
        h = canvas.winfo_height()
        w = canvas.winfo_width()
        x_axis = canvas.create_line(0, 0.5*h, w, h/2, dash=(4,2))
        y_axis = canvas.create_line(w/2, 0, w/2, h, dash=(4,2))
        coord = w/4, h/4, 3*w/4, 3*h/4
        oval = canvas.create_oval(coord,dash=(1,1))
        
def DrawLine(event):
    global num_points
    num_points = (num_points+1) % 2
    if num_points % 2 == 1:
        global x_1
        global y_1
        h = canvas.winfo_height()
        w = canvas.winfo_width()
        xx = event.x - w/2
        yy = -(event.y - h/2)
        x_1 = event.x
        y_1 = event.y
        list_points.append(xx)
        list_points.append(yy)
        global line_id
        line_id = canvas.create_line(x_1,y_1,x_1,y_1)
    if num_points % 2 == 0:
        h = canvas.winfo_height()
        w = canvas.winfo_width()
        xx = event.x - w/2
        yy = -(event.y - h/2)
        x_2 = event.x
        y_2 = event.y
        list_points.append(xx)
        list_points.append(yy)
        canvas.create_line(x_1, y_1, x_2, y_2)
        
def motion(event):
    global v
    h = canvas.winfo_height()
    w = canvas.winfo_width()
    xx = event.x - w/2
    yy = -(event.y - h/2)

    s = "Coordinates (x,y) = (%d,%d)" % (xx,yy)
    v.set(s)
    if num_points % 2 == 1:
        global line_id
        canvas.after(0, canvas.delete, line_id)
        line_id = canvas.create_line(x_1, y_1, event.x, event.y)
    

# Initialize Variables

num_points = 0
list_points = []

# Initialize Root Window

root = Tk()
root.geometry("500x500")
root.title("Line Fractal Transformer")
root.config(padx=5,pady=5)

# Initialize Canvas

canvas = Canvas(width=300,height=300,bg="white",bd=3,relief="groove")
canvas.bind('<Motion>',motion)
canvas.bind('<Button-1>', DrawLine)
canvas.pack(fill="both",padx=2,pady=2,expand=True)


## Buttons with Images

line_image = PhotoImage(file="line_0.png")
axis_image = PhotoImage(file="axis_button.png")

Line_Button = Button(root, command=toggleLine,image=line_image,relief="sunken")
Line_Button.pack(side=LEFT)
Axis_Button = Button(root, command=DrawAxis, image=axis_image,relief="raised")
Axis_Button.pack(side=LEFT)

### Status Bar

v = StringVar()
v.set("Coordinates (x,y) = ... ")
status = Label(root,textvariable=v,bg="white",height=2)
status.pack(fill=X,side=LEFT,expand=True)


## Normie Buttons

Exit_Button = Button(root, text="Quit", command=exitWindow)
Exit_Button.pack(side=RIGHT)
Clear_Button = Button(root, text="Clear", command=clearWindow)
Clear_Button.pack(side=RIGHT)
Button3 = Button(root, text="Transform", command=FractalTransform)
Button3.pack(side=RIGHT)

##print(Axis_Button.config('relief')[-1])
Axis_Button.invoke()
canvas.update()
##print(Axis_Button.config('relief')[-1])

h = canvas.winfo_height()
w = canvas.winfo_width()
x_axis = canvas.create_line(0, 0.5*h, w, h/2, dash=(4,2))
y_axis = canvas.create_line(w/2, 0, w/2, h, dash=(4,2))
coord = w/4, h/4, 3*w/4, 3*h/4
oval = canvas.create_oval(coord,dash=(1,1))

# Labels

#label = Label(root,text="Draw Here",bg="yellow")
#label.pack()

### Magic
#root.winfo_pointerxy()

#root.mainloop()
