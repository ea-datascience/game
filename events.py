import tkinter
from tkinter import *

ws = Tk(  )
ws.geometry("200x200")
display='Press Any Button, or Press  Key'
Lab= Label(ws, text=display, width=len(display))
Lab.pack(pady=40)

def key(eve):
    if eve.char==eve.keysym:
        message ='Normal Key %r' % eve.char
    elif len(eve.char)==1:
        message ='Punctuation Key %r (%r)' % (eve.keysym, eve.char)
    else:
        message ='Special Key %r' % eve.keysym
    Lab.config(text=message)
Lab.bind_all('<Key>', key)

def do_mouse(eventname):
    def mouse_binding(event):
        message = 'Mouse event %s' % eventname
        Lab.config(text=message)
    Lab.bind_all('<%s>'%eventname, mouse_binding)

for i in range(1,4):
    do_mouse('Button-%s'%i)
    do_mouse('ButtonRelease-%s'%i)
    do_mouse('Double-Button-%s'%i)


ws.mainloop(  )