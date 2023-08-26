import tkinter as tk
import threading
import time
import re
import psutil
import ctypes
import sys

class KeyloggerDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Keylogger Detector")

        self.start_button = tk.Button(self.root, text="Start Detector", command=self.start_detector)
        self.start_button.pack(pady=10)

        self.console_text = tk.Text(self.root, height=10, width=50, bg="black", fg="#0078D4")
        self.console_text.pack(pady=5)

    def start_detector(self):
        self.start_button.config(state=tk.DISABLED)
        self.clear_console_text()
        self.insert_console_text("Starting keylogger detection...")
        self.detect_keyloggers()
        self.insert_console_text("Detection complete.")
        self.start_button.config(state=tk.NORMAL)

    def insert_console_text(self, text):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        formatted_text = f"{timestamp} - INFO - {text}"
        self.console_text.insert(tk.END, formatted_text + "\n")
        self.console_text.see(tk.END)
        self.root.update()

    def clear_console_text(self):
        self.console_text.delete(1.0, tk.END)

    def detect_keyloggers(self):
        signature_pattern = re.compile(r'.*logs the keys struck on your keyboard.*covert manner.*', re.IGNORECASE)
        detected_keyloggers = []

        process_list = [
            "explorer.exe", "svchost.exe", "winlogon.exe", "csrss.exe", "lsass.exe",
            "spoolsv.exe", "notepad.exe", "iexplore.exe", "firefox.exe", "chrome.exe",
            "opera.exe", "edge.exe", "java.exe", "javaw.exe", "msword.exe", "excel.exe",
            "powerpnt.exe", "outlook.exe", "thunderbird.exe", "adobe_reader.exe",
            "acrotray.exe", "acrobat.exe", "vlc.exe", "media_player.exe", "spotify.exe"
        ]

        self.insert_console_text("Start scan...")
        time.sleep(1)

        for process_name in process_list:
            self.insert_console_text(f"Scanning process: {process_name}")
            process_description = self.get_process_description(process_name)
            self.insert_console_text(f"Retrieved process: {process_description}")

            if signature_pattern.match(process_description):
                detected_keyloggers.append(process_name)

            if self.heuristic_process_name(process_name) or self.heuristic_window_title(process_name):
                detected_keyloggers.append(process_name)

        time.sleep(1)
        self.insert_console_text("Complete scan.")

        if detected_keyloggers:
            self.insert_console_text("Detected keyloggers:")
            for keylogger in detected_keyloggers:
                self.insert_console_text(f"Process Name: {keylogger}")
                self.insert_console_text("=" * 30)
        else:
            self.insert_console_text("No keyloggers detected.")

    def get_process_description(self, process_name):
        try:
            for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
                if process.info['name'] == process_name:
                    return " ".join(process.info['cmdline'])
            return "Unknown process"
        except (IndexError, psutil.NoSuchProcess):
            return "Unknown process"

    def heuristic_process_name(self, process_name):
        return "keylogger" in process_name.lower()

    def heuristic_window_title(self, process_name):
        for window in psutil.process_iter(attrs=['pid', 'name']):
            if window.info['name'] == process_name:
                try:
                    window_title = window.info['name']
                    if "keylogger" in window_title.lower():
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        return False

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin():
        detector = KeyloggerDetector()
        detector.run()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)













