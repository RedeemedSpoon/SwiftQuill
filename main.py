import json, webbrowser, random, pandas as pd, plotly.graph_objects as go
from PIL import Image, ImageTk
from tkinter import (
    ttk, Tk, Label,
    Button, Radiobutton,
    Entry, StringVar,
    BooleanVar, IntVar,
    messagebox, Canvas,
)


class SwiftQuill(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("SwiftQuill - Home")
        self.icon = ImageTk.PhotoImage(Image.open("./Assets/Logo.png").convert("RGBA"))
        self.logo = ImageTk.PhotoImage(
            Image.open("./Assets/Mono_SwiftQuill.png")
            .convert("RGBA")
            .resize((162, 93), Image.ADAPTIVE)
        )
        self.iconphoto(False, self.icon)

        self.setting = Label(
            self, text="Settings", cursor="hand2", font=("Noto Sans", 15)
        )
        self.score = Label(self, text="Score", cursor="hand2", font=("Noto Sans", 15))
        self.home = Label(self, text="Home", cursor="hand2", font=("Noto Sans", 15))
        self.brand = Label(self, image=self.logo, cursor="hand2")

        self.setting.grid(row=0, column=8, padx=(10, 20))
        self.score.grid(row=0, column=7, padx=10)
        self.home.grid(row=0, column=6, padx=10)
        self.brand.grid(row=0, column=0, padx=30, pady=(10, 0))

        self.placeholder_left = Label(self, text=None)
        self.placeholder_right = Label(self, text=None)
        self.placeholder_left.grid(row=0, column=1)
        self.placeholder_right.grid(row=0, column=5)

        self.open_tab = "Start"
        self.lang_list = ["English", "French", "Spanish", "Portuguese", "Russian"]

        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.initialize_settings()
        self.analyse_data()
        self.home_tab()
        self.bindings()

    def home_tab(self, event=None):
        if self.open_tab != "Home":
            self.open_tab = "Home"
            self.title("SwiftQuill - Home")
            self.clear()
            self.pick_text(), self.print_text()
            Label(self, text="Typing Speed Test", font=("Noto Sans", 25)).grid(
                row=1, column=2, pady=(0, 10)
            )

            self.timer = Label(self, text="Start a Test", font=("Noto Sans", 15))
            self.timer.grid(row=2, column=2, pady=10)

            self.uie = Entry(self, font=("Noto Sans", 15), relief="flat")
            self.uie.grid(row=4, column=2, pady=20)

            self.button = Button(
                self, text="Start", font=("Noto Sans", 15), command=self.start_test
            )
            self.button.grid(row=5, column=2)

    def score_tab(self, event=None):
        if self.open_tab != "Score":
            self.open_tab = "Score"
            self.title("SwiftQuill - Score")
            self.clear()
            df = pd.read_csv("Progress.csv")
            if df.shape[0] < 2:
                Label(self, text="No Scores Yet!", font=("Noto Sans", 25)).grid(
                    row=1, column=2, pady=(0, 20)
                )
                Label(
                    self, text="You must start at least 3 tests", font=("Noto Sans", 15)
                ).grid(row=2, column=2)
            else:
                Label(
                    self,
                    text=f"Progress Since {df['Date'][1].split(' ')[0]}",
                    font=("Noto Sans", 25),
                ).grid(row=1, column=2, columnspan=2, pady=(0, 30))
                self.graph = ImageTk.PhotoImage(Image.open("./Assets/graph.png"))
                Label(self, image=self.graph).grid(
                    row=2, column=2, columnspan=2, pady=(0, 15)
                )
                Label(
                    text=f"Average WPM: { round(df['WPM'].mean(), 2) }",
                    font=("Noto Sans", 15),
                ).grid(row=3, column=2)
                Label(
                    text="Average Accuracy: "
                    + str(round(df["Accuracy"].mean(), 2))
                    + "%",
                    font=("Noto Sans", 15),
                ).grid(row=4, column=2)
                Label(
                    text=f"Latest WPM: {str(df['WPM'].tail(1).values[0])}",
                    font=("Noto Sans", 15),
                ).grid(row=3, column=3)
                Label(
                    text="Latest Accuracy: "
                    + str(df["Accuracy"].tail(1).values[0])
                    + "%",
                    font=("Noto Sans", 15),
                ).grid(row=4, column=3)

    def setting_tab(self, event=None):
        if self.open_tab != "Settings":
            self.open_tab = "Settings"
            self.title("SwiftQuill - Settings")
            self.clear()
            Label(self, text="Settings Options", font=("Noto Sans", 25)).grid(
                row=1, column=2, columnspan=3, pady=(0, 30)
            )

            self.op_language = StringVar(value=self.language)
            Label(self, text="Language", font=("Noto Sans", 15)).grid(
                row=2, column=2, padx=10, pady=10
            )
            ttk.Combobox(
                self, values=self.lang_list, width=15, textvariable=self.op_language
            ).grid(row=2, column=3, columnspan=2, padx=10, pady=10)

            self.op_tracking = BooleanVar(value=self.tracking)
            Label(self, text="Progress Tracking", font=("Noto Sans", 15)).grid(
                row=3, column=2, padx=10, pady=10
            )
            Radiobutton(
                self,
                text="Yes",
                variable=self.op_tracking,
                value=True,
                cursor="hand2",
                font=("Noto Sans", 12),
            ).grid(row=3, column=3, padx=10, pady=10)
            Radiobutton(
                self,
                text="No",
                variable=self.op_tracking,
                value=False,
                cursor="hand2",
                font=("Noto Sans", 12),
            ).grid(row=3, column=4, padx=10, pady=10)

            self.op_literature = BooleanVar(value=self.literature)
            Label(self, text="Text Type", font=("Noto Sans", 15)).grid(
                row=4, column=2, padx=10, pady=10
            )
            Radiobutton(
                self,
                text="Literature Writing",
                variable=self.op_literature,
                value=True,
                cursor="hand2",
                font=("Noto Sans", 12),
            ).grid(row=4, column=3, padx=10, pady=10)
            Radiobutton(
                self,
                text="Research Paper Writing",
                variable=self.op_literature,
                value=False,
                cursor="hand2",
                font=("Noto Sans", 12),
            ).grid(row=4, column=4, padx=10, pady=10)

            self.op_test_length = IntVar(value=self.test_length)
            Label(self, text="Test Length (Seconds)", font=("Noto Sans", 15)).grid(
                row=5, column=2, padx=10, pady=10
            )
            tle = Entry(
                self,
                validate="key",
                validatecommand=(
                    self.register(
                        lambda v: v.isdigit() or (not v and tle.get().isdigit())
                    ),
                    "%P",
                ),
                textvariable=self.op_test_length,
            )
            tle.grid(row=5, column=3, columnspan=2, padx=10, pady=10)

            self.op_graph_mean = IntVar(value=self.graph_mean)
            Label(self, text="Graph Mean (Simplicity)", font=("Noto Sans", 15)).grid(
                row=6, column=2, padx=10, pady=10
            )
            gme = Entry(
                self,
                validate="key",
                validatecommand=(
                    self.register(
                        lambda v: v.isdigit() or (not v and gme.get().isdigit())
                    ),
                    "%P",
                ),
                textvariable=self.op_graph_mean,
            )
            gme.grid(row=6, column=3, columnspan=2, padx=10, pady=10)
            Button(
                self, text="Save", font=("Noto Sans", 15), command=self.save_settings
            ).grid(row=7, column=2, columnspan=3, pady=50)

    def initialize_settings(self):
        with open("./settings.json", "r") as f:
            self.settings = json.load(f)
            self.language = self.settings["Language"]
            self.tracking = self.settings["Tracking"]
            self.test_length = self.settings["TestLength"]
            self.literature = self.settings["Literature"]
            self.graph_mean = self.settings["GraphMean"]
            self.cp_test_length = self.test_length

    def save_settings(self):
        current_settings = {
            "Language": self.op_language.get(),
            "Tracking": self.op_tracking.get(),
            "Literature": self.op_literature.get(),
            "TestLength": self.op_test_length.get(),
            "GraphMean": self.op_graph_mean.get(),
        }

        with open("./settings.json", "w") as f:
            json.dump(current_settings, f, indent=4)
            messagebox.showinfo("Success", "Settings saved successfully!")

        self.initialize_settings()

    def start_test(self):
        self.current_letter = 0
        self.fail = 0
        self.key_pressed = 0
        self.uie.delete(0, "end")
        self.uie.bind("<KeyRelease>", self.check_input)
        self.button.config(text="Stop", command=self.stop_test)
        self.update_timer()

    def stop_test(self):
        self.timer.config(text="Stopped!")
        self.pick_text()
        self.uie.delete(0, "end")
        self.uie.unbind("<KeyRelease>")
        self.test_length = self.cp_test_length
        self.button.config(text="Start", command=self.start_test)
        self.timer.after_cancel(self.count)
        self.canvas.delete("all")
        self.print_text()

    def check_input(self, event):
        if self.uie.get() and event.keysym == "BackSpace" and self.current_letter > 0:
            self.canvas.itemconfig(self.current_letter, fill="black")
            self.current_letter -= 1
            self.key_pressed += 1

        elif self.uie.get() and event.keysym not in ["Shift_L", "Shift_R"]:
            self.letter = self.uie.get()[-1]

            if self.letter == self.picked_text[self.current_letter]:
                self.canvas.itemconfig(self.current_letter + 1, fill="green")
                self.uie.delete(0, "end") if self.letter == " " else None
            else:
                self.canvas.itemconfig(self.current_letter + 1, fill="red")
                self.uie.delete(0, "end") if self.letter == " " else None
                self.fail += 1

            self.current_letter += 1
            self.key_pressed += 1
            if self.current_letter == len(self.picked_text):
                self.stop_test()
                self.add_data()

    def update_timer(self):
        self.timer.config(text=self.test_length)
        self.test_length -= 1
        self.count = self.timer.after(1000, self.update_timer)
        if self.test_length + 1 == 0:
            self.stop_test()
            self.add_data()

    def pick_text(self):
        self.type = (
            "Literature Writing.json"
            if self.literature
            else "Research Paper Writing.json"
        )
        with open(f"./Assets/{self.type}", "r") as f:
            self.texts = json.load(f)
            self.picked_text = self.texts[self.language][str(random.randint(1, 25))]

    def print_text(self):
        self.canvas = Canvas(
            self,
            width=705,
            height=350,
            background="#c3c3c3",
            borderwidth=3,
            highlightcolor="#373737",
            relief="solid",
        )
        self.canvas.grid(row=3, column=2, pady=10)
        x = 15
        y = 15

        for index, letter in enumerate(self.picked_text):
            self.index = self.canvas.create_text(x, y, text=letter, font=("Mono", 14))
            x += 11
            if x > 700:
                x = 15
                y += 25

    def add_data(self):
        if self.key_pressed > 15:
            self.accuracy = round(100 - (self.fail / self.key_pressed) * 100, 2)
            self.WPM = round(self.key_pressed / 5, 2)
            self.timer.configure(
                text="Accuracy: " + str(self.accuracy) + "% | WPM: " + str(self.WPM)
            )
            if self.tracking:
                self.date = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame(
                    [{"Date": self.date, "WPM": self.WPM, "Accuracy": self.accuracy}]
                )
                new_row.to_csv("Progress.csv", index=False, mode="a", header=False)
                self.analyse_data()
        else:
            self.timer.configure(text="Were you Active?")

    def analyse_data(self):
        df = pd.read_csv("Progress.csv")
        if df.shape[0] > 2:
            df["Accuracy"] = df["Accuracy"].rolling(window=self.graph_mean).mean()
            df["WPM"] = df["WPM"].rolling(window=self.graph_mean).mean()
            self.fig = go.Figure()
            self.fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df["Accuracy"],
                    name="Accuracy",
                    line=dict(color="crimson"),
                )
            )
            self.fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df["WPM"],
                    name="WPM",
                    line=dict(color="skyblue"),
                    yaxis="y2",
                )
            )
            self.fig.update_layout(
                title="Accuracy and WPM (Word Per Minute) Over Time",
                yaxis=dict(title="Accuracy in %", color="crimson"),
                yaxis2=dict(
                    title="Words Per Minute",
                    overlaying="y",
                    side="right",
                    color="skyblue",
                ),
                showlegend=False,
            )
            self.fig.write_image("./Assets/graph.png", width=750, height=425)

    def clear(self):
        for widget in self.winfo_children()[4:]:
            widget.destroy()

    def bindings(self):
        self.setting.bind(
            "<Enter>", lambda event: self.underline_on_hover(event, self.setting)
        )
        self.score.bind(
            "<Enter>", lambda event: self.underline_on_hover(event, self.score)
        )
        self.home.bind(
            "<Enter>", lambda event: self.underline_on_hover(event, self.home)
        )

        self.setting.bind(
            "<Leave>", lambda event: self.remove_underline(event, self.setting)
        )
        self.score.bind(
            "<Leave>", lambda event: self.remove_underline(event, self.score)
        )
        self.home.bind("<Leave>", lambda event: self.remove_underline(event, self.home))

        self.brand.bind(
            "<Button-1>",
            lambda event: webbrowser.open(
                "https://github.com/RedeemedSpoon/SwiftQuill"
            ),
        )
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
