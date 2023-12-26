from tkinter import ttk, Tk, Label, Button, Radiobutton, Entry, StringVar, BooleanVar, IntVar, messagebox, Canvas
import json, webbrowser, random, pandas as pd, plotly.express as px
from PIL import Image, ImageTk

class SwiftQuill(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("SwiftQuill - Home")
        self.icon = ImageTk.PhotoImage(Image.open("./Assets/Logo.png").convert("RGBA"))
        self.logo = ImageTk.PhotoImage(Image.open("./Assets/SwiftQuill.png").convert("RGBA").resize((130, 75), Image.ADAPTIVE))
        self.iconphoto(False, self.icon)

        self.setting = Label(self, text="Settings", cursor='hand2', font=("Noto Sans", 15))
        self.score = Label(self, text="Score", cursor='hand2', font=("Noto Sans", 15))
        self.home = Label(self, text="Home", cursor='hand2', font=("Noto Sans", 15))
        self.brand = Label(self, image=self.logo, cursor='hand2')

        self.setting.grid(row=0, column=6, padx=(10, 40)) 
        self.score.grid(row=0, column=5, padx=10)
        self.home.grid(row=0, column=4, padx=10)
        self.brand.grid(row=0, column=0, padx=20, pady=10)

        self.open_tab = 'Start'
        self.protected_widgets = []
        self.lang_list = ['English', 'Chinese', 'Spanish', 'French', 'German', 'Japanese', 'Russian', 'Arabic', 'Hindi', 'Portuguese']

        self.protected_widgets.extend([self.setting, self.score, self.home, self.brand])
        self.grid_columnconfigure(1, weight=1)
        self.initialize_settings()
        self.home_tab()
        self.bindings()
      
    def initialize_settings(self):
        with open("./settings.json", "r") as f:
            self.settings = json.load(f)
            self.language = self.settings["Language"]
            self.tracking = self.settings["Tracking"]
            self.dark_mode = self.settings["DarkMode"]
            self.test_length = self.settings["TestLength"]
            self.literature = self.settings["Literature"]
            self.graph_mean = self.settings["GraphMean"]
            self.cp_test_length = self.test_length
            
    def save_settings(self):
        current_settings = {
            "Language": self.op_language.get(),
            "Tracking": self.op_tracking.get(),
            "DarkMode": self.op_dark_mode.get(),
            "Literature": self.op_literature.get(),
            "TestLength": self.op_test_length.get(),
            "GraphMean": self.op_graph_mean.get()
        }
        
        with open("./settings.json", "w") as f:
            json.dump(current_settings, f, indent=4)
            messagebox.showinfo("Success", "Settings saved successfully!")
            
        self.initialize_settings()

    def setting_tab(self, event=None):
        if self.open_tab != 'Settings':
            self.open_tab = 'Settings'
            self.title("SwiftQuill - Settings")
            self.clear()
            Label(self, text="Settings Options", font=("Noto Sans", 25)).grid(row=1, column=1, columnspan=3, pady=(0,30))

            self.op_language = StringVar(value=self.language)
            Label(self, text='Language', font=("Noto Sans", 15)).grid(row=2, column=1, padx=10, pady=10)
            ttk.Combobox(self, values=self.lang_list, width=15, textvariable=self.op_language).grid(row=2, column=2, columnspan=2, padx=10, pady=10)

            self.op_dark_mode = BooleanVar(value=self.dark_mode)
            Label(self, text='App Theme', font=("Noto Sans", 15)).grid(row=3, column=1, padx=10, pady=10)
            Radiobutton(self, text="Dark Mode", variable=self.op_dark_mode, value=True, cursor='hand2', font=("Noto Sans", 12)).grid(row=3, column=2, padx=10, pady=10)
            Radiobutton(self, text="Light Mode", variable=self.op_dark_mode, value=False, cursor='hand2', font=("Noto Sans", 12)).grid(row=3, column=3, padx=10, pady=10)

            self.op_tracking = BooleanVar(value=self.tracking)
            Label(self, text='Progress Tracking', font=("Noto Sans", 15)).grid(row=4, column=1, padx=10, pady=10)
            Radiobutton(self, text="Yes", variable=self.op_tracking, value=True, cursor='hand2', font=("Noto Sans", 12)).grid(row=4, column=2, padx=10, pady=10)
            Radiobutton(self, text="No", variable=self.op_tracking, value=False, cursor='hand2', font=("Noto Sans", 12)).grid(row=4, column=3, padx=10, pady=10)

            self.op_literature = BooleanVar(value=self.literature)
            Label(self, text='Text Type', font=("Noto Sans", 15)).grid(row=5, column=1, padx=10, pady=10)
            Radiobutton(self, text="Literature Writing", variable=self.op_literature, value=True, cursor='hand2', font=("Noto Sans", 12)).grid(row=5, column=2, padx=10, pady=10)
            Radiobutton(self, text="Research Paper Writing", variable=self.op_literature, value=False, cursor='hand2', font=("Noto Sans", 12)).grid(row=5, column=3, padx=10, pady=10)

            self.op_test_length = IntVar(value=self.test_length)
            Label(self, text='Test Length (Seconds)', font=("Noto Sans", 15)).grid(row=6, column=1, padx=10, pady=10)
            tle = Entry(self, validate="key", validatecommand=(self.register(lambda v: v.isdigit() or (not v and tle.get().isdigit())), '%P'), textvariable=self.op_test_length)
            tle.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

            self.op_graph_mean = IntVar(value=self.graph_mean)
            Label(self, text='Graph Mean (Simplicity)', font=("Noto Sans", 15)).grid(row=7, column=1, padx=10, pady=10)
            gme = Entry(self, validate="key", validatecommand=(self.register(lambda v: v.isdigit() or (not v and gme.get().isdigit())), '%P'), textvariable=self.op_graph_mean)
            gme.grid(row=7, column=2, columnspan=2, padx=10, pady=10)
            Button(self, text="Save", font=("Noto Sans", 15), command=self.save_settings).grid(row=8, column=1, columnspan=3, pady=50)

    def home_tab(self, event=None):
        if self.open_tab != 'Home':
            self.open_tab = 'Home'
            self.title("SwiftQuill - Home")
            self.clear(); self.pick_text()
            Label(self, text="Typing Speed Test", font=("Noto Sans", 25)).grid(row=1, column=1, pady=(0,10))

            self.timer = Label(self, text="Start a Test", font=("Noto Sans", 15))
            self.timer.grid(row=2, column=1, pady=10)

            self.canvas = Canvas(self, width=700, height=350, background="#c3c3c3", borderwidth=3, highlightcolor="#373737", relief="solid")
            self.printed_text = self.canvas.create_text(10, 10, anchor="nw", text=self.picked_text, font=("Noto Sans", 15), width=690)
            self.canvas.grid(row=3, column=1, pady=10)

            self.uie = Entry(self, font=("Noto Sans", 15), relief="flat")
            self.uie.grid(row=4, column=1, pady=20)

            self.button = Button(self, text="Start", font=("Noto Sans", 15), command=self.start_test)
            self.button.grid(row=5, column=1)

    def check_input(self, event):
        if self.uie.get() and event.keysym == 'BackSpace' and self.current_letter > 0:
            self.current_letter -= 1
            self.key_pressed += 1
            
        elif self.uie.get() and event.keysym not in ['Shift_L', 'Shift_R']:
            self.letter = self.uie.get()[-1]
            
            if self.letter == self.picked_text[self.current_letter]:
                self.canvas.itemconfig(self.printed_text, fill="green")
                self.uie.delete(0, 'end') if self.letter == ' ' else None
            else:
                self.canvas.itemconfig(self.printed_text, fill="red")
                self.uie.delete(0, 'end') if self.letter == ' ' else None
                self.fail += 1
        
            self.current_letter += 1
            self.key_pressed += 1
            if self.current_letter == len(self.picked_text):
                self.stop_test("Finished!")
                self.add_data()

    def start_test(self):
        self.current_letter = 0; self.fail = 0; self.key_pressed = 0
        self.uie.delete(0, "end")
        self.uie.bind('<KeyRelease>', self.check_input)
        self.button.config(text="Stop", command=self.stop_test)
        self.update_timer() 

    def update_timer(self):
        self.timer.config(text=self.test_length)
        self.test_length -= 1
        self.count = self.timer.after(1000, self.update_timer)
        if (self.test_length + 2) == 0:
            self.stop_test("Time's up!")
            self.add_data()

    def stop_test(self, message='Stopped!'):
        self.timer.config(text=message)
        self.uie.delete(0, "end")
        self.uie.unbind('<KeyRelease>')
        self.test_length = self.cp_test_length
        self.canvas.itemconfig(self.printed_text, text=self.picked_text, fill='black')
        self.button.config(text="Start", command=self.start_test)
        self.timer.after_cancel(self.count)
        self.pick_text()
        
    def pick_text(self):
        self.type = "Literature Writing.json" if self.literature else "Research Paper Writing.json"
        with open(f"./Assets/{self.type}", "r") as f:
            self.texts = json.load(f)
            self.picked_text = self.texts[self.language][str(random.randint(1, 5))]
            
    def add_data(self):
        if self.key_pressed > 15:
            self.accuracy = round(100 - (self.fail / self.key_pressed) * 100, 2)
            self.WPM = round(self.key_pressed / 5, 2)
            self.date = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            
            new_row = pd.DataFrame([{'Date': self.date, 'WPM': self.WPM, 'Accuracy': self.accuracy}])
            new_row.to_csv('Progress.csv', index=False, mode='a', header=False)

    def score_tab(self, event=None):
        if self.open_tab != 'Score':
            self.open_tab = 'Score'
            self.title("SwiftQuill - Score")
            self.clear()
            Label(self, text="Progress Since", font=("Noto Sans", 25)).grid(row=1, column=1, columnspan=3, pady=(0,30))

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy() if widget not in self.protected_widgets else None    

    def bindings(self):
        self.setting.bind("<Enter>", lambda event: self.underline_on_hover(event, self.setting))
        self.score.bind("<Enter>", lambda event: self.underline_on_hover(event, self.score))
        self.home.bind("<Enter>", lambda event: self.underline_on_hover(event, self.home))
        
        self.setting.bind("<Leave>", lambda event: self.remove_underline(event, self.setting))
        self.score.bind("<Leave>", lambda event: self.remove_underline(event, self.score))
        self.home.bind("<Leave>", lambda event: self.remove_underline(event, self.home))
        
        self.brand.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/RedeemedSpoon/SwiftQuill"))
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
    app.mainloop()
