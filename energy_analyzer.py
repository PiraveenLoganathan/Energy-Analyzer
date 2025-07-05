import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

def plot_daily_usage(df):
    daily = df['energy_kWh'].resample('D').sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    daily.plot(ax=ax, color="#2e8b57", linewidth=2)

    ax.set_title("Daily Energy Usage", fontsize=12, fontname="Helvetica Neue")
    ax.set_ylabel("Energy (kWh)", fontsize=10, fontname="Helvetica Neue")
    ax.set_xlabel("Date", fontsize=10, fontname="Helvetica Neue")

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45, ha='right', fontname="Helvetica Neue")
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    plot_win = tk.Toplevel()
    plot_win.wm_title("Daily Energy Usage Plot")
    canvas = FigureCanvasTkAgg(fig, master=plot_win)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

def detect_night_usage(df, output_widget):
    df['hour'] = df.index.hour
    night_df = df[(df['hour'] >= 0) & (df['hour'] <= 5)]
    avg = night_df['energy_kWh'].mean()
    msg = f"Night usage: {avg:.2f} kWh\n"
    msg += "⚠️ Consider reducing overnight usage." if avg > 3 else "✅ Within normal range."

    output_widget.configure(state='normal')
    output_widget.delete(1.0, tk.END)
    output_widget.insert(tk.END, msg)
    output_widget.configure(state='disabled')

def forecast(df, output_widget):
    daily = df['energy_kWh'].resample('D').sum().reset_index()
    daily['day_num'] = (daily['timestamp'] - daily['timestamp'].min()).dt.days
    X = daily[['day_num']]
    y = daily['energy_kWh']

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.array([[X['day_num'].max() + i] for i in range(1, 8)])
    predictions = model.predict(future_days)
    future_dates = pd.date_range(start=daily['timestamp'].max() + pd.Timedelta(days=1), periods=7)

    text = "Next 7 Days Forecast:\n"
    for d, p in zip(future_dates, predictions):
        text += f"{d.date()}: {p:.2f} kWh\n"
    output_widget.configure(state='normal')
    output_widget.delete(1.0, tk.END)
    output_widget.insert(tk.END, text)
    output_widget.configure(state='disabled')

def center_window(win, width=580, height=460):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

class GreenEnergyAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy Analyzer")
        center_window(self.root)
        self.root.configure(bg="#eef6ef")
        self.show_welcome_screen()

    def show_welcome_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        card = tk.Frame(self.root, bg="#ffffff", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=180)

        welcome_label = tk.Label(card, text="Welcome to Energy Analyzer",
                                 font=("Helvetica Neue", 14),
                                 fg="#2e8b57", bg="#ffffff")
        welcome_label.pack(pady=(30, 10))

        add_csv_btn = tk.Button(card, text="Upload CSV",
                                font=("Helvetica Neue", 11),
                                bg="#a3d9a5", fg="black",
                                activebackground="#8ccf90",
                                width=18, height=1,
                                bd=0,
                                command=self.load_csv)
        add_csv_btn.pack()

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select Energy Data CSV",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not filepath:
            messagebox.showinfo("No file selected", "No CSV file was selected.")
            return

        try:
            df = pd.read_csv(filepath, parse_dates=["timestamp"])
            df.dropna(inplace=True)
            df.set_index("timestamp", inplace=True)
            df.sort_index(inplace=True)
            self.df = df
            self.show_main_ui()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load CSV:\n{e}")

    def show_main_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        card = tk.Frame(self.root, bg="#ffffff", bd=0)
        card.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.output = scrolledtext.ScrolledText(card, wrap=tk.WORD, height=8,
                                                font=("Helvetica Neue", 10),
                                                state='disabled', bg="#f0fdf0",
                                                relief=tk.FLAT, borderwidth=0)
        self.output.pack(padx=20, pady=(10, 25), fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.pack(pady=10)

        def make_button(text, command):
            return tk.Button(btn_frame, text=text, command=command,
                             font=("Helvetica Neue", 10), bg="#a3d9a5", fg="black",
                             activebackground="#8ccf90", relief=tk.FLAT, bd=0, width=20)

        make_button("Plot Daily Usage", lambda: plot_daily_usage(self.df)).grid(row=0, column=0, padx=8, pady=4)
        make_button("Detect Night Usage", lambda: detect_night_usage(self.df, self.output)).grid(row=0, column=1, padx=8, pady=4)
        make_button("Forecast Usage", lambda: forecast(self.df, self.output)).grid(row=0, column=2, padx=8, pady=4)

        tk.Button(card, text="Exit", command=self.root.destroy,
                  bg="#dbeedb", font=("Helvetica Neue", 10),
                  relief=tk.FLAT, bd=0, width=64).pack(pady=10)

def main():
    root = tk.Tk()
    app = GreenEnergyAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
