from Tkinter import *
import ttk

def remove_all():
    x = tv.get_children()
    if x != '()':
        for child in x:
            tv.delete(child)

root = Tk()

tv = ttk.Treeview(root)
tv['columns'] = ('Time','Date','Scores')
tv.heading('#0',text='Time')
tv.column('#0',anchor='center',width=60)
tv.heading('#1',text='Date')
tv.column('#1',anchor='center',width=60)
tv.heading('#2',text='Player')
tv.column('#2',anchor='center',width=60)
tv.heading('#3',text='Computer')
tv.column('#3',anchor='center',width=60)
ttk.Style().configure(tv,font=('',11),background="red",foreground="white", fieldbackground="dark red")
ysb = ttk.Scrollbar(root)
ysb.pack(side="right",fill="y")
tv.config(yscrollcommand=ysb.set)
ysb.config(command=tv.yview)
tv.pack(side="left")
for i in range(0,100):
    tv.insert('','end',text="%d"%i,values=('1','1','1'))
#erase
#remove_all()

root.mainloop()
