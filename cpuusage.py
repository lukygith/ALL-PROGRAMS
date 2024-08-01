import tkinter as tk
from tkinter import ttk
import psutil
import time

class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor")
        self.geometry("300x200")
        
        # CPU Usage
        self.cpu_label = ttk.Label(self, text="CPU Usage: ", font=('Arial', 12))
        self.cpu_label.pack(pady=10)
        
        # Memory Usage
        self.memory_label = ttk.Label(self, text="Memory Usage: ", font=('Arial', 12))
        self.memory_label.pack(pady=10)
        
        # Network Usage
        self.network_label = ttk.Label(self, text="Network Usage: ", font=('Arial', 12))
        self.network_label.pack(pady=10)
        
        # Update data every second
        self.update_data()
    
    def update_data(self):
        # CPU Usage
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        
        # Memory Usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
        
        # Network Usage
        net = psutil.net_io_counters()
        network_usage = f"In: {net.bytes_recv / (1024 ** 2):.2f} MB, Out: {net.bytes_sent / (1024 ** 2):.2f} MB"
        self.network_label.config(text=f"Network Usage: {network_usage}")
        
        # Call this method again after 1 second
        self.after(1000, self.update_data)

if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()
