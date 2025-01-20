import os
import pickle
import logging

class Configuration:
    """Singleton class to manage global application settings like default profile."""
    
    _instance = None  # ✅ Singleton instance
    CONFIG_FILE = "config.dat"

    def __new__(cls, config_dir):
        """Ensure only one instance of Configuration exists."""
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._init_config(config_dir)
        return cls._instance

    def _init_config(self, config_dir):
        """Initialize configuration settings."""
        self.config_path = os.path.join(config_dir, self.CONFIG_FILE)
        self.default_profile = None
        self.load_config()

    def save_config(self):
        """Save configuration settings to a file."""
        try:
            with open(self.config_path, "wb") as file:
                pickle.dump({"default_profile": self.default_profile}, file)
                logging.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")
            raise

    def load_config(self):
        """Load configuration from a file, or create default if not found."""
        if not os.path.exists(self.config_path):
            logging.info("No configuration file found. Creating default configuration.")
            self.save_config()  # Create default configuration file
            return
        
        try:
            with open(self.config_path, "rb") as file:
                config_data = pickle.load(file)
                self.default_profile = config_data.get("default_profile", None)
                logging.info(f"Configuration loaded: Default profile = {self.default_profile}")
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            raise

    def set_default_profile(self, profile_id):
        """Set the default profile ID and save the configuration."""
        self.default_profile = profile_id
        self.save_config()
        logging.info(f"Default profile set to {profile_id}")

    def get_default_profile(self):
        """Retrieve the default profile ID."""
        return self.default_profile
