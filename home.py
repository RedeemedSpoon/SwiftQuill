import tkinter as tk
from PIL import Image, ImageTk

class SwiftQuill(tk.Tk):
    def __init__(self):
      super().__init__()
      self.geometry("1280x720")
      self.title("SwiftQuill - Home")
      self.icon = ImageTk.PhotoImage(Image.open("./Assets/Logo.png").convert("RGBA"))
      self.logo = ImageTk.PhotoImage(Image.open("./Assets/SwiftQuill.png").convert("RGBA").resize((130, 75), Image.ADAPTIVE))
      self.iconphoto(False, self.icon)

      self.setting = tk.Label(self, text="Settings", cursor='hand2', font=("Noto Sans", 15))
      self.score = tk.Label(self, text="Score", cursor='hand2', font=("Noto Sans", 15))
      self.home = tk.Label(self, text="Home", cursor='hand2', font=("Noto Sans", 15))
      self.brand = tk.Label(self, image=self.logo, cursor='hand2')
      
      self.setting.grid(row=0, column=4, padx=(10, 40)) 
      self.score.grid(row=0, column=3, padx=10)
      self.home.grid(row=0, column=2, padx=10)
      self.brand.grid(row=0, column=0, padx=30, pady=10)

      self.t_hello = tk.Label(self)
      self.c_hello = tk.Label(self)
      self.hello = tk.Label(self)
      
      self.grid_columnconfigure(1, weight=1)
      self.bindings()
        
    def home_tab(self, free_pass=False, event=None):
        if not self.hello.winfo_exists() or free_pass:
            self.hello = tk.Label(self, text="Hello World!", font=("Noto Sans", 15))
            self.hello.grid(row=1, column=1, padx=10, pady=10)
            self.c_hello.destroy()
            self.t_hello.destroy()

    def setting_tab(self, event=None):
        if not self.c_hello.winfo_exists():
            self.c_hello = tk.Label(self, text="Hello Settings!", font=("Noto Sans", 15))
            self.c_hello.grid(row=1, column=1, padx=10, pady=10)
            self.hello.destroy()
            self.t_hello.destroy()

    def score_tab(self, event=None):
        if not self.t_hello.winfo_exists():
            self.t_hello = tk.Label(self, text="Hello Score!", font=("Noto Sans", 15))
            self.t_hello.grid(row=1, column=1, padx=10, pady=10)
            self.hello.destroy()
            self.c_hello.destroy()

    def bindings(self):
        self.setting.bind("<Enter>", lambda event: self.underline_on_hover(event, self.setting))
        self.score.bind("<Enter>", lambda event: self.underline_on_hover(event, self.score))
        self.home.bind("<Enter>", lambda event: self.underline_on_hover(event, self.home))
        
        self.setting.bind("<Leave>", lambda event: self.remove_underline(event, self.setting))
        self.score.bind("<Leave>", lambda event: self.remove_underline(event, self.score))
        self.home.bind("<Leave>", lambda event: self.remove_underline(event, self.home))
        
        self.brand.bind("<Button-1>", self.home_tab)
        self.home.bind("<Button-1>", self.home_tab)
        self.score.bind("<Button-1>", self.score_tab)
        self.setting.bind("<Button-1>", self.setting_tab)

    @staticmethod
    def underline_on_hover(event, label):
        label.config(font=("Noto Sans", 15, "underline"))

    @staticmethod
    def remove_underline(event, label):
        label.config(font=("Noto Sans", 15))

if __name__ == "__main__":
    app = SwiftQuill()
    app.home_tab(free_pass=True)
    app.mainloop()
