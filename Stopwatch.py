import tkinter as tk
from datetime import datetime, timedelta
import ctypes
import random

class Stopwatch(tk.Tk):
    is_paused = False
    flash_interval = timedelta(minutes=60)

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("+{}+{}".format(self.winfo_screenwidth() - 200, self.winfo_screenheight() // 2 - 50))
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)

        self.title_bar = tk.Frame(self, bg="blue", relief="raised", bd=2)
        self.title_bar.pack(fill="x")

        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_drag)
        self.title_bar.bind("<B1-Motion>", self.drag_window)
        self.title_bar.bind("<Button-3>", self.show_popup_menu)

        self.drag_button = tk.Label(self.title_bar, text="Productivity timer", bg="blue", fg="white")
        self.drag_button.pack(side="left")

        self.close_button = tk.Button(self.title_bar, text="X", command=self.destroy, bg="blue", fg="white")
        self.close_button.pack(side="right")

        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(fill="both", expand=True)

        self.clock_frame = tk.Frame(self.content_frame, bg="white")
        self.clock_frame.pack()

        self.label = tk.Label(self.clock_frame, font=("Helvetica", 32))
        self.label.pack()

        self.counter_frame = tk.Frame(self.content_frame, bg="white")
        self.counter_frame.pack()

        self.counter_label = tk.Label(self.counter_frame, font=("Helvetica", 10))
        self.counter_label.pack()

        self.interval_label = tk.Label(self.counter_frame, font=("Helvetica", 10))
        self.interval_label.pack()

        self.start_time = datetime.now()
        self.update_clock()
        self.interval_count = 0
        self.interval_handler_id = None

        # Create restart and pause buttons
        button_font = ("Helvetica", 12)
        self.button_frame = tk.Frame(self.content_frame, bg="white")
        self.button_frame.pack()

        self.restart_button = tk.Button(self.button_frame, text="Restart", font=button_font, command=self.restart)
        self.restart_button.pack(side="left", padx=5)
        self.pause_button = tk.Button(self.button_frame, text="Pause", font=button_font, command=self.pause_resume)
        self.pause_button.pack(side="left", padx=5)

        self.is_dragging = False
        self.start_x = 0
        self.start_y = 0

        # Create right-click popup menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.interval_menu = tk.Menu(self.popup_menu, tearoff=0)
        self.interval_menu.add_command(label="TEST 10 sec", command=lambda: self.set_flash_interval(minutes=1/6))
        self.interval_menu.add_command(label="1 minute", command=lambda: self.set_flash_interval(minutes=1))
        self.interval_menu.add_command(label="5 minutes", command=lambda: self.set_flash_interval(minutes=5))
        self.interval_menu.add_command(label="10 minutes", command=lambda: self.set_flash_interval(minutes=10))
        self.interval_menu.add_command(label="15 minutes", command=lambda: self.set_flash_interval(minutes=15))
        self.interval_menu.add_command(label="30 minutes", command=lambda: self.set_flash_interval(minutes=30))
        self.interval_menu.add_command(label="45 minutes", command=lambda: self.set_flash_interval(minutes=45))
        self.interval_menu.add_command(label="60 minutes", command=lambda: self.set_flash_interval(minutes=60))
        self.interval_menu.add_command(label="90 minutes", command=lambda: self.set_flash_interval(minutes=90))
        self.popup_menu.add_cascade(label="Interval", menu=self.interval_menu)

    def update_clock(self):
        if not self.is_paused:
            elapsed_time = datetime.now() - self.start_time
            self.label.config(text=str(elapsed_time)[:-7])  # Remove milliseconds
        self.after(50, self.update_clock)

    def restart(self):
        self.stop_interval_handler()  # Stop the previous interval handler
        self.start_time = datetime.now()
        self.is_paused = False
        self.interval_count = 0
        self.update_counter()
        self.start_interval_handler()  # Start a new interval handler

    def pause_resume(self):
        self.is_paused = not self.is_paused

    def start_drag(self, event):
        self.is_dragging = True
        self.start_x = event.x
        self.start_y = event.y

    def stop_drag(self, event):
        self.is_dragging = False

    def drag_window(self, event):
        if self.is_dragging:
            x = self.winfo_pointerx() - self.start_x
            y = self.winfo_pointery() - self.start_y
            self.geometry("+{}+{}".format(x, y))

    def flash_window(self):
        colors = ['red', 'green', 'blue', 'yellow', 'orange']
        random.shuffle(colors)
        self.flash_sequence(colors)

    def flash_sequence(self, colors):
        if colors:
            color = colors.pop(0)
            self.title_bar.configure(bg=color)
            self.drag_button.configure(bg=color)
            self.after(500, self.flash_sequence, colors)
        else:
            self.title_bar.configure(bg="blue")  # Restore the title bar color
            self.drag_button.configure(bg="blue")  # Restore the drag button color

    def update_counter(self):
        self.counter_label.config(text=f"Intervals: {self.interval_count}")
        self.interval_label.config(text=f"Interval {self.flash_interval.total_seconds() // 60} minutes")

    def set_flash_interval(self, minutes):
        self.flash_interval = timedelta(minutes=minutes)  # Convert minutes to seconds
        self.interval_count = 0  # Reset interval count
        self.update_counter()
        self.restart()  # Restart the stopwatch

    def show_popup_menu(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def start_interval_handler(self):
        if not self.is_paused:
            self.interval_handler_id = self.after(int(self.flash_interval.total_seconds() * 1000), self.interval_handler)
    
    def stop_interval_handler(self):
        if self.interval_handler_id is not None:
            self.after_cancel(self.interval_handler_id)
            self.interval_handler_id = None
    
    def interval_handler(self):
        self.flash_window()
        self.interval_count += 1
        self.update_counter()
        self.start_interval_handler()

def on_system_start():
    stopwatch = Stopwatch()
    stopwatch.update_counter()
    stopwatch.start_interval_handler()

    # Set the window attributes to allow color changes on the title bar
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_uint(2)), 4)

if __name__ == '__main__':
    on_system_start()
    tk.mainloop()
