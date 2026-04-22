# import module
import tkinter as Tkinter
import random

# RGB Color Selecting Function
def rgb(x,y,z):
 return "#%02x%02x%02x" % (x,y,z)

# Random Color Chooser
def random_color():
 x = random.randint(1,255)
 y = random.randint(1,255)
 z = random.randint(1,255)
 return rgb(x,y,z)


# Some Configurations
WIDTH=25
HEIGHT=25
GRID_W = 20
GRID_H = 20

# Main Class For Canvas Widget
class Wall(Tkinter.Canvas):
 def __init__(self, *args, **kwargs):
  Tkinter.Canvas.__init__(self, *args, **kwargs)
  self.squares = []
  self.create_squares()

  # binding mouse motion
  self.bind("<Motion>", self.change)

 # Create Squares
 def create_squares(self):
  for i in range(GRID_W):
   for j in range(GRID_H):
    x1 = i*WIDTH
    y1 = j*HEIGHT
    x2 = x1+WIDTH
    y2 = y1+HEIGHT
    s=self.create_rectangle(x1,y1,x2,y2, fill=random_color(), tag="{}{}".format(i,j))
    self.squares.append(s)
  return

 # Change Colors 
 def change(self, event=None):
  for i in self.squares:
   self.itemconfig(i, fill=random_color())
  return


# main Function
def main():
 root=Tkinter.Tk(className=" Color Wall")
 k=Wall(root, width=300, height=200)
 k.pack(expand=True, fill="both")
 root.geometry('500x500')
 root.mainloop()
 return

# Main Trigger
if __name__=="__main__":
 main()