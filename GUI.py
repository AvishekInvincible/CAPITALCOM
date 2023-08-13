import tkinter as tk
# import customtkinter as tk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fast Order")
    def stock_label(self,Stock):
        self.label = tk.Label(self, text=str(Stock))
        self.label.pack()


app = MyApp()
app.mainloop()
