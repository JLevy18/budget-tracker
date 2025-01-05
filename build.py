import subprocess
import os
import time
import threading
from colorama import init, Fore, Style
import sys
import ctypes
import argparse

# Initialize colorama for colored output
init(autoreset=True)

def hide_cursor():
    """
    Hides the terminal cursor.
    """
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleCursorInfo(ctypes.windll.kernel32.GetStdHandle(-11), ctypes.byref(ctypes.c_int(1)))
    else:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    """
    Shows the terminal cursor.
    """
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleCursorInfo(ctypes.windll.kernel32.GetStdHandle(-11), ctypes.byref(ctypes.c_int(0)))
    else:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def show_progress_indicator(stop_event):
    """
    Displays a cascading "Building..." effect until the stop_event is set.
    """
    base_message = "Building"
    dots = ["", ".", "..", "..."]
    idx = 0

    hide_cursor()
    try:
        while not stop_event.is_set():
            print(f"\r{Style.BRIGHT}{Fore.YELLOW}{base_message}{dots[idx]:<3}", end="", flush=True)
            idx = (idx + 1) % len(dots)
            time.sleep(0.5)
    finally:
        show_cursor()  # Ensure cursor visibility is restored

def package_application(verbose=False):
    # Set IS_PROD in the code by replacing its default value before packaging
    with open("main.py", "r") as file:
        main_code = file.read()

    main_code = main_code.replace("IS_PROD = False", "IS_PROD = True")

    with open("main.py", "w") as file:
        file.write(main_code)

    try:
        # Build the application using PyInstaller
        command = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--name=BudgetTracker",
            "--icon=resources/BudgetTracker.ico",
            "--add-data=src/ui/dashboard.kv;src/ui",
            "main.py",
        ]

        print(f"{Style.BRIGHT}{Fore.BLUE}Starting build...")

        if verbose:
            # Run with real-time output display
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            try:
                for line in iter(process.stdout.readline, ""):
                    print(f"{Fore.WHITE}{line.strip()}")
            finally:
                process.stdout.close()
                return_code = process.wait()
                if return_code == 0:
                    print(f"\n{Style.BRIGHT}{Fore.GREEN}Build FINISHED")
                else:
                    print(f"\n{Style.BRIGHT}{Fore.RED}Error during packaging.")
        else:
            # Start the progress indicator in a separate thread
            stop_event = threading.Event()
            progress_thread = threading.Thread(target=show_progress_indicator, args=(stop_event,))
            progress_thread.start()

            try:
                process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Stop the progress indicator
                stop_event.set()
                progress_thread.join()

                # Create Logs directory in the dist folder
                logs_dir = os.path.join("dist", "Logs")
                os.makedirs(logs_dir, exist_ok=True)

                if process.returncode == 0:
                    print(f"\n{Style.BRIGHT}{Fore.GREEN}Build FINISHED:" + f"\n{Style.BRIGHT}{Fore.WHITE}- dist/BudgetTracker.exe")
                else:
                    print(f"\n{Style.BRIGHT}{Fore.RED}Error during packaging.")
                    print(process.stderr)
            except KeyboardInterrupt:
                stop_event.set()
                progress_thread.join()
                print(f"\n{Style.BRIGHT}{Fore.RED}Packaging canceled by user.")

    finally:
        # Revert the main.py back to its original state
        with open("main.py", "w") as file:
            file.write(main_code.replace("IS_PROD = True", "IS_PROD = False"))
        show_cursor()  # Ensure cursor visibility is restored even on errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package the Budget Tracker application.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    package_application(verbose=args.verbose)
