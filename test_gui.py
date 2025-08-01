import tkinter as tk

root = tk.Tk()
root.title("Test")
root.geometry("300x100")
label = tk.Label(root, text="Tkinter works!")
label.pack(pady=20)
root.mainloop()
