


from Tkinter import Tk, Label, Button, Canvas, Radiobutton, Toplevel, OptionMenu, StringVar, Message, Entry, IntVar, Checkbutton
from time import sleep
import numpy as np
import socket
import sys
from threading import Thread


class MapUI:
	
    def __init__(self, master):

        def center(win):
            win.update_idletasks()
            width = win.winfo_width()
            height = win.winfo_height()
            x = (win.winfo_screenwidth() // 4) - (width // 2) + 40
            y = (win.winfo_screenheight() // 4) - (height // 2) + 40
            win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        def callback(event):
            event.widget.focus_set()
            print "clicked at", event.x, event.y

            if self.add_tasks_flg.get() == 1:
                # Select number of robots
                # Define elements of pop up window
                self.top = Toplevel()

                self.num_robots = StringVar(self.top)
                self.num_robots.set("1") # default value
                w = OptionMenu(self.top, self.num_robots, '1','2','3','4').grid(row=0,column=1)
                text1 = Message(self.top, text="Number of robots:", width = 150).grid(row=0,column=0)

                self.e = Entry(self.top, width=10)
                self.e.grid(row=1,column=1)
                text2 = Message(self.top, text="Task duration:", width = 150).grid(row=1,column=0)
                text3 = Message(self.top, text="(s)", width=60).grid(row=1,column=2)

                newline = Message(self.top, text=" ").grid(row=2)

                button = Button(self.top, text='Enter', command=lambda: self.enter_task(event)).grid(row=3,column=1)
                button_cancel = Button(self.top, text='Cancel', command=self.cancel_task).grid(row=3,column=2)

                center(self.top)


        master.title("Map Interface")
        master.minsize(width=900, height=650)
        master.maxsize(width=900, height=650)
        master.config(bg=BKG_COLOUR)
        self.master = master

        # Canvas for overlaying map
        self.map_canvas = Canvas(master, width=CANVAS_W, height=CANVAS_H, bg='snow', highlightthickness=0)
        self.map_canvas.pack(side='right',padx=50)
        self.map_canvas.bind("<Button-1>", callback)
        global CANVAS_PTR
        CANVAS_PTR = self.map_canvas
        self.master.update()
        w = self.map_canvas.winfo_width()
        h = self.map_canvas.winfo_height()
        # Overlay a grid
        for i in range(0,w,SQ_SIZE):
        	if i != 0:
				self.map_canvas.create_line(i,0,i,h)
        for i in range(0,h,SQ_SIZE):
        	if i != 0:
        		self.map_canvas.create_line(0,i,w,i)

        # Define UI buttons
        self.add_tasks_flg = IntVar()
        self.add_tasks_b = Checkbutton(master, text="Add Tasks", variable=self.add_tasks_flg, highlightbackground=BKG_COLOUR, background=BKG_COLOUR)
        self.add_tasks_b.place(x=77,y=140)

        self.clear_wp_b = Button(master, text='Clear Tasks', command=self.clear_wp, highlightbackground=BKG_COLOUR)
        self.clear_wp_b.config(width=10)
        self.clear_wp_b.place(x=65, y=170)
        
        self.gen_wp_file_b = Button(master, text='Generate Waypoints File', command=self.gen_wp_file, highlightbackground=BKG_COLOUR)
        self.gen_wp_file_b.config(width=20)
        self.gen_wp_file_b.place(x=20, y=250)

        self.run_b = Button(master, text='Run', command=self.run, highlightbackground=BKG_COLOUR)
        self.run_b.config(width=10, height=10)
        self.run_b.place(x=65, y=350)

        # Set up coordinate system conversion and display corners of room:
        file_obj  = open('antenna_locations.txt', 'r')
        anchors = []
        for line in file_obj:
        	cur_anchors = map(float, line.split())
        	anchors.append(cur_anchors)
        file_obj.close()
        anchors = (np.array(anchors)).T

        # Find largest (abs) x and y values to use a reference for conversion ratio
        x_vals = anchors[0]
        largest_x_val = x_vals[np.argmax(abs(x_vals))]
        y_vals = anchors[1]
        largest_y_val = y_vals[np.argmax(abs(y_vals))]
        self.m_per_pixel_x = float(largest_x_val/(CANVAS_W/2))
        self.m_per_pixel_y = float(largest_y_val/(CANVAS_H/2))

        # Place antenna (anchors) on UI
        anchors = anchors.T
        for cur_anchor in anchors:
        	x_pixel_loc = cur_anchor[0] / self.m_per_pixel_x + CANVAS_W/2
        	y_pixel_loc = cur_anchor[1] / self.m_per_pixel_x + CANVAS_H/2
        	print(x_pixel_loc, y_pixel_loc)

        self.master.update()

    global SQ_SIZE 
    SQ_SIZE = 20
    global BKG_COLOUR
    BKG_COLOUR = 'light grey'
    global CANVAS_W
    CANVAS_W = 600
    global CANVAS_H
    CANVAS_H = 600
    global TASK_LIST
    TASK_LIST = None

    
    ui_wp_list = None
    #task_list = None
    add_wp_flag = False
    task_id = 0
    add_tasks_flg = None
    m_per_pixel_x = None
    m_per_pixel_y = None
    

    def add_tasks(self):
        print "adding tasks"
        # function imp here
        self.add_wp_flag = True
        self.map_canvas.config(cursor='pencil')


    def clear_wp(self):
        print "clear wp"
        global TASK_LIST
        TASK_LIST = None
        for element_id in self.ui_wp_list:
            self.map_canvas.delete(element_id[0])
        self.ui_wp_list = None

    def gen_wp_file(self):
        print "generate wp file"
        # function imp here

    def run(self):
        print "run"
        # function imp here

    def enter_task(self, event):
        # Determine square (top left corner coords):
        w_start = event.x - event.x%SQ_SIZE
        h_start = event.y - event.y%SQ_SIZE

        #Translate pixel location to physical location
        x_pixel = event.x
        y_pixel = event.y
        # Find out how many pixels from center:
        x_pixel = x_pixel - CANVAS_W/2
        x_physical = x_pixel*self.m_per_pixel_x

        #vertical case, note this is flipped
        y_pixel = y_pixel - CANVAS_W/2
        y_pixel = -1*y_pixel
        y_physical = y_pixel*self.m_per_pixel_y

        # Indicate waypoint in UI
        element_id = self.map_canvas.create_rectangle(w_start,h_start,w_start+SQ_SIZE,h_start+SQ_SIZE,fill='green')
        if self.ui_wp_list == None:
            self.ui_wp_list = [[element_id]]
        else:
            self.ui_wp_list.append([element_id])

        # Add to task list
        global TASK_LIST
        if TASK_LIST == None:
            TASK_LIST = [[self.task_id, int(self.num_robots.get()), float(self.e.get()), x_physical, y_physical]]
        else:
            TASK_LIST.append([self.task_id, int(self.num_robots.get()), float(self.e.get()), x_physical, y_physical])

        self.map_canvas.config(cursor='arrow')
        self.add_wp_flag = False

        print(TASK_LIST)
        
        self.task_id = self.task_id + 1
        self.top.destroy()

    def cancel_task(self):
        self.top.destroy()


global prev_x
prev_x = 0
global prev_y
prev_y = 0
global PREV_ROBOT_LOCATION
PREV_ROBOT_LOCATION = None

def socket_loop():
	HOST = 'localhost'   # Symbolic name, meaning all available interfaces
	PORT = 8888 # Arbitrary non-privileged port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT)) 
	s.listen(1)
	conn, addr = s.accept()
	position = conn.recv(20)
	position = map(float, position.split())
	
	
	if PREV_ROBOT_LOCATION != None:
		CANVAS_PTR.delete(PREV_ROBOT_LOCATION)

	global PREV_ROBOT_LOCATION
	PREV_ROBOT_LOCATION = CANVAS_PTR.create_rectangle(position[0], position[1], position[0]+10, position[1]+10, fill='black')
	
	'''

	# Redraw the grid
	for i in range(0,CANVAS_W,SQ_SIZE):
		if i != 0:
			CANVAS_PTR.create_line(i,0,i,CANVAS_H)
	for i in range(0,CANVAS_H,SQ_SIZE):
		if i != 0:
			CANVAS_PTR.create_line(0,i,CANVAS_W,i)
	# Redraw green squares
	global TASK_LIST
	if TASK_LIST != None:
		for tasks in TASK_LIST:
			x_pos = tasks[3]
			y_pos = tasks[4]
			#CANVAS_PTR.create_rectangle(x_pos,y_pos,x_pos+SQ_SIZE-1,y_pos+SQ_SIZE-1,fill='green',outline='white')

	'''
	global prev_x
	prev_x = position[0]
	global prev_y
	prev_y = position[1]
	#print(position)
	s.close()
	root.after(500, socket_loop)


root = Tk()
my_gui = MapUI(root)
socket_loop()
root.mainloop()
'''
root.mainloop()
'''
'''
root = Tk()
root.title("test")
root.geometry("600x600")
root.configure(background="grey")

def callback(event):
    event.widget.focus_set()
    print "clicked at", event.x, event.y


def create_grid(event=None):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, 10):
        c.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 10):
        c.create_line([(0, i), (w, i)], tag='grid_line')


c = Canvas(root, height=1000, width=1000, bg='white')
c = Canvas(root, height=1000, width=1000, bg='white')
c.pack(fill=BOTH, expand=True)

c.bind('<Configure>', create_grid)
c.bind("<Button-1>", callback)
'''

'''image_pil = Image.open("grid.png")
w, h = image_pil.size
resize_factor = w/500
resize_factor = float(w/500)
#image_pil = image_pil.resize((w/resize_factor, h/resize_factor))

photo = ImageTk.PhotoImage(image_pil)
label = Label(root, image=photo)
label.bind("<Button-1>", callback)
label.pack()
'''






