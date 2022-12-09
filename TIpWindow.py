from tkinter import *

class ToolTip():
    
    def __init__(self, widget):
        self.widget = widget
        self.tip = None
        self.x = self.y = 0
        
    def showtip(self, text):
        #Display the tooltip window with text
        self.text = text
        if self.tip or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 40
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#faedcd", relief=SOLID, borderwidth=0.5,
                      foreground="#111111",
                      font=("tahoma", "15", "normal"))
        label.pack(ipadx=1)
        
    def hidetip(self):
        tip = self.tip;
        self.tip = None
        if tip:
            tip.destroy()
            
def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)