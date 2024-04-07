import tkinter as tk
import time
import os

class ClickPerSecondTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Click Per Second Test")
        self.master.configure(bg="black")
        self.master.geometry("430x460")

        self.click_count = 0
        self.start_time = None
        self.duration = 10  # Default duration of the test in seconds

        self.label = tk.Label(self.master, text="Enter your name and click Start Test!", font=("Arial", 14),
                              fg="white", bg="black")
        self.label.pack(pady=10)

        self.name_entry = tk.Entry(self.master, font=("Arial", 12), bg="black", fg="white", insertbackground="white")
        self.name_entry.pack(pady=5)

        self.entry = tk.Entry(self.master, font=("Arial", 12), bg="black", fg="white", insertbackground="white")
        self.entry.pack(pady=5)
        self.entry.insert(0, str(self.duration))

        self.new_button = tk.Button(self.master, text="Click Me!", font=("Arial", 16), command=self.handle_click,
                                    bg="#39FF14", fg="black", activebackground="#00FF00", activeforeground="black")
        self.leaderboard_frame = tk.Frame(self.master, bg="black")
        self.leaderboard_frame.pack(pady=10)

        self.leaderboard_label = tk.Label(self.leaderboard_frame, text="Leaderboard:", font=("Arial", 14),
                                          fg="white", bg="black")
        self.leaderboard_label.pack(side=tk.LEFT, padx=(0, 10))

        self.leaderboard_text = tk.Text(self.leaderboard_frame, font=("Arial", 12), bg="black", fg="white", width=30,
                                         height=10)
        self.leaderboard_text.pack(side=tk.LEFT)
        self.load_leaderboard()

        self.start_button = tk.Button(self.master, text="Start Test", font=("Arial", 16), command=self.start_test,
                                      bg="#39FF14", fg="black", activebackground="#00FF00", activeforeground="black")
        self.start_button.pack(pady=5)

    def start_test(self):
        name = self.name_entry.get().strip()
        if not name:
            self.label.config(text="Please enter your name!", fg="red")
            return
        try:
            self.duration = int(self.entry.get())
            if self.duration <= 0:
                raise ValueError("Duration must be greater than 0")
        except ValueError:
            self.label.config(text="Please enter a valid duration (positive integer)!", fg="red")
        else:
            self.click_count = 0
            self.start_time = time.time()
            self.start_button.pack_forget()  # Remove the start button from the window
            self.name_entry.config(state=tk.DISABLED)
            self.entry.config(state=tk.DISABLED)
            self.label.config(text="Test in progress...", fg="#39FF14")
            self.new_button.pack(pady=20)
            self.update_label()

    def handle_click(self):
        self.click_count += 1

    def update_label(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.duration:
                self.display_result()
            else:
                time_left = self.duration - elapsed_time
                time_color = self.get_time_color(time_left)
                clicks_per_second = self.click_count / elapsed_time if elapsed_time > 0 else 0
                self.label.config(text=f"Time left: {int(time_left)} seconds\n"
                                        f"Clicks per second: {clicks_per_second:.2f}",
                                  fg=time_color)
                self.master.after(100, self.update_label)  # Update label every 100 milliseconds

    def display_result(self):
        name = self.name_entry.get()
        cps = self.click_count / self.duration
        self.label.config(text=f"Test completed!\n"
                                f"Clicks per second: {cps:.2f}", fg="#39FF14")
        self.new_button.config(state=tk.DISABLED)  # Disable the button after the test is completed
        self.update_leaderboard(name, cps)

    def get_time_color(self, time_left):
        if time_left <= 0:
            return "red"
        elif time_left <= 3:
            return "orange"
        elif time_left <= 5:
            return "yellow"
        else:
            return "#39FF14"  # Green

    def load_leaderboard(self):
        leaderboard_data = self.get_leaderboard_data()
        sorted_leaderboard = sorted(leaderboard_data.items(), key=lambda x: x[1], reverse=True)
        for name, score in sorted_leaderboard:
            self.leaderboard_text.insert(tk.END, f"{name}: {score:.2f} clicks per second\n")

    def get_leaderboard_data(self):
        leaderboard_data = {}
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(": ")
                    name = parts[0]
                    score = float(parts[1].split()[0])  # Extracting the score
                    leaderboard_data[name] = score
        return leaderboard_data

    def update_leaderboard(self, name, cps):
        with open("leaderboard.txt", "a") as file:
            file.write(f"{name}: {cps:.2f} clicks per second\n")
        self.leaderboard_text.delete("1.0", tk.END)
        self.load_leaderboard()

def main():
    root = tk.Tk()
    app = ClickPerSecondTest(root)
    root.iconbitmap("Click.ico") 
    root.mainloop()

if __name__ == "__main__":
    main()
