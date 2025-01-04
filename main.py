import os
import sys
import logging
from src import logging_config
from src.app_manager import launch_dashboard

# Default to DEV mode
IS_PROD = False

def create_directories(base_dir, is_prod):
    # Directory structure
    directories = ["budgets", "statements", "transactions"]

    for dir_name in directories:
        path = os.path.join(base_dir, dir_name)
        os.makedirs(path, exist_ok=True)

def check_logs_directory(logs_dir):
    if not os.path.exists(logs_dir):
        # Display an error dialog and exit
        import tkinter.messagebox as messagebox
        messagebox.showerror(
            "Error",
            "The application is in an unrecognized location. Please move it back to its original installation directory."
        )
        sys.exit(1)

def main():
    # Determine the mode
    is_prod = IS_PROD

    # Set base directory
    base_dir = os.path.expandvars(r"%userappdata%\BudgetTracker") if is_prod else os.path.join("src")

    # Create necessary directories
    create_directories(base_dir, is_prod)

    # Check logs directory only in PROD mode
    logs_dir = os.path.join(os.path.dirname(sys.argv[0]), "Logs") if is_prod else None
    if is_prod:
        check_logs_directory(logs_dir)

    logging_config.setup_logging("PROD" if is_prod else "DEV")

    # Launch the dashboard
    print(f"Running in {'PROD' if is_prod else 'DEV'} mode.")
    launch_dashboard(base_dir)

if __name__ == "__main__":
    main()