import os
import sys
import logging
from src import logging_config
from src.app_manager import initialize_app
from src.data_manager import set_data_manager

# Default to DEV mode
IS_PROD = False

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
    base_dir = os.path.expandvars(r"%appdata%\BudgetTracker") if is_prod else os.path.join("src")

    # Check logs directory only in PROD mode
    logs_dir = os.path.join(os.path.dirname(sys.argv[0]), "Logs") if is_prod else None
    if is_prod:
        check_logs_directory(logs_dir)

    logging_config.setup_logging("PROD" if is_prod else "DEV")

    # Launch the dashboard
    data_manager, app = initialize_app(base_dir, is_prod)
    set_data_manager(data_manager)
    app.run()

if __name__ == "__main__":
    main()