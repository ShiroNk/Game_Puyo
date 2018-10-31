from tkinter import *

root = Tk()
root.option_add('*font', ('FixedSys', 14))

buffer = StringVar()
buffer.set('')


# キーの表示
def print_key(event):
    key = event.keysym
    buffer.set('push key is %s' % key)

# ラベルの設定
Label(root, text = '*** push any key ***').pack()
a = Label(root, textvariable = buffer)
a.pack()
a.bind('<Any-KeyPress>', print_key)
a.focus_set()

root.mainloop()