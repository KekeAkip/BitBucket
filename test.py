import tkinter as tk
root = tk.Tk()
sv = tk.StringVar()
tk.Entry(root, textvariable=sv).pack()
root.mainloop()
