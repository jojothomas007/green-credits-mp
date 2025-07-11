from src.transcribe_test.config import Config
from src.transcribe_test.gui.layouts import App

Config.load_config()
root = App.create_window()
# Run the application
root.mainloop()