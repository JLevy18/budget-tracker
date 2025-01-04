import subprocess
import os
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

def print_green_bold(message):
    """
    Prints a message in green and bold.
    """
    print(f"{Style.BRIGHT}{Fore.GREEN}{message}")

def package_application():
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
            "--name=BudgetTracker",
            "--icon=resources/BudgetTracker.ico",
            "main.py",
        ]

        print_green_bold("Starting packaging process...")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffering
        )

        # Stream PyInstaller output in real-time
        for line in iter(process.stdout.readline, ""):
            print(f"{Fore.WHITE}{line.strip()}", flush=True)  # PyInstaller messages in white

        process.stdout.close()
        return_code = process.wait()

        if return_code == 0:
            print_green_bold("Packaging complete!")
        else:
            print(f"{Fore.RED}Error during packaging.")
    finally:
        # Revert the main.py back to its original state
        with open("main.py", "w") as file:
            file.write(main_code.replace("IS_PROD = True", "IS_PROD = False"))

if __name__ == "__main__":
    package_application()
